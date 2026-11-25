#!/usr/bin/env bash
# CI service database only. Never point this script at hosted staging.
set -euo pipefail
set +x
umask 077
[[ "${GITHUB_ACTIONS:-}" == true && "${CI:-}" == true && "${GITHUB_EVENT_NAME:-}" == pull_request ]] || exit 2
[[ "${PGHOST:-}" == 127.0.0.1 && "${PGPORT:-}" == 5432 && "${PGDATABASE:-}" == foundry_ci && "${PGUSER:-}" == postgres && "${PGPASSWORD:-}" == rehearsal_only_ephemeral_test_db ]] || exit 2
# No connection override or inherited alternative credential mechanism.
unset PGSERVICE PGSERVICEFILE PGPASSFILE PGOPTIONS PGHOSTADDR PGSSLCERT PGSSLKEY PGSSLROOTCERT PGSSLCRL PGSSLCRLDIR
here=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
python3 "$here/prepare.py" "$(git rev-parse --show-toplevel)" "$work/review"
psql -X -v ON_ERROR_STOP=1 -q -f "$here/baseline.sql"
psql -X -v ON_ERROR_STOP=1 -q -f "$work/review/fenced_task_test_fixture.sql"
psql -X -v ON_ERROR_STOP=1 -q -f "$work/review/hl_control_fenced_tasks_candidate_v1.sql"
psql -X -v ON_ERROR_STOP=1 -q -f "$work/review/test_fenced_canonical_lease.sql"
# Replace fixed shared temporary filenames with private work paths.
python3 - "$work/review/test_fenced_concurrent_claim.sh" <<'PY'
import pathlib,sys
p=pathlib.Path(sys.argv[1])
s=p.read_text()
for name in ('first','second'):
    s=s.replace(f'/tmp/hl_{name}_claim.log',f'"$HL_REHEARSAL_WORK/{name}.log"')
p.write_text(s)
PY
export HL_REHEARSAL_WORK="$work"
bash "$work/review/test_fenced_concurrent_claim.sh"
psql -X -v ON_ERROR_STOP=1 -q -f "$work/review/hl_fenced_executor_restricted_candidate_v1.sql"
psql -X -v ON_ERROR_STOP=1 -q -f "$here/harden.sql"
# Disposable database only; hosted TEMP policy must be separately reviewed.
psql -X -v ON_ERROR_STOP=1 -q -c 'REVOKE TEMPORARY ON DATABASE foundry_ci FROM PUBLIC'
psql -X -v ON_ERROR_STOP=1 -q -f "$work/review/test_restricted_fenced_executor.sql"
psql -X -v ON_ERROR_STOP=1 -q -f "$here/check.sql"
bash "$work/review/test_fenced_authenticated_login.sh"
psql -X -v ON_ERROR_STOP=1 -q -f "$here/check.sql"
export HL_FENCED_SCHEMA=hl_g3_rehearsal HL_FENCED_ROLE_PREFIX=hl_g3_rehearsal_ HL_FENCED_DEFINER=hl_g3_rehearsal_definer
bash "$here/../test_fenced_namespace_boundary.sh"
bash "$here/../test_fenced_acl_checker_mutations.sh"
psql -X -v ON_ERROR_STOP=1 -q -f "$here/check.sql"
psql -X -v ON_ERROR_STOP=1 -q -f "$here/cleanup.sql"
echo 'DISPOSABLE_STAGING_SHAPE_REHEARSAL_PASSED (not hosted login acceptance)'
