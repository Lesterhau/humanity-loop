#!/usr/bin/env bash
# Disposable PostgreSQL ONLY. Non-destructive namespace-boundary probes for the
# fenced executor facade.
#
# A caller controls its own temporary schema. This test fills that schema with
# look-alike types, tables and functions, then drives the full wrapper
# lifecycle over real password-authenticated connections. Every look-alike is
# inert for the session that created it and only raises an error if it is ever
# evaluated with privileges other than the caller's own. The facade passes when
# no look-alike is reached and every call behaves exactly as it does without
# them.
#
# The probes change no data beyond two synthetic tasks this script inserts and
# completes through the normal wrappers. Database TEMP is granted to two test
# logins for the duration of the probes and always removed again, so the
# function-level defense is exercised even where the database-level one holds.
set -euo pipefail
set +x

# Fail closed outside the two disposable GitHub Actions workflows.
[[ "${GITHUB_ACTIONS:-}" == true && "${CI:-}" == true && "${GITHUB_REPOSITORY:-}" == Lesterhau/humanity-loop ]] || exit 2
[[ "${PGHOST:-}" == 127.0.0.1 && "${PGPORT:-}" == 5432 && "${PGDATABASE:-}" == foundry_ci && "${PGUSER:-}" == postgres ]] || exit 2
[[ "${PGPASSWORD:-}" == test_only_ephemeral_local_db || "${PGPASSWORD:-}" == rehearsal_only_ephemeral_test_db ]] || exit 2
unset PGSERVICE PGSERVICEFILE PGPASSFILE PGOPTIONS PGHOSTADDR PGSSLCERT PGSSLKEY PGSSLROOTCERT PGSSLCRL PGSSLCRLDIR

: "${PGPASSWORD:?ephemeral CI database password must be supplied}"
: "${PGDATABASE:?}"
schema="${HL_FENCED_SCHEMA:-hl_control}"
prefix="${HL_FENCED_ROLE_PREFIX:-hl_test_executor_}"
[[ "$schema" =~ ^[a-z_][a-z0-9_]{0,40}$ && "$prefix" =~ ^[a-z_][a-z0-9_]{0,40}$ ]] || exit 2
role_a="${prefix}a"
role_unbound="${prefix}unbound"
marker='HL_BOUNDARY_PROBE_REACHED_PRIVILEGED_CONTEXT'
admin_password="$PGPASSWORD"
pass_a="$(openssl rand -hex 24)"
pass_unbound="$(openssl rand -hex 24)"
work="$(mktemp -d)"

admin() {
  PGUSER=postgres PGPASSWORD="$admin_password" psql -X -q -At -v ON_ERROR_STOP=1 \
    -v schema="$schema" -v role_a="$role_a" -v role_unbound="$role_unbound" "$@"
}
fail() { echo "BOUNDARY_FAILURE: $1" >&2; exit 1; }
public_temp="${HL_FENCED_ALLOW_PUBLIC_TEMP:-false}"
[[ "$public_temp" == true || "$public_temp" == false ]] || exit 2
revoke_temp() { # Never change database ACL in the public-TEMP rehearsal.
  if [[ "$public_temp" == false ]]; then
    admin -v db="$PGDATABASE" <<<'REVOKE TEMPORARY ON DATABASE :"db" FROM :"role_a", :"role_unbound";'
  fi
}
restore() {
  revoke_temp >/dev/null 2>&1 || true
  rm -rf -- "$work"
}
trap restore EXIT

# Fingerprint of everything the probes must leave untouched.
fingerprint() {
  admin <<'SQL'
SELECT pg_catalog.md5(pg_catalog.concat_ws('|',
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', db_session_role, agent_id, project_id, enabled), ';' ORDER BY db_session_role)
     FROM :"schema".fenced_executor_bindings),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', rolname, rolsuper, rolbypassrls, rolcreaterole, rolcreatedb, rolreplication, rolinherit, rolcanlogin), ';' ORDER BY rolname)
     FROM pg_catalog.pg_roles WHERE rolname !~ '^pg_'),
  (SELECT pg_catalog.count(*) FROM pg_catalog.pg_auth_members),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', p.proname, p.proowner, p.prosecdef, p.proconfig::pg_catalog.text, p.proacl::pg_catalog.text), ';' ORDER BY p.oid)
     FROM pg_catalog.pg_proc p JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname = :'schema'),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', c.relname, c.relowner, c.relrowsecurity, c.relacl::pg_catalog.text), ';' ORDER BY c.oid)
     FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = :'schema'),
  (SELECT pg_catalog.count(*) FROM :"schema".tasks WHERE task_id NOT LIKE 'fenced_boundary_probe_%'),
  (SELECT pg_catalog.md5(pg_catalog.string_agg(pg_catalog.concat_ws(',', task_id, status, lease_owner, fenced_epoch, fenced_token, payload::pg_catalog.text), ';' ORDER BY task_id))
     FROM :"schema".tasks WHERE task_id NOT LIKE 'fenced_boundary_probe_%')
));
SQL
}

before="$(fingerprint)"

if [[ "$public_temp" == false ]]; then
  admin -v db="$PGDATABASE" <<<'GRANT TEMPORARY ON DATABASE :"db" TO :"role_a", :"role_unbound";'
else
  [[ "$(admin <<<"SELECT has_database_privilege(:'role_a',current_database(),'TEMP') AND has_database_privilege(:'role_unbound',current_database(),'TEMP');")" == t ]] || fail 'public TEMP fixture unavailable'
fi
admin -v db="$PGDATABASE" -v pass_a="$pass_a" -v pass_unbound="$pass_unbound" <<'SQL'
ALTER ROLE :"role_a" PASSWORD :'pass_a';
ALTER ROLE :"role_unbound" PASSWORD :'pass_unbound';
INSERT INTO :"schema".tasks (task_id, project_id, payload, risk_tier, status, stages, current_stage, max_attempts)
SELECT v.task_id, b.project_id,
       pg_catalog.jsonb_build_object('fencing_required', 'true', 'idempotency_key', v.operation_key,
         'execution_mode', 'deterministic_only', 'external_actions', false,
         'model_calls', 0, 'max_provider_credits', 0),
       0, 'held', '["scout","outcome"]', 'scout', 3
FROM (VALUES ('fenced_boundary_probe_1', 'boundary-probe-1-operation-key'),
             ('fenced_boundary_probe_2', 'boundary-probe-2-operation-key')) AS v(task_id, operation_key)
JOIN :"schema".fenced_executor_bindings b ON b.db_session_role = :'role_a';
SQL
held="$(admin <<<"SELECT pg_catalog.count(*) FROM :\"schema\".tasks WHERE task_id LIKE 'fenced_boundary_probe_%' AND status = 'held';")"
[[ "$held" == 2 ]] || fail 'probe tasks were not created for the bound test role'

# Look-alike objects. Types the wrappers and base functions name, relations
# they read, and built-in functions they call.
cat > "$work/plant.sql" <<SQL
CREATE FUNCTION pg_temp.hl_boundary_probe(pg_catalog.anyelement) RETURNS pg_catalog.bool
LANGUAGE plpgsql AS \$probe\$
BEGIN
  IF current_user IS DISTINCT FROM session_user THEN
    RAISE EXCEPTION '$marker';
  END IF;
  RETURN true;
END \$probe\$;
CREATE DOMAIN pg_temp.text AS pg_catalog.text CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.jsonb AS pg_catalog.jsonb CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.uuid AS pg_catalog.uuid CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.int4 AS pg_catalog.int4 CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.int8 AS pg_catalog.int8 CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.bool AS pg_catalog.bool CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.name AS pg_catalog.name CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.timestamptz AS pg_catalog.timestamptz CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.interval AS pg_catalog.interval CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE DOMAIN pg_temp.regclass AS pg_catalog.regclass CHECK (pg_temp.hl_boundary_probe(VALUE));
CREATE TEMP TABLE fenced_executor_bindings (db_session_role pg_catalog.text, agent_id pg_catalog.text,
  project_id pg_catalog.text, enabled pg_catalog.bool);
INSERT INTO pg_temp.fenced_executor_bindings
  SELECT session_user, b.agent_id, b.project_id, true FROM (VALUES ('fenced_worker_a', 'humanity-loop')) AS b(agent_id, project_id);
CREATE TEMP TABLE agents (agent_id pg_catalog.text, status pg_catalog.text, permissions pg_catalog.jsonb,
  expires_at pg_catalog.timestamptz);
INSERT INTO pg_temp.agents VALUES ('fenced_worker_a', 'active', '["tier0"]', NULL);
CREATE TEMP TABLE tasks (task_id pg_catalog.text, project_id pg_catalog.text);
CREATE TEMP TABLE events (event_type pg_catalog.text);
CREATE TEMP TABLE dead_letters (reason pg_catalog.text);
CREATE FUNCTION pg_temp.clock_timestamp() RETURNS pg_catalog.timestamptz
LANGUAGE plpgsql AS \$probe\$ BEGIN RAISE EXCEPTION '$marker'; END \$probe\$;
CREATE FUNCTION pg_temp.gen_random_uuid() RETURNS pg_catalog.uuid
LANGUAGE plpgsql AS \$probe\$ BEGIN RAISE EXCEPTION '$marker'; END \$probe\$;
SET search_path TO pg_temp, public;
SQL

as_role() { # role, password, remaining psql arguments
  local role="$1" password="$2"; shift 2
  PGUSER="$role" PGPASSWORD="$password" psql -X -q -At -v ON_ERROR_STOP=1 -v schema="$schema" "$@"
}

# 1. A login with no binding stays unbound even with a look-alike bindings table.
cat "$work/plant.sql" > "$work/unbound.sql"
cat >> "$work/unbound.sql" <<'SQL'
SELECT * FROM :"schema".fenced_executor_claim_v1('fenced_boundary_probe_1', 'boundary-probe-1-operation-key', 60);
SQL
if out="$(as_role "$role_unbound" "$pass_unbound" -f "$work/unbound.sql" 2>&1)"; then
  fail 'unbound login obtained a lease'
fi
grep -q "$marker" <<<"$out" && fail 'a caller-supplied object was evaluated in a privileged context (unbound path)'
grep -q 'fenced_executor_unbound' <<<"$out" || fail 'unbound login was rejected for an unexpected reason'

# 2. A bound login completes the whole lifecycle exactly as without look-alikes.
cat "$work/plant.sql" > "$work/bound.sql"
cat >> "$work/bound.sql" <<'SQL'
SELECT lease_epoch AS e1, lease_token AS t1
  FROM :"schema".fenced_executor_claim_v1('fenced_boundary_probe_1', 'boundary-probe-1-operation-key', 60) \gset
SELECT (expires_at IS NOT NULL) AS renewed
  FROM :"schema".fenced_executor_renew_v1('fenced_boundary_probe_1', :e1, :'t1', 60) \gset
SELECT status AS s1, stage_name AS n1
  FROM :"schema".fenced_executor_advance_v1('fenced_boundary_probe_1', :e1, :'t1', 'scout',
       '{"probe":"namespace boundary"}', 'outcome', false) \gset
SELECT status AS s2
  FROM :"schema".fenced_executor_advance_v1('fenced_boundary_probe_1', :e1, :'t1', 'outcome',
       '{"human_review_required":true}', NULL, true) \gset
SELECT lease_epoch AS e2, lease_token AS t2
  FROM :"schema".fenced_executor_claim_v1('fenced_boundary_probe_2', 'boundary-probe-2-operation-key', 60) \gset
SELECT status AS s3
  FROM :"schema".fenced_executor_abort_v1('fenced_boundary_probe_2', :e2, :'t2', 'operator_abort') \gset
\echo BOUNDARY_RESULT :renewed :s1 :n1 :s2 :s3
SQL
out="$(as_role "$role_a" "$pass_a" -f "$work/bound.sql" 2>&1)" || {
  grep -q "$marker" <<<"$out" && fail 'a caller-supplied object was evaluated in a privileged context (bound path)'
  fail 'bound lifecycle failed with look-alike objects present'
}
grep -q "$marker" <<<"$out" && fail 'a caller-supplied object was evaluated in a privileged context (bound path)'
grep -qx 'BOUNDARY_RESULT t leased outcome completed dead_letter' <<<"$out" \
  || fail 'bound lifecycle produced an unexpected result'

# 3. Outcome, attribution and collateral state, read back by the administrator.
admin <<'SQL'
SELECT pg_catalog.set_config('hl_boundary.schema', :'schema', false) AS hl_boundary_1,
       pg_catalog.set_config('hl_boundary.role_a', :'role_a', false) AS hl_boundary_2 \gset
DO $verify$
DECLARE v_schema pg_catalog.text := pg_catalog.current_setting('hl_boundary.schema');
        v_role pg_catalog.text := pg_catalog.current_setting('hl_boundary.role_a');
        n pg_catalog.int8;
BEGIN
  EXECUTE pg_catalog.format($q$SELECT pg_catalog.count(*) FROM %1$I.tasks
     WHERE (task_id = 'fenced_boundary_probe_1' AND status = 'completed' AND fenced_token IS NULL AND lease_owner IS NULL)
        OR (task_id = 'fenced_boundary_probe_2' AND status = 'dead_letter' AND fenced_token IS NULL)$q$, v_schema) INTO n;
  IF n <> 2 THEN RAISE EXCEPTION 'BOUNDARY_FAILURE: probe tasks did not reach their expected final states'; END IF;
  EXECUTE pg_catalog.format($q$SELECT pg_catalog.count(*) FROM %1$I.events e
     WHERE e.task_id LIKE 'fenced_boundary_probe_%%'
       AND e.agent_id IS DISTINCT FROM (SELECT b.agent_id FROM %1$I.fenced_executor_bindings b WHERE b.db_session_role = %2$L)$q$,
     v_schema, v_role) INTO n;
  IF n <> 0 THEN RAISE EXCEPTION 'BOUNDARY_FAILURE: an audit event is attributed to another identity'; END IF;
END $verify$;
SQL

revoke_temp >/dev/null
[[ "$(fingerprint)" == "$before" ]] || fail 'state outside the two probe tasks changed'

# 4. With the temporary grant removed, the database-level defense holds as well.
if [[ "$public_temp" == true ]]; then
  as_role "$role_unbound" "$pass_unbound" -c 'CREATE TEMP TABLE hl_boundary_allowed (x pg_catalog.int4)' >/dev/null 2>&1 || fail 'baseline TEMP unexpectedly unavailable'
  echo 'G3_PUBLIC_TEMP_NAMESPACE_PROBE_PASSED'
elif as_role "$role_unbound" "$pass_unbound" -c 'CREATE TEMP TABLE hl_boundary_denied (x pg_catalog.int4)' >/dev/null 2>&1; then
  fail 'test executor can still create temporary objects'
fi

unset pass_a pass_unbound
echo 'G3_FENCED_NAMESPACE_BOUNDARY_PROBES_PASSED'
