-- G3 executor identity bridge: REVIEW-ONLY, not applied to production.
-- Invoke after hl_control_fenced_tasks_candidate_v1.sql, only after role audit.
-- The ONLY principal eligible for these wrappers is a dedicated PostgreSQL
-- login whose SESSION_USER is mapped by the administrator. No passwords,
-- login roles or grants are created here.
--
-- SECURITY DEFINER is an explicit exception for tightly scoped, privately
-- located methods. Public RPC access remains denied, and all access is
-- constrained by a server-owned session identity -> agent/project binding.
BEGIN;

CREATE TABLE IF NOT EXISTS hl_control.fenced_executor_bindings (
  db_session_role text PRIMARY KEY,
  agent_id text NOT NULL REFERENCES hl_control.agents(agent_id),
  project_id text NOT NULL,
  enabled boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
REVOKE ALL ON hl_control.fenced_executor_bindings FROM PUBLIC, anon, authenticated, service_role;

CREATE OR REPLACE FUNCTION hl_control.fenced_bound_identity_v1()
RETURNS TABLE (agent_id text, project_id text)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO ''
AS $fn$
BEGIN
  IF session_user IN ('postgres','anon','authenticated','service_role','supabase_admin')
     OR session_user LIKE 'pg_%' THEN
    RAISE EXCEPTION 'fenced_executor_unbound';
  END IF;
  RETURN QUERY
    SELECT b.agent_id, b.project_id
    FROM hl_control.fenced_executor_bindings b
    JOIN hl_control.agents a ON a.agent_id=b.agent_id
    WHERE b.db_session_role=session_user::text
      AND b.enabled=true
      AND a.status='active'
      AND (a.expires_at IS NULL OR a.expires_at>clock_timestamp())
      AND a.permissions @> '["tier0"]'::jsonb;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'fenced_executor_unbound';
  END IF;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.fenced_executor_claim_v1(
  p_task_id text,p_operation_key text,p_lease_seconds integer DEFAULT 60
) RETURNS TABLE(task_id text, lease_epoch bigint, lease_token uuid,
                stage_name text, expires_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO ''
AS $fn$
DECLARE bound_agent text; allowed_project text; t hl_control.tasks;
BEGIN
  SELECT i.agent_id, i.project_id INTO STRICT bound_agent,allowed_project
  FROM hl_control.fenced_bound_identity_v1() i;
  IF NOT EXISTS(
    SELECT 1 FROM hl_control.tasks task WHERE task.task_id=p_task_id
      AND task.project_id=allowed_project
  ) THEN
    RAISE EXCEPTION 'fenced_executor_task_out_of_scope';
  END IF;
  t:=hl_control.claim_fenced_task_v1(
    p_task_id,bound_agent,p_operation_key,p_lease_seconds
  );
  RETURN QUERY SELECT t.task_id,t.fenced_epoch,t.fenced_token,
                      t.current_stage,t.lease_expires_at;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.fenced_executor_advance_v1(
  p_task_id text,p_lease_epoch bigint,p_lease_token uuid,
  p_stage text,p_result jsonb,p_next_stage text DEFAULT NULL,
  p_complete boolean DEFAULT false
) RETURNS TABLE(task_id text,status text,stage_name text,
                completed_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO ''
AS $fn$
DECLARE bound_agent text; allowed_project text; t hl_control.tasks;
BEGIN
  SELECT i.agent_id,i.project_id INTO STRICT bound_agent,allowed_project
    FROM hl_control.fenced_bound_identity_v1() i;
  IF NOT EXISTS (
    SELECT 1 FROM hl_control.tasks task
    WHERE task.task_id=p_task_id AND task.project_id=allowed_project
  ) THEN RAISE EXCEPTION 'fenced_executor_task_out_of_scope'; END IF;
  t:=hl_control.advance_fenced_stage_v1(
    p_task_id,bound_agent,p_lease_epoch,p_lease_token,
    p_stage,p_result,p_next_stage,p_complete
  );
  RETURN QUERY SELECT t.task_id,t.status,t.current_stage,t.completed_at;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.fenced_executor_renew_v1(
  p_task_id text,p_lease_epoch bigint,p_lease_token uuid,
  p_lease_seconds integer DEFAULT 60
) RETURNS TABLE(task_id text,lease_epoch bigint,expires_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO ''
AS $fn$
DECLARE bound_agent text; allowed_project text; t hl_control.tasks;
BEGIN
  SELECT i.agent_id,i.project_id INTO STRICT bound_agent,allowed_project
    FROM hl_control.fenced_bound_identity_v1() i;
  IF NOT EXISTS(
    SELECT 1 FROM hl_control.tasks task
    WHERE task.task_id=p_task_id AND task.project_id=allowed_project
  ) THEN RAISE EXCEPTION 'fenced_executor_task_out_of_scope'; END IF;
  t:=hl_control.renew_fenced_lease_v1(
    p_task_id,bound_agent,p_lease_epoch,p_lease_token,p_lease_seconds
  );
  RETURN QUERY SELECT t.task_id,t.fenced_epoch,t.lease_expires_at;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.fenced_executor_abort_v1(
  p_task_id text,p_lease_epoch bigint,p_lease_token uuid,p_reason text
) RETURNS TABLE(task_id text,status text)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO ''
AS $fn$
DECLARE bound_agent text; allowed_project text; t hl_control.tasks;
BEGIN
  SELECT i.agent_id,i.project_id INTO STRICT bound_agent,allowed_project
    FROM hl_control.fenced_bound_identity_v1() i;
  IF NOT EXISTS(
    SELECT 1 FROM hl_control.tasks task
    WHERE task.task_id=p_task_id AND task.project_id=allowed_project
  ) THEN RAISE EXCEPTION 'fenced_executor_task_out_of_scope'; END IF;
  t:=hl_control.fail_fenced_task_v1(
    p_task_id,bound_agent,p_lease_epoch,p_lease_token,p_reason
  );
  RETURN QUERY SELECT t.task_id,t.status;
END $fn$;

-- Do not automatically create, log in, or grant the executor role. A future
-- audited operator must provision a dedicated role and grant ONLY schema
-- USAGE and EXECUTE on exactly four wrapper methods, never direct table DML
-- or EXECUTE on base functions. This migration is not a deployment approval.
REVOKE ALL ON FUNCTION hl_control.fenced_bound_identity_v1() FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_claim_v1(text,text,integer) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_advance_v1(text,bigint,uuid,text,jsonb,text,boolean) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_renew_v1(text,bigint,uuid,integer) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_abort_v1(text,bigint,uuid,text) FROM PUBLIC,anon,authenticated,service_role;
COMMIT;
