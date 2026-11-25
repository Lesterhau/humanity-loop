-- G3 executor identity bridge: REVIEW-ONLY, not applied to production.
-- Invoke after hl_control_fenced_tasks_candidate_v1.sql, only after role audit.
-- The ONLY principal eligible for these wrappers is a dedicated PostgreSQL
-- login whose SESSION_USER is mapped by the administrator. No passwords,
-- login roles or executor grants are created here.
--
-- The wrappers are owned by hl_fenced_definer, a NOLOGIN role created below
-- that holds only the rights the four wrappers need. A defect in a wrapper is
-- then bounded by that role's privileges, not by the migration owner's.
-- Requires PostgreSQL 16 or later (GRANT ... WITH SET).
--
-- SECURITY DEFINER is an explicit exception for tightly scoped, privately
-- located methods. Public RPC access remains denied, and all access is
-- constrained by a server-owned session identity -> agent/project binding.
BEGIN;
SET LOCAL search_path TO pg_catalog, pg_temp;

DO $role$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'hl_fenced_definer') THEN
    CREATE ROLE hl_fenced_definer NOLOGIN NOINHERIT NOSUPERUSER NOCREATEDB
      NOCREATEROLE NOREPLICATION NOBYPASSRLS;
  END IF;
  -- Fail closed on a pre-existing role that is broader than intended.
  IF EXISTS (
       SELECT 1 FROM pg_catalog.pg_roles r
       WHERE r.rolname = 'hl_fenced_definer'
         AND (r.rolcanlogin OR r.rolsuper OR r.rolbypassrls OR r.rolcreaterole
              OR r.rolcreatedb OR r.rolreplication OR r.rolinherit))
     OR EXISTS (
       SELECT 1 FROM pg_catalog.pg_auth_members m
       JOIN pg_catalog.pg_roles r ON r.oid = m.member
       WHERE r.rolname = 'hl_fenced_definer')
  THEN
    RAISE EXCEPTION 'fenced_definer_role_unsafe';
  END IF;
END $role$;

CREATE TABLE IF NOT EXISTS hl_control.fenced_executor_bindings (
  db_session_role text PRIMARY KEY,
  agent_id text NOT NULL REFERENCES hl_control.agents(agent_id),
  project_id text NOT NULL,
  enabled boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
ALTER TABLE hl_control.fenced_executor_bindings ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON hl_control.fenced_executor_bindings FROM PUBLIC, anon, authenticated, service_role;

-- Exact rights of the wrapper owner. Nothing here lets it change a task's
-- payload, project, tier or approval flags, read the audit tables, delete
-- rows, or touch a task that is not fenced.
GRANT USAGE ON SCHEMA hl_control TO hl_fenced_definer;
GRANT SELECT ON hl_control.fenced_executor_bindings, hl_control.tasks TO hl_fenced_definer;
GRANT SELECT (agent_id, status, permissions, expires_at) ON hl_control.agents TO hl_fenced_definer;
GRANT UPDATE (status, lease_owner, lease_expires_at, fenced_epoch, fenced_token,
              stage_results, current_stage, completed_at, attempts, updated_at)
  ON hl_control.tasks TO hl_fenced_definer;
GRANT INSERT ON hl_control.events, hl_control.dead_letters TO hl_fenced_definer;

-- serial (not identity) key columns need sequence USAGE for INSERT.
DO $seq$
DECLARE s pg_catalog.text;
BEGIN
  FOR s IN
    SELECT pg_catalog.pg_get_serial_sequence(
             pg_catalog.format('%I.%I', n.nspname, c.relname), a.attname)
    FROM pg_catalog.pg_attribute a
    JOIN pg_catalog.pg_class c ON c.oid = a.attrelid
    JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'hl_control' AND c.relname IN ('events', 'dead_letters')
      AND a.attnum > 0 AND NOT a.attisdropped AND a.attidentity = ''
  LOOP
    IF s IS NOT NULL THEN
      EXECUTE pg_catalog.format('GRANT USAGE ON SEQUENCE %s TO hl_fenced_definer', s);
    END IF;
  END LOOP;
END $seq$;

-- Row level security is enabled on every table above, so the non-owner wrapper
-- role sees and writes only what these policies allow.
DROP POLICY IF EXISTS hl_fenced_definer_read ON hl_control.fenced_executor_bindings;
CREATE POLICY hl_fenced_definer_read ON hl_control.fenced_executor_bindings
  FOR SELECT TO hl_fenced_definer USING (true);
DROP POLICY IF EXISTS hl_fenced_definer_read ON hl_control.agents;
CREATE POLICY hl_fenced_definer_read ON hl_control.agents
  FOR SELECT TO hl_fenced_definer USING (true);
DROP POLICY IF EXISTS hl_fenced_definer_read ON hl_control.tasks;
CREATE POLICY hl_fenced_definer_read ON hl_control.tasks
  FOR SELECT TO hl_fenced_definer USING (payload->>'fencing_required' = 'true');
DROP POLICY IF EXISTS hl_fenced_definer_write ON hl_control.tasks;
CREATE POLICY hl_fenced_definer_write ON hl_control.tasks
  FOR UPDATE TO hl_fenced_definer
  USING (payload->>'fencing_required' = 'true')
  WITH CHECK (payload->>'fencing_required' = 'true');
DROP POLICY IF EXISTS hl_fenced_definer_append ON hl_control.events;
CREATE POLICY hl_fenced_definer_append ON hl_control.events
  FOR INSERT TO hl_fenced_definer
  WITH CHECK (event_type IN ('fenced_task_claimed', 'fenced_stage_advanced',
                             'fenced_task_completed', 'fenced_lease_renewed',
                             'fenced_task_dead_letter'));
DROP POLICY IF EXISTS hl_fenced_definer_append ON hl_control.dead_letters;
CREATE POLICY hl_fenced_definer_append ON hl_control.dead_letters
  FOR INSERT TO hl_fenced_definer
  WITH CHECK (reason IN ('verifier_hold', 'safety_hold', 'deadline_exhausted',
                         'model_error', 'operator_abort'));

-- The wrappers are created by their owner, so no privileged ownership transfer
-- is needed. CREATE on the schema and the ability to assume the role exist
-- only inside this transaction.
GRANT hl_fenced_definer TO CURRENT_USER WITH SET TRUE, INHERIT FALSE;
GRANT CREATE ON SCHEMA hl_control TO hl_fenced_definer;

-- Upgrade in place: wrappers left by an earlier candidate change owner first.
DO $own$
DECLARE f pg_catalog.regprocedure;
BEGIN
  FOR f IN
    SELECT p.oid::pg_catalog.regprocedure
    FROM pg_catalog.pg_proc p
    JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace
    JOIN pg_catalog.pg_roles o ON o.oid = p.proowner
    WHERE n.nspname = 'hl_control'
      AND p.proname IN ('fenced_bound_identity_v1', 'fenced_executor_claim_v1',
                        'fenced_executor_advance_v1', 'fenced_executor_renew_v1',
                        'fenced_executor_abort_v1')
      AND o.rolname <> 'hl_fenced_definer'
  LOOP
    EXECUTE pg_catalog.format('ALTER FUNCTION %s OWNER TO hl_fenced_definer', f);
  END LOOP;
END $own$;

SET LOCAL ROLE hl_fenced_definer;

CREATE OR REPLACE FUNCTION hl_control.fenced_bound_identity_v1()
RETURNS TABLE (agent_id pg_catalog.text, project_id pg_catalog.text)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO pg_catalog, pg_temp
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
    WHERE b.db_session_role=session_user::pg_catalog.text
      AND b.enabled=true
      AND a.status='active'
      AND (a.expires_at IS NULL OR a.expires_at>clock_timestamp())
      AND a.permissions @> '["tier0"]'::pg_catalog.jsonb;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'fenced_executor_unbound';
  END IF;
END $fn$;

CREATE OR REPLACE FUNCTION hl_control.fenced_executor_claim_v1(
  p_task_id pg_catalog.text,p_operation_key pg_catalog.text,p_lease_seconds integer DEFAULT 60
) RETURNS TABLE(task_id pg_catalog.text, lease_epoch bigint, lease_token uuid,
                stage_name pg_catalog.text, expires_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO pg_catalog, pg_temp
AS $fn$
DECLARE bound_agent pg_catalog.text; allowed_project pg_catalog.text; t hl_control.tasks;
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
  p_task_id pg_catalog.text,p_lease_epoch bigint,p_lease_token uuid,
  p_stage pg_catalog.text,p_result pg_catalog.jsonb,p_next_stage pg_catalog.text DEFAULT NULL,
  p_complete boolean DEFAULT false
) RETURNS TABLE(task_id pg_catalog.text,status pg_catalog.text,stage_name pg_catalog.text,
                completed_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO pg_catalog, pg_temp
AS $fn$
DECLARE bound_agent pg_catalog.text; allowed_project pg_catalog.text; t hl_control.tasks;
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
  p_task_id pg_catalog.text,p_lease_epoch bigint,p_lease_token uuid,
  p_lease_seconds integer DEFAULT 60
) RETURNS TABLE(task_id pg_catalog.text,lease_epoch bigint,expires_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO pg_catalog, pg_temp
AS $fn$
DECLARE bound_agent pg_catalog.text; allowed_project pg_catalog.text; t hl_control.tasks;
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
  p_task_id pg_catalog.text,p_lease_epoch bigint,p_lease_token uuid,p_reason pg_catalog.text
) RETURNS TABLE(task_id pg_catalog.text,status pg_catalog.text)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO pg_catalog, pg_temp
AS $fn$
DECLARE bound_agent pg_catalog.text; allowed_project pg_catalog.text; t hl_control.tasks;
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
-- or EXECUTE on base functions. Those EXECUTE grants are issued as the wrapper
-- owner (SET ROLE hl_fenced_definer) or by a superuser. This migration is not
-- a deployment approval.
REVOKE ALL ON FUNCTION hl_control.fenced_bound_identity_v1() FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_claim_v1(pg_catalog.text,pg_catalog.text,integer) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_advance_v1(pg_catalog.text,bigint,uuid,pg_catalog.text,pg_catalog.jsonb,pg_catalog.text,boolean) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_renew_v1(pg_catalog.text,bigint,uuid,integer) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_control.fenced_executor_abort_v1(pg_catalog.text,bigint,uuid,pg_catalog.text) FROM PUBLIC,anon,authenticated,service_role;
RESET ROLE;

-- Close the creation window: the owner keeps USAGE only, and nobody keeps the
-- ability to assume it.
REVOKE CREATE ON SCHEMA hl_control FROM hl_fenced_definer;
REVOKE hl_fenced_definer FROM CURRENT_USER;

-- The wrappers call exactly these four token-checked base functions.
GRANT EXECUTE ON FUNCTION hl_control.claim_fenced_task_v1(pg_catalog.text,pg_catalog.text,pg_catalog.text,integer) TO hl_fenced_definer;
GRANT EXECUTE ON FUNCTION hl_control.advance_fenced_stage_v1(pg_catalog.text,pg_catalog.text,bigint,uuid,pg_catalog.text,pg_catalog.jsonb,pg_catalog.text,boolean) TO hl_fenced_definer;
GRANT EXECUTE ON FUNCTION hl_control.renew_fenced_lease_v1(pg_catalog.text,pg_catalog.text,bigint,uuid,integer) TO hl_fenced_definer;
GRANT EXECUTE ON FUNCTION hl_control.fail_fenced_task_v1(pg_catalog.text,pg_catalog.text,bigint,uuid,pg_catalog.text) TO hl_fenced_definer;
COMMIT;
