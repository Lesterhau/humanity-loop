# G3 — canonical fenced lease v1: tested migration candidate, NOT deployed

**Current release truth (November 22–23, 2026):** G2 is still the active milestone; G3 may develop in parallel but is not released. The production `hl_control.tasks` table and all its legacy stored procedures were **read-only audited**, not modified. Foundry native cron remains OFF and the owner-protected AppDeploy credit reserve has **no verified hard provider-level stop**.

## Real production gap identified

The authoritative production Supabase project runs **PostgreSQL 17.11**, with one existing `hl_control.tasks` table (at inspection: four completed historical Foundry tasks; no pending current task in that table). `claim_next_task` already uses `FOR UPDATE SKIP LOCKED`, giving atomic *initial* claims. However existing legacy advance/renew/fail methods check the stable lease **owner ID** and (sometimes) an expiry, **not the unique instance of a lease**. A delayed stage write by a prior process holding the same stable worker ID could be erroneously authorized after re-acquisition by that identity. This is a **preventive race analysis**, not a claim that an exploit occurred.

Read-only production privilege checks found `anon`, `authenticated` and `service_role` do **not** have usage on the private `hl_control` schema, UPDATE on the task table, or EXECUTE on `claim_next_task` (as inspected). Those facts are a point-in-time access snapshot, not a permanent guarantee.

## Candidate SQL in this repository

[Migration candidate](supabase/sql/hl_control_fenced_tasks_candidate_v1.sql) adds `fenced_epoch` and `fenced_token` to the **existing canonical task table**, not a competing database or scheduler.

One manually reviewed Tier-0 `held` task must explicitly carry immutable operation idempotency, `execution_mode=deterministic_only`, `model_calls=0`, `max_provider_credits=0` and `external_actions=false`. A granted lease consists of **task ID + specific active agent + monotonically increasing epoch + unpredictable UUID token + bounded expiry**. A claim is an atomic SQL UPDATE; only the holder of the **current** matching tuple may write a stage, renew or abort. Completion and abort revoke the token. Expired leases **dead-letter**, and do not silently retry any prior external action or model run.

Legacy `claim_next_task` is excluded from fenced tasks; existing legacy advance, v2 advance, renew, fail and expiry paths gain exact **fenced-scope** rejections. They remain available to nonfenced historical tasks. The new private functions are **SECURITY INVOKER** and explicitly revoke `PUBLIC` EXECUTE, with **no new grants** to external `anon`, `authenticated` or `service_role`.

**Important architecture caveat:** this migration is NOT enough to make a networked model executor safe. A `SECURITY INVOKER` role needs underlying table privileges; giving such a role broad UPDATE would defeat the intended function-only boundary. A future approved least-privileged backend principal, strongly scoped RPC interface or a narrowly audited **SECURITY DEFINER** service must be designed and negatively tested in staging **before any production grant or worker integration**. Do not add access grants to make a failed client call pass. The migration intentionally grants no one new execution authority.

## Actual isolated acceptance

**Independently checked GitHub execution:** [run #45097124531](https://github.com/Lesterhau/humanity-loop/actions/runs/45097124531), isolated PostgreSQL 17 job, **success**. Earlier isolated run #45096569416 also passed initial atomic-claim and stale-worker assertions; subsequent tightened scenarios were rerun and corrected before the passing final run. This final run includes explicit zero-model/zero-credit, denied unauthorized institutional outreach, and unchanged legitimate **unfenced** renew/advance/fail/retry/expiry/child-role completion. The concurrency step runs **two distinct overlapping real psql sessions** against the disposable DB. An ordinary repository ledger/governance CI run also passed; **neither run connected to Supabase production**.


The [PostgreSQL 17 CI workflow](.github/workflows/g3-canonical-lease-postgres.yml) runs in **a disposable GitHub Actions PostgreSQL service**, not Supabase production. It builds minimal canonical-shape synthetic tasks and agents, applies this migration there, and tests:

- Two genuinely overlapping SQL sessions claiming the same task: **one wins, one is rejected**.
- Same owner obtaining a *new* generation: stale prior UUID+epoch cannot write, renew or complete.
- Unauthorized role, missing human approval, Tier-1, bad idempotency, excessively long lease, bad stage transition, duplicate stage output: **rejected**.
- Explicit zero-model/no-outreach admission: claims with `model_calls > 0` or `external_actions=true` are **rejected**. This is **not** a paid-model budget stop.
- Old legacy APIs cannot mutate or requeue fenced tasks.
- Lease expiry transitions to a dead-letter record and invalidates the token; no automatic paid/provider retry.
- New entry points are not executable by test `anon`, `authenticated` or `service_role` roles.

These are SQL-level proofs in a **synthetic PostgreSQL 17 environment**. The isolated CI demonstrates SQL transaction behavior, **not a successful Supabase staging migration, privileged caller audit or production cutover**.

## Safely cut over later (not authorized by this candidate)

1. Independently inspect current production schema, function definitions, grants, active leases, dependent Edge functions and schedules. Save original function DDL/privileges for a reviewed rollback. The introspection above is a dated baseline, not a live migration contract.
2. Reconnect/recover the existing dedicated Supabase staging project (not a paid new branch) and install only there. Verify all nonfenced functions remain compatible and stale-owner/nonowner/expired rejection works with **real database permissions**.
3. Design a least-privileged server-side execution identity. No direct public task UPDATE; no exposed generic callable SECURITY DEFINER function. Revoke all unexpected grants and validate with negative RLS/role tests.
4. Deploy exactly one runner adapter requiring the token+epoch on EVERY stage/side-effect admission; carefully handle interrupted tasks and idempotent external effects. Protect against token logging and token reuse. Confirm the **existing task table** stays the one authority.
5. Independently enforce provider-level hard spending and per-call cost upper bounds. Until these are proven, `foundry_budget_governor.py` must continue to **DENY ALL discretionary paid AI**; no cron or fallback provider.
6. Execute one truly bounded, model-produced public-safe artifact and independent review, then separately record G3 release acceptance. Do not count local synthetic role text as a real LLM model call, and never count internal CI as a public-benefit WIN.

**Zero new payments, hosted accounts, provider calls or scheduled workers.** Current safe next step after PR merge: staging-role/cutover acceptance and provider hard-stop feasibility; if staging remains inaccessible, report the block and continue offline negative tests rather than quietly altering production.
