#!/usr/bin/env bash
# Disposable GitHub Actions PostgreSQL ONLY. No hosted Supabase login, secrets,
# networked AI, paid provider, external case, or persistent service identity.
set -euo pipefail
set +x

: "$PGPASSWORD"
admin_password="$PGPASSWORD"
password_a="$(openssl rand -hex 24)"
password_b="$(openssl rand -hex 24)"
password_unbound="$(openssl rand -hex 24)"

# Roles exist as NOLOGIN from the separate privilege test. Give them genuine
# password-authenticated LOGIN exclusively in this ephemeral CI database.
# psql quoted variables prevent SQL injection; passwords are never echoed.
PGUSER=postgres PGPASSWORD="$admin_password" psql -X -q -v ON_ERROR_STOP=1 \
  -v pass_a="$password_a" -v pass_b="$password_b" -v pass_unbound="$password_unbound" <<'SQL'
ALTER ROLE hl_test_executor_a LOGIN PASSWORD :'pass_a';
ALTER ROLE hl_test_executor_b LOGIN PASSWORD :'pass_b';
ALTER ROLE hl_test_executor_unbound LOGIN PASSWORD :'pass_unbound';

INSERT INTO hl_control.tasks
  (task_id,project_id,payload,risk_tier,status,stages,current_stage,max_attempts)
VALUES
 ('fenced_password_login_a','humanity-loop',
  '{"fencing_required":"true","idempotency_key":"login-a-20261123-task-key",
    "execution_mode":"deterministic_only","external_actions":false,
    "model_calls":0,"max_provider_credits":0}'::jsonb,
  0,'held','["scout","outcome"]','scout',3),
 ('fenced_password_login_b','other-project',
  '{"fencing_required":"true","idempotency_key":"login-b-20261123-task-key",
    "execution_mode":"deterministic_only","external_actions":false,
    "model_calls":0,"max_provider_credits":0}'::jsonb,
  0,'held','["scout","outcome"]','scout',3),
 ('fenced_password_paid_a','humanity-loop',
  '{"fencing_required":"true","idempotency_key":"login-paid-20261123-key",
    "execution_mode":"deterministic_only","external_actions":false,
    "model_calls":1,"max_provider_credits":0}'::jsonb,
  0,'held','["scout","outcome"]','scout',3);
SQL

# Failed password and role elevation MUST fail. Authentication is via TCP,
# not SET SESSION AUTHORIZATION executed by the privileged fixture creator.
if PGUSER=hl_test_executor_a PGPASSWORD=definitely_invalid_test_password \
   psql -X -Atqc 'select 1' >/dev/null 2>&1; then
  echo "FAIL: executor accepted an incorrect password" >&2
  exit 1
fi

if PGUSER=hl_test_executor_a PGPASSWORD="$password_a" \
   psql -X -v ON_ERROR_STOP=1 -Atqc 'SET ROLE postgres' >/dev/null 2>&1; then
  echo "FAIL: low-privilege executor elevated to postgres" >&2
  exit 1
fi
if PGUSER=hl_test_executor_a PGPASSWORD="$password_a" \
   psql -X -v ON_ERROR_STOP=1 -Atqc 'SET ROLE hl_test_executor_b' >/dev/null 2>&1; then
  echo "FAIL: executor assumed a different project identity" >&2
  exit 1
fi

# An actual LOGIN may not change the immutable session principal either.
if PGUSER=hl_test_executor_a PGPASSWORD="$password_a" \
   psql -X -v ON_ERROR_STOP=1 -Atqc 'SET SESSION AUTHORIZATION hl_test_executor_b' >/dev/null 2>&1; then
  echo "FAIL: executor switched session authorization to a different worker" >&2
  exit 1
fi

# Genuine authenticated connection as the only bound A principal. The session
# cannot SELECT or UPDATE private task data, cannot call underlying functions,
# cannot claim B's project, cannot call any paid-model task, but can complete
# the scoped zero-model work with the current fenced epoch and UUID.
PGUSER=hl_test_executor_a PGPASSWORD="$password_a" psql -X -q -v ON_ERROR_STOP=1 <<'SQL'
DO $login$
DECLARE lease record; next_step record; final_step record;
BEGIN
 IF session_user IS DISTINCT FROM 'hl_test_executor_a'
     OR current_user IS DISTINCT FROM 'hl_test_executor_a' THEN
   RAISE EXCEPTION 'real_login_identity_not_established';
 END IF;
 IF has_table_privilege(session_user,'hl_control.tasks','SELECT')
     OR has_table_privilege(session_user,'hl_control.tasks','UPDATE')
     OR has_table_privilege(session_user,'hl_control.fenced_executor_bindings','SELECT') THEN
   RAISE EXCEPTION 'executor_has_direct_private_table_privileges';
 END IF;
 BEGIN
   PERFORM 1 FROM hl_control.tasks LIMIT 1;
   RAISE EXCEPTION 'unexpected_private_table_read';
 EXCEPTION WHEN insufficient_privilege THEN NULL;
 END;
 BEGIN
   PERFORM * FROM hl_control.fenced_executor_claim_v1(
     'fenced_password_login_b','login-b-20261123-task-key',60);
   RAISE EXCEPTION 'cross_project_claim_accepted';
 EXCEPTION WHEN OTHERS THEN
   IF SQLERRM NOT LIKE '%fenced_executor_task_out_of_scope%' THEN RAISE; END IF;
 END;
 BEGIN
   PERFORM * FROM hl_control.fenced_executor_claim_v1(
     'fenced_password_paid_a','login-paid-20261123-key',60);
   RAISE EXCEPTION 'paid_model_claim_accepted';
 EXCEPTION WHEN OTHERS THEN
   IF SQLERRM NOT LIKE '%fenced_task_unavailable_or_already_leased%' THEN RAISE; END IF;
 END;
 SELECT * INTO lease FROM hl_control.fenced_executor_claim_v1(
   'fenced_password_login_a','login-a-20261123-task-key',60);
 IF lease.task_id <> 'fenced_password_login_a'
     OR lease.lease_epoch <> 1 OR lease.lease_token IS NULL THEN
   RAISE EXCEPTION 'authenticated_claim_failed';
 END IF;
 BEGIN
   PERFORM * FROM hl_control.fenced_executor_advance_v1(
     lease.task_id,lease.lease_epoch,gen_random_uuid(),
     'scout','{"verified":false}'::jsonb,'outcome',false);
   RAISE EXCEPTION 'wrong_token_was_accepted';
 EXCEPTION WHEN OTHERS THEN
   IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
 END;
 SELECT * INTO next_step FROM hl_control.fenced_executor_advance_v1(
   lease.task_id,lease.lease_epoch,lease.lease_token,
   'scout','{"review_plan_only":true,"model_calls":0}'::jsonb,
   'outcome',false);
 IF next_step.status <> 'leased' OR next_step.stage_name <> 'outcome' THEN
   RAISE EXCEPTION 'authenticated_stage_transition_failed';
 END IF;
 SELECT * INTO final_step FROM hl_control.fenced_executor_advance_v1(
   lease.task_id,lease.lease_epoch,lease.lease_token,
   'outcome','{"human_review_required":true,"external_actions":0}'::jsonb,
   NULL,true);
 IF final_step.status <> 'completed' THEN
   RAISE EXCEPTION 'authenticated_completion_failed';
 END IF;
 BEGIN
   PERFORM * FROM hl_control.fenced_executor_advance_v1(
     lease.task_id,lease.lease_epoch,lease.lease_token,
     'outcome','{"duplicate":true}'::jsonb,NULL,true);
   RAISE EXCEPTION 'replayed_completed_token_accepted';
 EXCEPTION WHEN OTHERS THEN
   IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
 END;
END $login$;
SQL

# A different password-authenticated connection is confined to its own
# project, and may abort its own task but cannot act as the A principal.
PGUSER=hl_test_executor_b PGPASSWORD="$password_b" psql -X -q -v ON_ERROR_STOP=1 <<'SQL'
DO $login$
DECLARE lease record; result record;
BEGIN
 IF session_user IS DISTINCT FROM 'hl_test_executor_b' THEN
   RAISE EXCEPTION 'second_authenticated_session_identity_wrong';
 END IF;
 BEGIN
   PERFORM * FROM hl_control.fenced_executor_claim_v1(
     'fenced_password_login_a','login-a-20261123-task-key',60);
   RAISE EXCEPTION 'second_role_cross_project_access';
 EXCEPTION WHEN OTHERS THEN
   IF SQLERRM NOT LIKE '%fenced_executor_task_out_of_scope%' THEN RAISE; END IF;
 END;
 SELECT * INTO lease FROM hl_control.fenced_executor_claim_v1(
   'fenced_password_login_b','login-b-20261123-task-key',60);
 SELECT * INTO result FROM hl_control.fenced_executor_abort_v1(
   lease.task_id,lease.lease_epoch,lease.lease_token,'operator_abort');
 IF result.status <> 'dead_letter' THEN
   RAISE EXCEPTION 'authenticated_abort_failed';
 END IF;
END $login$;
SQL

# Unmapped, password-authenticated login still cannot take a task.
PGUSER=hl_test_executor_unbound PGPASSWORD="$password_unbound" \
  psql -X -q -v ON_ERROR_STOP=1 <<'SQL'
DO $login$
BEGIN
 IF session_user IS DISTINCT FROM 'hl_test_executor_unbound' THEN
   RAISE EXCEPTION 'unbound_session_login_failed';
 END IF;
 BEGIN
   PERFORM * FROM hl_control.fenced_executor_claim_v1(
     'fenced_password_login_a','login-a-20261123-task-key',60);
   RAISE EXCEPTION 'unbound_login_was_authorized';
 EXCEPTION WHEN OTHERS THEN
   IF SQLERRM NOT LIKE '%fenced_executor_unbound%' THEN RAISE; END IF;
 END;
END $login$;
SQL

# Non-sensitive assertions run only as the ephemeral fixture administrator.
PGUSER=postgres PGPASSWORD="$admin_password" psql -X -q -v ON_ERROR_STOP=1 <<'SQL'
SELECT public.assert_true(
  (SELECT status='completed' AND fenced_token IS NULL
   FROM hl_control.tasks WHERE task_id='fenced_password_login_a'),
  'authenticated_login_a_completed_and_revoked_token');
SELECT public.assert_true(
  (SELECT status='dead_letter' AND fenced_token IS NULL
   FROM hl_control.tasks WHERE task_id='fenced_password_login_b'),
  'authenticated_login_b_aborted_own_project');
SELECT public.assert_true(
  (SELECT status='held' AND lease_owner IS NULL
   FROM hl_control.tasks WHERE task_id='fenced_password_paid_a'),
  'authenticated_login_never_authorized_paid_model');
SQL

unset password_a password_b password_unbound admin_password
echo "G3_REAL_PASSWORD_AUTHENTICATED_RESTRICTED_LOGIN_PASSED"
