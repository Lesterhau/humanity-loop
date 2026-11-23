-- Test-only role grant fixture for ephemeral postgres: NEVER apply to production.
-- Bind two distinct DB session identities; none can UPDATE/SELECT private tables.
CREATE ROLE hl_test_executor_a NOLOGIN NOINHERIT;
CREATE ROLE hl_test_executor_b NOLOGIN NOINHERIT;
CREATE ROLE hl_test_executor_unbound NOLOGIN NOINHERIT;
GRANT USAGE ON SCHEMA hl_control TO hl_test_executor_a,hl_test_executor_b,hl_test_executor_unbound;
GRANT EXECUTE ON FUNCTION hl_control.fenced_executor_claim_v1(text,text,integer)
 TO hl_test_executor_a,hl_test_executor_b,hl_test_executor_unbound;
GRANT EXECUTE ON FUNCTION hl_control.fenced_executor_advance_v1(text,bigint,uuid,text,jsonb,text,boolean)
 TO hl_test_executor_a,hl_test_executor_b;
GRANT EXECUTE ON FUNCTION hl_control.fenced_executor_renew_v1(text,bigint,uuid,integer)
 TO hl_test_executor_a,hl_test_executor_b;
GRANT EXECUTE ON FUNCTION hl_control.fenced_executor_abort_v1(text,bigint,uuid,text)
 TO hl_test_executor_a,hl_test_executor_b;

INSERT INTO hl_control.fenced_executor_bindings(db_session_role,agent_id,project_id,enabled)
VALUES ('hl_test_executor_a','fenced_worker_a','humanity-loop',true),
       ('hl_test_executor_b','fenced_worker_b','other-project',true);
INSERT INTO hl_control.tasks(task_id,project_id,payload,risk_tier,status,
                             stages,current_stage,max_attempts,priority)
VALUES ('fenced_role_task_a','humanity-loop',
 '{"fencing_required":"true","idempotency_key":"role-a-operation-key-2026",
   "execution_mode":"deterministic_only","external_actions":false,
   "model_calls":0,"max_provider_credits":0}'::jsonb,
 0,'held','["scout","outcome"]','scout',3,5),
 ('fenced_role_task_other_project','other-project',
 '{"fencing_required":"true","idempotency_key":"role-b-operation-key-2026",
   "execution_mode":"deterministic_only","external_actions":false,
   "model_calls":0,"max_provider_credits":0}'::jsonb,
 0,'held','["scout","outcome"]','scout',3,5);

-- Role ACL: no schema data access, no base mutation method, no authentication
-- by agent_id alone; ONLY the small SECDEF wrapper is executable.
SELECT public.assert_true(
 NOT has_table_privilege('hl_test_executor_a','hl_control.tasks','SELECT')
 AND NOT has_table_privilege('hl_test_executor_a','hl_control.tasks','UPDATE')
 AND NOT has_table_privilege('hl_test_executor_a','hl_control.tasks','INSERT')
 AND NOT has_table_privilege('hl_test_executor_a','hl_control.events','SELECT')
 AND NOT has_table_privilege('hl_test_executor_a','hl_control.fenced_executor_bindings','SELECT'),
 'executor_must_have_zero_direct_canonical_table_permissions');
SELECT public.assert_true(
 NOT has_function_privilege('hl_test_executor_a',
   'hl_control.claim_fenced_task_v1(text,text,text,integer)','EXECUTE')
 AND NOT has_function_privilege('hl_test_executor_a',
   'hl_control.claim_next_task(text,integer)','EXECUTE'),
 'executor_must_not_call_base_lease_or_legacy_claim');
SELECT public.assert_true(
 has_function_privilege('hl_test_executor_a',
  'hl_control.fenced_executor_claim_v1(text,text,integer)','EXECUTE')
 AND NOT has_function_privilege('anon',
  'hl_control.fenced_executor_claim_v1(text,text,integer)','EXECUTE')
 AND NOT has_function_privilege('authenticated',
  'hl_control.fenced_executor_claim_v1(text,text,integer)','EXECUTE')
 AND NOT has_function_privilege('service_role',
  'hl_control.fenced_executor_claim_v1(text,text,integer)','EXECUTE'),
 'executor_only_private_rpc_grants');

-- Switch the SQL SESSION principal (not merely SET ROLE), so SECURITY
-- DEFINER must enforce the true database-login identity via SESSION_USER.
SET SESSION AUTHORIZATION hl_test_executor_a;
DO $test$
DECLARE l record; advanced record; finished record;
BEGIN
  IF session_user IS DISTINCT FROM 'hl_test_executor_a' THEN
    RAISE EXCEPTION 'ASSERTION_FAILED: wrong session user %', session_user;
  END IF;
  -- The role cannot read direct data despite schema USAGE.
  BEGIN
    PERFORM 1 FROM hl_control.tasks LIMIT 1;
    RAISE EXCEPTION 'ASSERTION_FAILED: task SELECT became available';
  EXCEPTION WHEN insufficient_privilege THEN NULL;
  END;
  BEGIN
    PERFORM hl_control.claim_fenced_task_v1(
      'fenced_role_task_a','fenced_worker_a','role-a-operation-key-2026',60);
    RAISE EXCEPTION 'ASSERTION_FAILED: base claim permitted';
  EXCEPTION WHEN insufficient_privilege THEN NULL;
  END;
  -- Correct principal can safely claim only its bound project and task.
  SELECT * INTO l FROM hl_control.fenced_executor_claim_v1(
      'fenced_role_task_a','role-a-operation-key-2026',60);
  IF l.task_id <> 'fenced_role_task_a' OR l.lease_epoch<>1 OR l.lease_token IS NULL THEN
    RAISE EXCEPTION 'ASSERTION_FAILED: bound lease claims missing';
  END IF;
  BEGIN
    PERFORM * FROM hl_control.fenced_executor_advance_v1(
      l.task_id,l.lease_epoch,gen_random_uuid(),
      'scout','{}'::jsonb,'outcome',false);
    RAISE EXCEPTION 'ASSERTION_FAILED: wrong fence token accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
  END;
  SELECT * INTO advanced FROM hl_control.fenced_executor_advance_v1(
      l.task_id,l.lease_epoch,l.lease_token,'scout',
      '{"draft":"manual review required"}'::jsonb,'outcome',false);
  IF advanced.status<>'leased' OR advanced.stage_name<>'outcome' THEN
    RAISE EXCEPTION 'ASSERTION_FAILED: bounded stage did not advance';
  END IF;
  SELECT * INTO finished FROM hl_control.fenced_executor_advance_v1(
      l.task_id,l.lease_epoch,l.lease_token,'outcome',
      '{"human_review_required":true,"outside_action":false}'::jsonb,NULL,true);
  IF finished.status<>'completed' OR finished.completed_at IS NULL THEN
    RAISE EXCEPTION 'ASSERTION_FAILED: scoped completion was not committed';
  END IF;
END $test$;
RESET SESSION AUTHORIZATION;

-- Even if an authorized role can invoke the wrapper, it cannot claim another
-- project, impersonate another worker via p_agent_id (there is no such input),
-- or select the private identity mapping.
SET SESSION AUTHORIZATION hl_test_executor_b;
DO $test$
BEGIN
  BEGIN
    PERFORM * FROM hl_control.fenced_executor_claim_v1(
      'fenced_role_task_a','role-a-operation-key-2026',60);
    RAISE EXCEPTION 'ASSERTION_FAILED: cross-project claim accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_executor_task_out_of_scope%' THEN RAISE; END IF;
  END;
  BEGIN
    PERFORM 1 FROM hl_control.fenced_executor_bindings;
    RAISE EXCEPTION 'ASSERTION_FAILED: executor mapping readable';
  EXCEPTION WHEN insufficient_privilege THEN NULL;
  END;
  -- Its own project and agent mapping can work without table UPDATE privilege.
  PERFORM * FROM hl_control.fenced_executor_claim_v1(
    'fenced_role_task_other_project','role-b-operation-key-2026',60);
END $test$;
RESET SESSION AUTHORIZATION;

SET SESSION AUTHORIZATION hl_test_executor_unbound;
DO $test$
BEGIN
  BEGIN
    PERFORM * FROM hl_control.fenced_executor_claim_v1(
      'fenced_role_task_a','role-a-operation-key-2026',60);
    RAISE EXCEPTION 'ASSERTION_FAILED: unbound executor succeeded';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_executor_unbound%' THEN RAISE; END IF;
  END;
END $test$;
RESET SESSION AUTHORIZATION;

-- Real hosted cutover still needs secure actual login provisioning and runtime
-- identity confirmation; NO such credential or production permission is made.
SELECT public.assert_true(
  (SELECT status='completed' AND fenced_token IS NULL
   FROM hl_control.tasks WHERE task_id='fenced_role_task_a'),
 'bound executor test completed and revoked lease token'
);
SELECT 'RESTRICTED_SESSION_EXECUTOR_ACCEPTANCE_PASSED' AS result;
