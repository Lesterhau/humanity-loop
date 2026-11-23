-- REVIEW-ONLY CANDIDATE. DO NOT APPLY TO PRODUCTION WITHOUT CUTOVER REVIEW.
-- PostgreSQL 15/16, production canonical relation hl_control.tasks. No parallel
-- ledger, service keys, scheduled jobs or new paid provider is introduced.
--
-- Fenced tasks start HELD with payload:
-- {"fencing_required":"true","idempotency_key":"unique-immutable-task-operation"}
-- A client without a fresh (lease_owner, lease_epoch, lease_token) tuple cannot
-- advance, renew, abort or complete a fenced task; expiry dead-letters, never
-- silently replays external actions.
BEGIN;

ALTER TABLE hl_control.tasks
  ADD COLUMN IF NOT EXISTS fenced_epoch bigint NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS fenced_token uuid;

DO $guard$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conrelid='hl_control.tasks'::regclass AND conname='tasks_fenced_epoch_nonnegative'
  ) THEN
    ALTER TABLE hl_control.tasks ADD CONSTRAINT tasks_fenced_epoch_nonnegative
      CHECK (fenced_epoch >= 0);
  END IF;
END $guard$;

-- Existing general claim API must NEVER claim an opt-in fenced record even
-- if a legacy administrator accidentally returns it to queued state.
CREATE OR REPLACE FUNCTION hl_control.claim_next_task(
  p_agent_id text, p_lease_seconds integer DEFAULT 300
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE claimed hl_control.tasks;
BEGIN
  UPDATE hl_control.tasks
  SET status='leased',
      lease_owner=p_agent_id,
      lease_expires_at=clock_timestamp()+make_interval(secs => greatest(p_lease_seconds,1))
  WHERE task_id=(
    SELECT task_id FROM hl_control.tasks
    WHERE status='queued'
      AND coalesce(payload->>'fencing_required','false') <> 'true'
      AND (human_approval_required=false OR human_approval_received=true)
    ORDER BY priority DESC,created_at
    FOR UPDATE SKIP LOCKED
    LIMIT 1
  )
  RETURNING * INTO claimed;
  IF claimed.task_id IS NOT NULL THEN
    INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
    VALUES ('task_claimed',claimed.task_id,p_agent_id,claimed.project_id,
            jsonb_build_object('lease_expires_at',claimed.lease_expires_at));
  END IF;
  RETURN claimed;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.claim_fenced_task_v1(
  p_task_id text, p_agent_id text, p_idempotency_key text,
  p_lease_seconds integer DEFAULT 60
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE claimed hl_control.tasks;
BEGIN
  IF p_task_id IS NULL OR length(p_task_id)<6 OR
     p_agent_id IS NULL OR length(p_agent_id)<6 OR
     p_idempotency_key IS NULL OR length(p_idempotency_key)<12 OR
     length(p_idempotency_key)>128 OR
     p_lease_seconds IS NULL OR p_lease_seconds NOT BETWEEN 1 AND 300 THEN
    RAISE EXCEPTION 'fenced_claim_invalid_arguments';
  END IF;
  IF NOT EXISTS(
    SELECT 1 FROM hl_control.agents
    WHERE agent_id=p_agent_id AND status='active'
      AND permissions @> '["tier0"]'::jsonb
      AND (expires_at IS NULL OR expires_at > clock_timestamp())
  ) THEN
    RAISE EXCEPTION 'fenced_claim_unapproved_agent';
  END IF;

  UPDATE hl_control.tasks
  SET status='leased',
      lease_owner=p_agent_id,
      lease_expires_at=clock_timestamp()+make_interval(secs => p_lease_seconds),
      fenced_epoch=fenced_epoch+1,
      fenced_token=gen_random_uuid(),
      updated_at=clock_timestamp()
  WHERE task_id=p_task_id AND status='held'
    AND risk_tier=0
    AND payload->>'fencing_required'='true'
    AND payload->>'idempotency_key'=p_idempotency_key
    -- V1 is deterministic only: a valid lease is NEVER paid-model authority.
    AND payload->>'execution_mode'='deterministic_only'
    AND payload->>'external_actions'='false'
    AND payload->>'model_calls'='0'
    AND payload->>'max_provider_credits'='0'
    AND (human_approval_required=false OR human_approval_received=true)
    AND lease_owner IS NULL
    AND fenced_token IS NULL
    AND attempts<max_attempts
  RETURNING * INTO claimed;

  IF claimed.task_id IS NULL THEN
    RAISE EXCEPTION 'fenced_task_unavailable_or_already_leased';
  END IF;
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES ('fenced_task_claimed',claimed.task_id,p_agent_id,claimed.project_id,
          jsonb_build_object('epoch',claimed.fenced_epoch,
                             'lease_expires_at',claimed.lease_expires_at));
  RETURN claimed;
END $fn$;

-- Lock the canonical row so every check and mutation happens in one transaction.
-- A NEW lease for the SAME owner still has a NEW epoch and token. Old workers
-- cannot complete after expiration/rearming.
CREATE OR REPLACE FUNCTION hl_control.advance_fenced_stage_v1(
  p_task_id text, p_agent_id text, p_fenced_epoch bigint, p_fenced_token uuid,
  p_stage text, p_result jsonb, p_next_stage text DEFAULT NULL,
  p_complete boolean DEFAULT false
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks; v_ord bigint; expected_next text;
BEGIN
  IF p_fenced_token IS NULL OR p_fenced_epoch IS NULL OR
     p_stage IS NULL OR p_result IS NULL OR
     jsonb_typeof(p_result)<>'object' OR pg_column_size(p_result)>16384 THEN
    RAISE EXCEPTION 'fenced_stage_invalid_arguments';
  END IF;
  SELECT * INTO t FROM hl_control.tasks
  WHERE task_id=p_task_id FOR UPDATE;
  IF t.task_id IS NULL OR
     t.payload->>'fencing_required' IS DISTINCT FROM 'true' OR
     t.status<>'leased' OR
     t.lease_owner IS DISTINCT FROM p_agent_id OR
     t.fenced_epoch IS DISTINCT FROM p_fenced_epoch OR
     t.fenced_token IS DISTINCT FROM p_fenced_token OR
     t.lease_expires_at IS NULL OR t.lease_expires_at<=clock_timestamp() OR
     t.current_stage IS DISTINCT FROM p_stage OR
     t.stage_results ? p_stage THEN
    RAISE EXCEPTION 'fenced_stage_stale_or_unauthorized';
  END IF;

  SELECT stage_no INTO v_ord
  FROM jsonb_array_elements_text(t.stages) WITH ORDINALITY AS s(stage_name,stage_no)
  WHERE stage_name=p_stage
  ORDER BY stage_no LIMIT 1;
  IF v_ord IS NULL OR jsonb_typeof(t.stages)<>'array' THEN
    RAISE EXCEPTION 'fenced_stage_not_in_sequence';
  END IF;
  expected_next := t.stages->>(v_ord::integer);  -- JSON index 1 denotes second stage.
  IF (expected_next IS NULL AND (p_complete IS DISTINCT FROM true OR p_next_stage IS NOT NULL))
  OR (expected_next IS NOT NULL AND (p_complete IS DISTINCT FROM false OR
       p_next_stage IS DISTINCT FROM expected_next)) THEN
    RAISE EXCEPTION 'fenced_stage_invalid_transition';
  END IF;

  UPDATE hl_control.tasks
  SET stage_results=stage_results||jsonb_build_object(p_stage,p_result),
      current_stage=CASE WHEN p_complete THEN NULL ELSE p_next_stage END,
      status=CASE WHEN p_complete THEN 'completed' ELSE 'leased' END,
      completed_at=CASE WHEN p_complete THEN clock_timestamp() ELSE completed_at END,
      lease_owner=CASE WHEN p_complete THEN NULL ELSE lease_owner END,
      lease_expires_at=CASE WHEN p_complete THEN NULL ELSE lease_expires_at END,
      fenced_token=CASE WHEN p_complete THEN NULL ELSE fenced_token END,
      updated_at=clock_timestamp()
  WHERE task_id=p_task_id
  RETURNING * INTO t;

  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES (CASE WHEN p_complete THEN 'fenced_task_completed' ELSE 'fenced_stage_advanced' END,
          t.task_id,p_agent_id,t.project_id,
          jsonb_build_object('stage',p_stage,'epoch',p_fenced_epoch,
                             'next_stage',p_next_stage,'complete',p_complete));
  RETURN t;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.renew_fenced_lease_v1(
  p_task_id text,p_agent_id text,p_fenced_epoch bigint,p_fenced_token uuid,
  p_lease_seconds integer DEFAULT 60
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks;
BEGIN
  IF p_lease_seconds IS NULL OR p_lease_seconds NOT BETWEEN 1 AND 300 OR
     p_fenced_token IS NULL THEN
    RAISE EXCEPTION 'fenced_renew_invalid_arguments';
  END IF;
  UPDATE hl_control.tasks
  SET lease_expires_at=clock_timestamp()+make_interval(secs=>p_lease_seconds),
      updated_at=clock_timestamp()
  WHERE task_id=p_task_id AND status='leased'
    AND payload->>'fencing_required'='true'
    AND lease_owner=p_agent_id
    AND fenced_epoch=p_fenced_epoch AND fenced_token=p_fenced_token
    AND lease_expires_at>clock_timestamp()
  RETURNING * INTO t;
  IF t.task_id IS NULL THEN
    RAISE EXCEPTION 'fenced_renew_stale_or_unauthorized';
  END IF;
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES ('fenced_lease_renewed',t.task_id,p_agent_id,t.project_id,
          jsonb_build_object('epoch',t.fenced_epoch,'lease_expires_at',t.lease_expires_at));
  RETURN t;
END $fn$;

-- A genuinely failed task is held for review. Never automatically repeat
-- the external side effect or the 8 model calls under a new lease.
CREATE OR REPLACE FUNCTION hl_control.fail_fenced_task_v1(
  p_task_id text,p_agent_id text,p_fenced_epoch bigint,p_fenced_token uuid,
  p_reason text
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks;
BEGIN
  IF p_reason IS NULL OR p_reason NOT IN
      ('verifier_hold','safety_hold','deadline_exhausted','model_error','operator_abort') THEN
    RAISE EXCEPTION 'fenced_failure_reason_invalid';
  END IF;
  UPDATE hl_control.tasks
  SET status='dead_letter',attempts=attempts+1,
      lease_owner=NULL,lease_expires_at=NULL,fenced_token=NULL,
      updated_at=clock_timestamp()
  WHERE task_id=p_task_id AND status='leased'
    AND payload->>'fencing_required'='true'
    AND lease_owner=p_agent_id
    AND fenced_epoch=p_fenced_epoch AND fenced_token=p_fenced_token
    AND lease_expires_at>clock_timestamp()
  RETURNING * INTO t;
  IF t.task_id IS NULL THEN
    RAISE EXCEPTION 'fenced_fail_stale_or_unauthorized';
  END IF;
  INSERT INTO hl_control.dead_letters(task_id,project_id,reason,snapshot)
  VALUES (t.task_id,t.project_id,p_reason,
          jsonb_build_object('epoch',p_fenced_epoch,'reason',p_reason));
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES ('fenced_task_dead_letter',t.task_id,p_agent_id,t.project_id,
          jsonb_build_object('epoch',p_fenced_epoch,'reason',p_reason));
  RETURN t;
END $fn$;

-- Administrator-only recovery: expired fenced leases DEAD-LETTER, never requeue.
-- No scheduled invocation is created. Future manual retry requires separate
-- review and an explicit new idempotency operation.
CREATE OR REPLACE FUNCTION hl_control.expire_fenced_task_v1(p_task_id text)
RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks; previous_owner text;
BEGIN
  SELECT * INTO t FROM hl_control.tasks WHERE task_id=p_task_id FOR UPDATE;
  IF t.task_id IS NULL OR t.status<>'leased' OR
     t.payload->>'fencing_required' IS DISTINCT FROM 'true' OR
     t.lease_expires_at IS NULL OR t.lease_expires_at>clock_timestamp() THEN
    RAISE EXCEPTION 'fenced_expiry_not_eligible';
  END IF;
  previous_owner := t.lease_owner;
  UPDATE hl_control.tasks
  SET status='dead_letter',attempts=attempts+1,
      lease_owner=NULL,lease_expires_at=NULL,fenced_token=NULL,
      updated_at=clock_timestamp()
  WHERE task_id=p_task_id RETURNING * INTO t;
  INSERT INTO hl_control.dead_letters(task_id,project_id,reason,snapshot)
  VALUES (t.task_id,t.project_id,'lease_expired',
          jsonb_build_object('epoch',t.fenced_epoch));
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES ('fenced_lease_expired_dead_letter',t.task_id,previous_owner,
          t.project_id,jsonb_build_object('epoch',t.fenced_epoch));
  RETURN t;
END $fn$;

-- Prevent the old stage/renew/fail paths from bypassing fenced token checks.
-- They continue to serve only PRE-EXISTING unfenced task IDs.
CREATE OR REPLACE FUNCTION hl_control.advance_task_stage(
  p_task_id text,p_agent_id text,p_stage text,p_result jsonb,
  p_next_stage text DEFAULT NULL,p_complete boolean DEFAULT false
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks;
BEGIN
  SELECT * INTO t FROM hl_control.tasks WHERE task_id=p_task_id FOR UPDATE;
  IF t.task_id IS NULL THEN RAISE EXCEPTION 'task_not_found'; END IF;
  IF t.payload->>'fencing_required'='true' THEN
    RAISE EXCEPTION 'fenced_task_requires_token';
  END IF;
  IF t.status<>'leased' OR t.lease_owner IS DISTINCT FROM p_agent_id THEN
    RAISE EXCEPTION 'task_not_leased_by_agent';
  END IF;
  IF t.lease_expires_at IS NOT NULL AND t.lease_expires_at<clock_timestamp() THEN
    RAISE EXCEPTION 'legacy_lease_expired';
  END IF;
  IF t.current_stage IS DISTINCT FROM p_stage THEN RAISE EXCEPTION 'stage_mismatch'; END IF;
  UPDATE hl_control.tasks SET
    stage_results=stage_results||jsonb_build_object(p_stage,coalesce(p_result,'{}'::jsonb)),
    current_stage=CASE WHEN p_complete THEN NULL ELSE p_next_stage END,
    status=CASE WHEN p_complete THEN 'completed' ELSE 'leased' END,
    completed_at=CASE WHEN p_complete THEN clock_timestamp() ELSE completed_at END
  WHERE task_id=p_task_id RETURNING * INTO t;
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES (CASE WHEN p_complete THEN 'task_completed' ELSE 'stage_completed' END,
          t.task_id,p_agent_id,t.project_id,
          jsonb_build_object('stage',p_stage,'next_stage',p_next_stage,'complete',p_complete));
  RETURN t;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.advance_task_stage_v2(
  p_task_id text,p_lease_owner_id text,p_role_agent_id text,p_stage text,
  p_result jsonb,p_next_stage text DEFAULT NULL,p_complete boolean DEFAULT false
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks; r hl_control.agents;
BEGIN
  SELECT * INTO r FROM hl_control.agents WHERE agent_id=p_role_agent_id;
  IF r.agent_id IS NULL OR r.status<>'active' OR
     r.parent_id IS DISTINCT FROM p_lease_owner_id THEN
    RAISE EXCEPTION 'invalid_role_agent_parent';
  END IF;
  SELECT * INTO t FROM hl_control.tasks WHERE task_id=p_task_id FOR UPDATE;
  IF t.task_id IS NULL THEN RAISE EXCEPTION 'task_not_found'; END IF;
  IF t.payload->>'fencing_required'='true' THEN
    RAISE EXCEPTION 'fenced_task_requires_token';
  END IF;
  IF t.status<>'leased' OR t.lease_owner IS DISTINCT FROM p_lease_owner_id THEN
    RAISE EXCEPTION 'task_not_leased_by_agent';
  END IF;
  IF t.lease_expires_at IS NOT NULL AND t.lease_expires_at<clock_timestamp() THEN
    RAISE EXCEPTION 'legacy_lease_expired';
  END IF;
  IF t.current_stage IS DISTINCT FROM p_stage THEN RAISE EXCEPTION 'stage_mismatch'; END IF;
  UPDATE hl_control.tasks SET
    stage_results=stage_results||jsonb_build_object(p_stage,
       jsonb_build_object('role_agent_id',p_role_agent_id,
                          'result',coalesce(p_result,'{}'::jsonb))),
    current_stage=CASE WHEN p_complete THEN NULL ELSE p_next_stage END,
    status=CASE WHEN p_complete THEN 'completed' ELSE 'leased' END,
    completed_at=CASE WHEN p_complete THEN clock_timestamp() ELSE completed_at END
  WHERE task_id=p_task_id RETURNING * INTO t;
  UPDATE hl_control.agents SET last_heartbeat=clock_timestamp()
  WHERE agent_id=p_role_agent_id;
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES (CASE WHEN p_complete THEN 'task_completed' ELSE 'role_stage_completed' END,
          t.task_id,p_role_agent_id,t.project_id,
          jsonb_build_object('stage',p_stage,'lease_owner',p_lease_owner_id,
                             'next_stage',p_next_stage,'complete',p_complete));
  RETURN t;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.renew_task_lease(
  p_task_id text,p_agent_id text,p_lease_seconds integer DEFAULT 300
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks;
BEGIN
  UPDATE hl_control.tasks
  SET lease_expires_at=clock_timestamp()+make_interval(secs=>greatest(p_lease_seconds,1))
  WHERE task_id=p_task_id AND status='leased' AND lease_owner=p_agent_id
    AND coalesce(payload->>'fencing_required','false')<>'true'
    AND (lease_expires_at IS NULL OR lease_expires_at>clock_timestamp())
  RETURNING * INTO t;
  IF t.task_id IS NULL THEN RAISE EXCEPTION 'legacy_renew_denied'; END IF;
  INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
  VALUES ('lease_renewed',t.task_id,p_agent_id,t.project_id,
          jsonb_build_object('lease_expires_at',t.lease_expires_at));
  RETURN t;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.fail_task(
  p_task_id text,p_agent_id text,p_reason text,p_snapshot jsonb DEFAULT '{}'::jsonb
) RETURNS hl_control.tasks
LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE t hl_control.tasks; next_attempts integer;
BEGIN
  SELECT * INTO t FROM hl_control.tasks WHERE task_id=p_task_id FOR UPDATE;
  IF t.task_id IS NULL THEN RAISE EXCEPTION 'task_not_found'; END IF;
  IF t.payload->>'fencing_required'='true' THEN
    RAISE EXCEPTION 'fenced_task_requires_token';
  END IF;
  IF t.status<>'leased' OR t.lease_owner IS DISTINCT FROM p_agent_id THEN
    RAISE EXCEPTION 'task_not_leased_by_agent';
  END IF;
  next_attempts:=t.attempts+1;
  IF next_attempts>=t.max_attempts THEN
    UPDATE hl_control.tasks SET status='dead_letter',attempts=next_attempts,
      lease_owner=NULL,lease_expires_at=NULL
    WHERE task_id=p_task_id RETURNING * INTO t;
    INSERT INTO hl_control.dead_letters(task_id,project_id,reason,snapshot)
    VALUES (t.task_id,t.project_id,p_reason,coalesce(p_snapshot,'{}'::jsonb));
    INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
    VALUES ('task_dead_lettered',t.task_id,p_agent_id,t.project_id,
            jsonb_build_object('reason',p_reason,'attempts',next_attempts));
  ELSE
    UPDATE hl_control.tasks SET status='queued',attempts=next_attempts,
      lease_owner=NULL,lease_expires_at=NULL
    WHERE task_id=p_task_id RETURNING * INTO t;
    INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
    VALUES ('task_requeued',t.task_id,p_agent_id,t.project_id,
            jsonb_build_object('reason',p_reason,'attempts',next_attempts));
  END IF;
  RETURN t;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.release_expired_leases()
RETURNS integer LANGUAGE plpgsql SECURITY INVOKER SET search_path TO ''
AS $fn$
DECLARE r record; processed integer:=0; next_attempts integer;
BEGIN
  FOR r IN SELECT * FROM hl_control.tasks
    WHERE status='leased'
      AND coalesce(payload->>'fencing_required','false')<>'true'
      AND lease_expires_at IS NOT NULL AND lease_expires_at<clock_timestamp()
    FOR UPDATE SKIP LOCKED
  LOOP
    next_attempts:=r.attempts+1;
    IF next_attempts>=r.max_attempts THEN
      UPDATE hl_control.tasks SET status='dead_letter',attempts=next_attempts,
          lease_owner=NULL,lease_expires_at=NULL
      WHERE task_id=r.task_id;
      INSERT INTO hl_control.dead_letters(task_id,project_id,reason,snapshot)
      VALUES (r.task_id,r.project_id,'lease_expired',
              jsonb_build_object('previous_owner',r.lease_owner,'expired_at',r.lease_expires_at));
      INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
      VALUES ('lease_expired_dead_letter',r.task_id,r.lease_owner,r.project_id,
              jsonb_build_object('attempts',next_attempts));
    ELSE
      UPDATE hl_control.tasks SET status='queued',attempts=next_attempts,
          lease_owner=NULL,lease_expires_at=NULL
      WHERE task_id=r.task_id;
      INSERT INTO hl_control.events(event_type,task_id,agent_id,project_id,payload)
      VALUES ('lease_expired_requeued',r.task_id,r.lease_owner,r.project_id,
              jsonb_build_object('attempts',next_attempts));
    END IF;
    processed:=processed+1;
  END LOOP;
  RETURN processed;
END $fn$;

-- The schema remains PRIVATE: no new open Data API/RPC surface. These
-- functions have no EXECUTE grant to PUBLIC/anon/authenticated/service_role.
-- A future reviewed, least-privileged backend identity must be explicitly
-- provisioned/granted, after staging acceptance and production cutover review.
REVOKE ALL ON FUNCTION hl_control.claim_fenced_task_v1(text,text,text,integer) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.advance_fenced_stage_v1(text,text,bigint,uuid,text,jsonb,text,boolean) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.renew_fenced_lease_v1(text,text,bigint,uuid,integer) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.fail_fenced_task_v1(text,text,bigint,uuid,text) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.expire_fenced_task_v1(text) FROM PUBLIC;
-- Legacy functions may predate this migration with private ACLs in Supabase,
-- but a fresh staging fixture creates them with PostgreSQL's PUBLIC default.
-- Explicitly preserve a deny-by-default RPC boundary in both environments.
REVOKE ALL ON FUNCTION hl_control.claim_next_task(text,integer) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.advance_task_stage(text,text,text,jsonb,text,boolean) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.advance_task_stage_v2(text,text,text,text,jsonb,text,boolean) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.renew_task_lease(text,text,integer) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.fail_task(text,text,text,jsonb) FROM PUBLIC;
REVOKE ALL ON FUNCTION hl_control.release_expired_leases() FROM PUBLIC;
COMMIT;
