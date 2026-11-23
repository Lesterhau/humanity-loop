# Staging auto-pause: zero-cash continuity and recovery

**Verified November 15, 2026, 18:13 Central / November 16, 00:13 UTC. Status: staging `ACTIVE_HEALTHY`; production `ACTIVE_HEALTHY`. No Supabase plan upgrade, synthetic new traffic, backup export, scheduler, cron change, or production write occurred during this assessment.**

## November 22–23 restoration and real hosted recheck

**New owner-provided Supabase screenshot:** the existing Free-tier project was actually **paused** after inactivity. This supersedes the November 15 *pre-pause* status in the historical entry below. The precise pause timestamp cannot be established from the image alone; no arbitrary 90-day deadline is invented.

**Actual recovery performed, with no plan upgrade or new project:** the project's authorized Supabase connector confirmed `INACTIVE`, accepted a `restore_project` action, progressed through `COMING_UP` and then returned **`ACTIVE_HEALTHY`**. Production `Humanity Loop Control Plane` remained a separate `ACTIVE_HEALTHY` project; neither project was replaced.

**Actual hosted synthetic acceptance:** In isolated staging `hl_foundry_test` (NOT production), ran a single SQL transaction that inserted one unique `ftest_...` Tier-0 queued task, atomically claimed it with the existing `claim_task` function, proved a **wrong lease token cannot complete it**, proved the right token succeeds, and checked its `completed` status. The whole transaction was **ROLLBACK**. A separate read-back query confirmed **0 residual tasks, 0 residual events** for that test identifier and **no new production-schema task table** in staging. No external report, contributor registration, model call, institutional message or paid service occurred.

**Staging compatibility finding:** `hl_foundry_test.claim_task/complete_task` already implements a test-only UUID lease-token check against expiry. This is **NOT** the full new production-canonical fenced-generation protocol, which includes an epoch and session-bound executor authorization. That [review-only code](G3-FENCED-LEASE-ACCEPTANCE.md) is still in isolated GitHub CI. Do not describe this hosted test as a deployed new fencing migration, G3 release or a public outcome.

**Vercel notifications from owner screenshots:** PR #108 and #109 each produced a Vercel `Ready` **preview**. The notifications do not prove a live database migration or external outcome and do not require action. Avoid deploying an independent new worker to resolve a preview notification.

## Immediate warning and impact

The project owner received a Supabase inactivity warning at approximately 18:07 Central November 15: **Humanity Loop Staging – Isolated**, ref `prisrhkxiwyrbcagxcxx`, would be automatically paused if sufficient project activity did not resume. The email states it was **not paused at send time**, and the current project management API separately confirms `ACTIVE_HEALTHY`. Supabase organization **RL Perspectives** is on the **Free** plan; low-activity projects may pause after a seven-day observation window.

**Not an outage of the live service:** separate production **Humanity Loop Control Plane**, ref `jxtcccrlnhkcjfnwlfea`, is `ACTIVE_HEALTHY`, and the production contributor front door uses that separate project. Auto-pausing this staging project should not itself stop the production site or production contributor-ledger queries. Staging-specific tests, `foundry-staging-bridge`, and `contributor-node-stage0` will stop responding until staging is resumed. Never redirect real people, their tokens, a real submission, or production traffic onto staging to keep it active.

The existing AppDeploy Foundry Alpha snapshot `1793911810822` is `READY`, and its own `cron.json=[]` (native Foundry scheduler OFF). Its server-to-server test bridge targets this staging project. If staging pauses, **the authorized synthetic bridge will temporarily be unavailable**; that is an expected test-only failure mode, not permission to retry automatically, recreate the project, issue new service tokens or activate model calls.

## Independently read-back non-secret recovery inventory

| Resource | Verified staging state |
| --- | --- |
| Supabase project | `prisrhkxiwyrbcagxcxx`, **ACTIVE_HEALTHY**, Postgres `17.11.0.011` |
| Organization / billing | RL Perspectives, **Free** |
| Edge Function | `foundry-staging-bridge` **ACTIVE v6**, no direct public access authorized without its separate secret |
| Edge Function | `contributor-node-stage0` **ACTIVE v3**, for isolated Stage-0 tests only |
| `hl_foundry_test` | 3 RLS-enabled tables: `tasks`, `events`, `approvals` |
| `hl_control` | 5 RLS-enabled isolated contributor simulation tables |
| Synthetic data | 5 Foundry tasks; 10 Foundry events; 0 approvals; 4 staging contributor nodes; 1 simulated submission; 9 simulated contributor events |
| Read-only ACL check | All 8 tables had RLS enabled and **no** direct SELECT for `anon`/`authenticated`/`service_role` |
| Foundry test procedures | `claim_task`, `complete_task`, `recover_expired_leases` — invoker, **no** direct EXECUTE/USAGE to `anon` or `authenticated` |
| Applied migration IDs | `20261101172121`, `20261101172137`, `20261104041238`, `20261104205353`, `20261108141202` |

The inventory is **metadata only**. It is **not a database backup**, a source-code export, a migration recreation guarantee, proof of full role isolation, or a validation that all private staging records were simulated. Do not commit the raw staging tables, Node token material, signed URLs, applicant details or private server secrets to this public GitHub repository.

## Restore deadline: treat 90 days as controlling

Supabase's owner warning says **resume within 90 days after actual pause**; older [Supabase policy announcement](https://supabase.com/changelog/27497-paused-free-plan-projects-are-restorable-for-90-days) agrees. The currently published [Free Project Pausing guide](https://supabase.com/docs/guides/platform/free-project-pausing) says **one year**, which conflicts with the warning. **For the owner's risk management, assume the shorter 90-day window until Supabase explicitly confirms a longer period for this project.** Do not start a deadline from the warning alone; record the actual pause-confirmation timestamp if it happens. The absence of a second email today does not establish that future pausing was avoided.

Do not upgrade to Pro or send meaningless keepalive pings to avoid a predictable free-plan behavior. Genuine, owner-authorized staging testing and Supabase dashboard operations are acceptable when an actual test is needed. Supabase's current guide notes that legitimate database requests count toward activity but does not guarantee a few calls will prevent pause.

## When an authorized test needs staging

1. Check [the isolated project in Supabase](https://supabase.com/dashboard/project/prisrhkxiwyrbcagxcxx). If status is active, verify the stored migration list and relevant Edge Function versions, then run the **specific legitimate low-risk synthetic test** once; no live contributor, external contact, production table write or paid model call.
2. If paused, **owner manually resumes that existing project** in the Supabase Dashboard; do not create a replacement Free project or rename one. Confirm it returns `ACTIVE_HEALTHY`; allow the normal restore process to finish.
3. Recheck both staging Edge Function slugs/versions, three test Foundry invoker routines, five applied migration IDs and the eight RLS-enabled tables. Confirm public `anon`/`authenticated` cannot directly read private tables. A restored project may have changed runtime or key status; don't silently trust old client tokens or recreate deleted keys.
4. Read AppDeploy `cron.json` and do not enable it. Run **one bounded, owner-authorized zero-model-call synthetic bridge health/reconciliation test** only after checking the already-consumed one-use test lock; never repeat a claim to recreate an earlier pass. Capture new read-only receipt with source/version/time.
5. If any security, schema, credential, or synchronization check fails, **stop**. Keep production independent and Founder/Foundry AI execution off; diagnose before granting access, resubmitting or moving test data.

## Backups and recovery outside the platform

Supabase's [database backups guide](https://supabase.com/docs/guides/platform/backups) recommends **`supabase db dump`** and private off-site backups for Free tier; automatic daily downloadable backups belong to paid plans. A proper owner-controlled encrypted export (schema, migration history and permissible synthetic data) requires a private authenticated database connection and verification that tokens/credentials are excluded. **No independent export or restore test has been performed here.** Never use a public GitHub commit as the backup store. The Supabase CLI v3 [November 4 breaking change](https://supabase.com/changelog/supabase-cli-v3) makes local the default target; explicitly verify CLI flags/target with `supabase db dump --help` before any hosted dump, and never guess connection parameters or expose a DSN to an AI/public terminal.

## Action owner and monitoring

- **Current disposition:** monitor opportunistically on next genuine staging usage; **do not add a keepalive schedule or new paid resource**. The existing Humanity Loop hourly coordination remains separate from native Foundry scheduling.
- **If paused:** owner can resume from the project Dashboard. Treat the **actual pause date plus 90 days** as the conservative recovery deadline.
- **Before a Foundry test resumes:** open [`FOUNDRY-RUNTIME.md`](FOUNDRY-RUNTIME.md), [issue #14](https://github.com/Lesterhau/humanity-loop/issues/14), verify credit hard stop and current deployed first-line decisions; do not treat a code snapshot or a staging test as evidence of public impact.

**Source boundary:** Supabase get-project/list-edge-functions/list-migrations/read-only SQL (Nov 15–16 UTC), current official Supabase docs, and the owner's warning screenshot. No change to infrastructure or cost assumptions has been made.
