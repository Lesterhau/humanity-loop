#!/usr/bin/env bash
# Only runs in GitHub Actions ephemeral PostgreSQL CI, never production.
set -euo pipefail
export PGHOST=127.0.0.1 PGPORT=5432 PGDATABASE=foundry_ci PGUSER=postgres
: "${PGPASSWORD:?ephemeral CI database password must be supplied}"

psql -X -v ON_ERROR_STOP=1 -Atqc "BEGIN;
  SELECT (hl_control.claim_fenced_task_v1(
    'fenced_race','fenced_worker_a','race-operation-key-2026',60
  )).task_id;
  SELECT pg_sleep(2);
COMMIT;" > /tmp/hl_first_claim.log 2>&1 &
first_pid=$!
sleep 0.35

if psql -X -v ON_ERROR_STOP=1 -Atqc  "SELECT (hl_control.claim_fenced_task_v1(
   'fenced_race','fenced_worker_b','race-operation-key-2026',60
 )).task_id;" > /tmp/hl_second_claim.log 2>&1; then
  echo "FENCING_FAILURE: simultaneous second claimant was accepted" >&2
  wait "$first_pid" || true
  exit 1
fi
wait "$first_pid"

if ! grep -q 'fenced_task_unavailable_or_already_leased' /tmp/hl_second_claim.log; then
  echo "FENCING_FAILURE: second claimant failed for an unexpected reason" >&2
  exit 1
fi

psql -X -v ON_ERROR_STOP=1 -Atqc  "SELECT public.assert_true(
   (SELECT status='leased' AND lease_owner='fenced_worker_a'
       AND fenced_epoch=1 AND fenced_token IS NOT NULL
    FROM hl_control.tasks WHERE task_id='fenced_race'),
   'exactly_one_claim_holder_after_concurrency'
 );"
echo 'FENCED_CONCURRENT_CLAIM_TEST_PASSED'
