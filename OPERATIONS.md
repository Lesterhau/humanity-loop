# Humanity Loop External Action Reliability Protocol

## November 7, 2026 — verified cost-containment cutover and rollback standard

**Active official-source monitors:** GitHub Actions `critical-guidance-delta.yml` for WHO/FDA/EMA and `federal-policy-delta.yml` for 17 federal sources. Both have two independently verified scheduled runs, source-level receipt checks and official-source baselines. AppDeploy native crons removed after verified cutover: Critical Guidance `critical-guidance-delta-y7nzmd` snapshot `1794087830193` and Federal Policy `federal-policy-delta-p49z0b` snapshot `1794088040386`; each has `cron.json=[]`. Historical app-local read APIs and dashboards remain; browser-facing archive disclaimers link to current GitHub source receipts. Critical Guidance public POST scan returns HTTP 410 and no longer triggers via frontend boot.

**Operational rollback if GitHub coverage degrades:** (1) inspect last saved `runtime/critical-guidance-delta/latest-run.json` / `runtime/federal-policy-delta/latest-run.json`, Actions run/job conclusions, source failures, and GitHub scheduling delays; (2) retain source snapshots and publish visible incomplete-coverage status, do not issue medical or legal claims; (3) consider manual deterministic GitHub `workflow_dispatch` for read-only scan only if supported without new cash; (4) restoring native AppDeploy cron requires separate risk-informed reauthorization, current credit-budget check, protection against duplicate processing, and a new deliberate deployment. Never silently reactivate native AI scanning while reserve breached. No outside publication/outreach from these monitors.

**Feature/coverage tradeoff:** GitHub detects pages but does not replicate native AI `ai.extract` safety materiality or `ai.generate` legal-question summaries. Human/approved agent review is required. Federal legislative source is official GPO/LOC bulk feed vs native Congress.gov homepage. Other native CAP/Evidence Integrity schedules remain in service until independent parity and historical UI decisions.

Every external write or action is treated as a transaction.

## Transaction lifecycle

1. **INTEND** — define the exact intended external mutation/action.
2. **EXECUTE** — perform it through an authorized tool.
3. **VERIFY** — independently read/check the destination or returned state.
4. **COMMIT** — only call the action successful after verification.
5. **FAILOVER** — if execution or verification fails, preserve the intended payload and failure details in a secondary durable store.
6. **RETRY / ESCALATE** — diagnose and retry only when safe; otherwise surface the blocker.

## Verification requirements

Examples:
- GitHub file write → fetch the file/commit back and confirm expected content.
- GitHub issue → retrieve/list the issue and confirm title/body/state.
- App deployment → check deployment status and, where relevant, rendered/API behavior.
- Email → confirm send result/thread state when tools expose it.
- Public form/report → preserve submission receipt or acknowledgement when available.

## Failure classes

- **Tool unavailable**
- **Permission/auth**
- **Rate limit**
- **Validation/schema**
- **Conflict/stale version**
- **Safety/policy interception**
- **Network/provider**
- **Unknown/unverified**

## Failure preservation

**Preservation is not resolution.** A fallback record exists so work is not lost; it never counts as completion.

Every unresolved fallback item must include:
- owner;
- exact blocked action;
- failure class;
- retry condition;
- next retry/review time or concrete blocker-change signal;
- escalation path;
- final closure evidence when resolved.

If GitHub is unavailable or a GitHub write is intercepted:
1. preserve the intended write, target path/issue, timestamp, and error in Undermind at:
   `/humanity-loop/operations/pending-external-actions.md`
2. mention the unresolved failure in the hourly automation output;
3. assign a next retry/review condition instead of leaving the item passively parked;
4. retry automatically when that condition is met or materially changed;
5. if the blocker persists past its stale threshold, escalate rather than silently carrying it forward;
6. once successful, mark the fallback item resolved with the final artifact/commit URL.

Do not weaken a safety/permission control merely to force a write through.

## Notification threshold

A failed external action is **always meaningful** when it:
- would otherwise cause work/evidence to be lost;
- blocks a live project;
- blocks a required ledger update;
- affects a safety/reliability control;
- persists across more than one cycle.

Those failures must be surfaced rather than hidden in routine logs.

## Monitoring cadence

The main Humanity Loop worker runs hourly, which is the maximum supported scheduled-task frequency. Each cycle must inspect unresolved external-action failures before starting lower-priority new work.


## Tertiary failover

If both the primary destination and the documented secondary durable store fail:
1. send a minimal internal alert to the MOTHER project inbox `mother.humanityloop@agentmail.to` with subject prefix `[FAILOVER]`;
2. include only non-sensitive metadata: timestamp, intended destination, failure class, project/item name, and a short recoverable summary;
3. never include secrets, credentials, private personal data, or other sensitive payloads in the email fallback;
4. surface the failure in the hourly log;
5. on the next successful storage cycle, reconcile the incident into `PENDING-ACTIONS.md`.

The system should not rely on one storage provider for failed-action recovery.


## Action authorization receipts

For side-effecting Humanity Loop actions, especially Tier-1+ actions, persist a compact authorization/execution receipt using `schema/action-receipt.schema.json` when practical.

The receipt binds:
- actor/role;
- exact target and action;
- a digest of the intended arguments/payload;
- risk tier and policy references;
- allow/transform/hold/deny/escalate decision;
- any required approval reference;
- execution evidence;
- independent verification evidence.

The executor should fail closed when a required receipt is missing, expired/stale, mismatched to the side-effecting payload, or explicitly held/denied.

A receipt does not replace human approval where governance requires it. It makes the permission and verification chain inspectable and reduces the risk that a later tool call executes a materially different action than the one that was reviewed.
