#!/usr/bin/env bash
# Disposable PostgreSQL ONLY. Self-test of check_fenced_candidate_acl.sql.
#
# A privilege checker that never fails proves nothing. Each case below applies
# one unsafe change, runs the checker and requires it to fail for the stated
# reason. Every case runs inside a transaction that is never committed, and a
# catalog fingerprint taken before and after must match, so the database is
# left exactly as it was.
set -euo pipefail
set +x

# Fail closed outside the two disposable GitHub Actions workflows.
[[ "${GITHUB_ACTIONS:-}" == true && "${CI:-}" == true && "${GITHUB_REPOSITORY:-}" == Lesterhau/humanity-loop ]] || exit 2
[[ "${PGHOST:-}" == 127.0.0.1 && "${PGPORT:-}" == 5432 && "${PGDATABASE:-}" == foundry_ci && "${PGUSER:-}" == postgres ]] || exit 2
[[ "${PGPASSWORD:-}" == test_only_ephemeral_local_db || "${PGPASSWORD:-}" == rehearsal_only_ephemeral_test_db ]] || exit 2
unset PGSERVICE PGSERVICEFILE PGPASSFILE PGOPTIONS PGHOSTADDR PGSSLCERT PGSSLKEY PGSSLROOTCERT PGSSLCRL PGSSLCRLDIR

: "${PGPASSWORD:?ephemeral CI database password must be supplied}"
: "${PGDATABASE:?}"
here="$(cd -- "$(dirname -- "$0")" && pwd)"
schema="${HL_FENCED_SCHEMA:-hl_control}"
prefix="${HL_FENCED_ROLE_PREFIX:-hl_test_executor_}"
definer="${HL_FENCED_DEFINER:-hl_fenced_definer}"
checker="${HL_FENCED_CHECKER:-$here/check_fenced_candidate_acl.sql}"
for v in "$schema" "$prefix" "$definer"; do
  [[ "$v" =~ ^[a-z_][a-z0-9_]{0,40}$ ]] || exit 2
done
[[ -f "$checker" && "$checker" != *[[:space:]\'\"\\]* ]] || exit 2
work="$(mktemp -d)"
trap 'rm -rf -- "$work"' EXIT

admin() {
  PGUSER=postgres psql -X -q -At -v ON_ERROR_STOP=1 \
    -v hl_schema="$schema" -v hl_role_prefix="$prefix" -v hl_definer="$definer" -v hl_allow_public_temp="${HL_FENCED_ALLOW_PUBLIC_TEMP:-false}" \
    -v exec_a="${prefix}a" -v exec_b="${prefix}b" -v exec_unbound="${prefix}unbound" \
    -v db="$PGDATABASE" -v owner="$owner" "$@"
}
owner=''
owner="$(admin <<<"SELECT pg_catalog.pg_get_userbyid(nspowner) FROM pg_catalog.pg_namespace WHERE nspname = :'hl_schema';")"
[[ -n "$owner" ]] || { echo 'MUTATION_SELF_TEST_FAILURE: schema not found' >&2; exit 1; }

fingerprint() {
  admin <<'SQL'
SELECT pg_catalog.md5(pg_catalog.concat_ws('|',
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', rolname, rolsuper, rolbypassrls, rolcreaterole, rolcreatedb, rolreplication, rolinherit, rolcanlogin), ';' ORDER BY rolname)
     FROM pg_catalog.pg_roles WHERE rolname !~ '^pg_'),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', roleid, member, admin_option, inherit_option, set_option), ';' ORDER BY roleid, member, grantor)
     FROM pg_catalog.pg_auth_members),
  (SELECT datacl::pg_catalog.text FROM pg_catalog.pg_database WHERE datname = pg_catalog.current_database()),
  (SELECT nspacl::pg_catalog.text FROM pg_catalog.pg_namespace WHERE nspname = :'hl_schema'),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', c.relname, c.relkind, c.relowner, c.relrowsecurity, c.relacl::pg_catalog.text), ';' ORDER BY c.relname)
     FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = :'hl_schema'),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', c.relname, a.attname, a.attacl::pg_catalog.text), ';' ORDER BY c.relname, a.attname)
     FROM pg_catalog.pg_attribute a JOIN pg_catalog.pg_class c ON c.oid = a.attrelid
     JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = :'hl_schema' AND a.attacl IS NOT NULL),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', p.proname, pg_catalog.oidvectortypes(p.proargtypes), p.proowner, p.prosecdef, p.proconfig::pg_catalog.text, p.proacl::pg_catalog.text), ';' ORDER BY p.proname, p.oid)
     FROM pg_catalog.pg_proc p JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname = :'hl_schema'),
  (SELECT pg_catalog.string_agg(pg_catalog.concat_ws(',', tablename, policyname, cmd, roles::pg_catalog.text, qual, with_check), ';' ORDER BY tablename, policyname)
     FROM pg_catalog.pg_policies WHERE schemaname = :'hl_schema'),
  (SELECT pg_catalog.count(*) FROM pg_catalog.pg_default_acl)
));
SQL
}

failures=0
cases=0
run_case() { # name, expected reason fragment, mutation SQL (empty for the control)
  local name="$1" expected="$2" sql="$3" out rc=0
  cases=$((cases + 1))
  {
    echo 'BEGIN;'
    printf '%s\n' "$sql"
    echo '\echo HL_MUTATION_APPLIED'
    echo "\\i $checker"
    echo 'ROLLBACK;'
  } > "$work/case.sql"
  out="$(admin -f "$work/case.sql" 2>&1)" || rc=$?
  if ! grep -q 'HL_MUTATION_APPLIED' <<<"$out"; then
    echo "MUTATION_SETUP_ERROR: $name" >&2; failures=$((failures + 1)); return
  fi
  if [[ -z "$sql" ]]; then
    [[ $rc -eq 0 ]] || { echo "CONTROL_FAILED: checker rejects the unmodified candidate" >&2; failures=$((failures + 1)); }
    return
  fi
  if [[ $rc -eq 0 ]]; then
    echo "MUTATION_NOT_DETECTED: $name" >&2; failures=$((failures + 1)); return
  fi
  if ! grep -q -- "$expected" <<<"$out"; then
    echo "MUTATION_WRONG_REASON: $name" >&2; failures=$((failures + 1))
  fi
}

before="$(fingerprint)"

run_case control '' ''

# Role attributes, membership and database privileges.
run_case executor_member_of_owner 'member of another role' \
  'GRANT :"owner" TO :"exec_b";'
run_case executor_bypassrls 'unsafe role attributes' \
  'ALTER ROLE :"exec_b" BYPASSRLS;'
if [[ "${HL_FENCED_ALLOW_PUBLIC_TEMP:-false}" == false ]]; then
  run_case executor_temp 'database TEMP or CREATE allowed' \
    'GRANT TEMPORARY ON DATABASE :"db" TO :"exec_unbound";'
fi
run_case wrapper_owner_login 'wrapper owner role can log in' \
  'ALTER ROLE :"hl_definer" LOGIN;'
run_case wrapper_owner_assumable 'can assume or inherit' \
  'CREATE ROLE hl_acl_mutation_probe LOGIN; GRANT :"hl_definer" TO hl_acl_mutation_probe;'

# Schema, table, column and default privileges.
run_case schema_create 'schema CREATE allowed' \
  'GRANT CREATE ON SCHEMA :"hl_schema" TO :"exec_a";'
run_case executor_table_grant 'table privilege differs' \
  'GRANT SELECT ON :"hl_schema".fenced_executor_bindings TO :"exec_unbound";'
run_case executor_column_grant 'column privilege' \
  'GRANT SELECT (task_id, fenced_token) ON :"hl_schema".tasks TO :"exec_b";'
run_case unlisted_role_table_grant 'table privilege differs' \
  'CREATE ROLE hl_acl_mutation_probe NOLOGIN; GRANT SELECT ON :"hl_schema".tasks TO hl_acl_mutation_probe;'
run_case wrapper_owner_extra_column 'UPDATE columns differ' \
  'GRANT UPDATE (payload) ON :"hl_schema".tasks TO :"hl_definer";'
run_case wrapper_owner_reads_audit 'table privilege differs' \
  'GRANT SELECT ON :"hl_schema".events TO :"hl_definer";'
run_case default_privileges 'default privileges are defined' \
  'ALTER DEFAULT PRIVILEGES IN SCHEMA :"hl_schema" GRANT SELECT ON TABLES TO anon;'

# Relations and row level security.
run_case rls_disabled 'row level security missing' \
  'ALTER TABLE :"hl_schema".fenced_executor_bindings DISABLE ROW LEVEL SECURITY;'
run_case open_policy 'policy applies to a role other' \
  'CREATE POLICY hl_acl_mutation_open ON :"hl_schema".tasks FOR SELECT TO PUBLIC USING (true);'
run_case view_over_private_table 'unexpected relation kind' \
  'CREATE VIEW :"hl_schema".task_overview AS SELECT task_id, fenced_token FROM :"hl_schema".tasks; GRANT SELECT ON :"hl_schema".task_overview TO :"exec_a";'

# Functions: path, owner, security mode, EXECUTE and look-alikes.
run_case wrapper_path_reset 'search_path is not pinned' \
  'ALTER FUNCTION :"hl_schema".fenced_executor_claim_v1(text,text,integer) RESET search_path;'
run_case wrapper_path_empty 'search_path is not pinned' \
  $'ALTER FUNCTION :"hl_schema".fenced_executor_claim_v1(text,text,integer) SET search_path TO \'\';'
run_case core_path_widened 'search_path is not pinned' \
  'ALTER FUNCTION :"hl_schema".claim_fenced_task_v1(text,text,text,integer) SET search_path TO pg_catalog, public, pg_temp;'
run_case wrapper_owner_changed 'wrapper not owned by' \
  'ALTER FUNCTION :"hl_schema".fenced_executor_renew_v1(text,bigint,uuid,integer) OWNER TO :"owner";'
run_case core_made_definer 'unexpected security mode' \
  'ALTER FUNCTION :"hl_schema".renew_fenced_lease_v1(text,text,bigint,uuid,integer) SECURITY DEFINER;'
run_case core_execute_public 'unexpected EXECUTE' \
  'GRANT EXECUTE ON FUNCTION :"hl_schema".claim_fenced_task_v1(text,text,text,integer) TO PUBLIC;'
run_case lookalike_overload 'unexpected function' \
  $'CREATE FUNCTION :"hl_schema".fenced_executor_claim_v1(text) RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path TO pg_catalog, pg_temp AS \'BEGIN END\'; GRANT EXECUTE ON FUNCTION :"hl_schema".fenced_executor_claim_v1(text) TO :"exec_unbound";'

[[ "$(fingerprint)" == "$before" ]] || { echo 'MUTATION_SELF_TEST_FAILURE: catalog state changed' >&2; exit 1; }
if [[ $failures -ne 0 ]]; then
  echo "MUTATION_SELF_TEST_FAILURE: $failures of $cases cases" >&2
  exit 1
fi
echo "G3_FENCED_ACL_CHECKER_MUTATION_SELF_TEST_PASSED cases=$cases"
