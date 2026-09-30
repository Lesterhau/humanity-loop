# Humanity Loop External Action Reliability Protocol

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

If GitHub is unavailable or a GitHub write is intercepted:
1. preserve the intended write, target path/issue, timestamp, and error in Undermind at:
   `/humanity-loop/operations/pending-external-actions.md`
2. mention the unresolved failure in the hourly automation output;
3. retry on a later cycle only after diagnosing the failure;
4. once successful, mark the fallback item resolved with the final artifact/commit URL.

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
