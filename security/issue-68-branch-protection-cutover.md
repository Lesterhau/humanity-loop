# Issue #68 — reviewable branch-protection cutover (preparation only)

**Prepared:** November 16, 2026 (read-only repo and account verification). **Status: DRAFT, NOT ACTIVATED.** This document is an implementation and acceptance handoff, not a request to bypass GitHub controls. Preparing the document does **not** change existing branch rules, CODEOWNERS, credentials, workflow behavior, workers, billing, hosting or permissions.

**Acceptance issue:** [#68](https://github.com/Lesterhau/humanity-loop/issues/68). The related Foundry safety gate [#14](https://github.com/Lesterhau/humanity-loop/issues/14) is separate. All actual administrative and worker identity changes require distinct, explicit owner approval.

## Verified trust-root gap

- GitHub repository `Lesterhau/humanity-loop` is public. The actual `main` branch reports `protected=false`; repository rulesets API returns `[]`. There is no enforced CODEOWNERS review.
- `.github/CODEOWNERS` exists (merged PR #86) and assigns sensitive runtime, gateway, governance and automation instruction paths to `@Lesterhau`. Its existence alone has no blocking effect.
- The connected GitHub principal is currently **`Lesterhau` with admin permission**. An autonomous writer operating through the same principal cannot provide independent owner-vs-agent identity separation by opening a PR. Merely asking a model not to bypass a rule is not enforcement.
- The **original hourly worker is already active**. Keep the worker and its existing queue intact during migration; do not create a second worker or grant a new identity broader permissions than needed.

## Five directly dependent automated receipt writers

Each named workflow currently has `contents: write` and a `git push origin HEAD:main` step. This is different from workflows that only read files or write issue comments.

| Existing workflow | What directly reaches `main` today | Required replacement acceptance |
|---|---|---|
| `.github/workflows/ops-sentinel.yml` | `runtime/ops-sentinel/latest.json` and `runtime/reciprocal-audit/latest.json` | Scheduled watchdog + weekly audit receipts remain legible, persisted, and alerting remains truthful |
| `.github/workflows/cap-daily-audit.yml` | `runtime/cap-daily-audit/**` | Source checks, historical comparison and saved CAP receipt verified |
| `.github/workflows/federal-policy-delta.yml` | `runtime/federal-policy-delta/**` | All configured official sources and daily receipt verified; no hidden native replacement |
| `.github/workflows/critical-guidance-delta.yml` | `runtime/critical-guidance-delta/**` | WHO/FDA/EMA coverage and failure visibility retained; no unapproved AI classification spend |
| `.github/workflows/evidence-integrity-backup.yml` | `runtime/evidence-integrity-backup/**` | Public-metadata-only research backup and limitations/queue retained |

**Do not enable a blanket "Require a pull request" rule until these writers have an approved and tested destination.** Direct pushes would then fail; green execution steps are not proof of durable receipts. A broad bot bypass weakens the exact security boundary being installed.

Other workflow-sensitive paths include registry/release publishing and issue-only actions. Re-audit `.github/workflows/` and available repository settings immediately before activating a rule; the table above lists the **five confirmed direct-`main` receipt writers**, not every possible branch/ruleset dependency.

## Proposed staged migration

### A. Establish distinct writer identity (owner action; NOT done)

1. Create a **Humanity Loop-only** GitHub App / machine principal with minimum read, issue-comment, branch/content and PR scopes needed for approved tasks, **no Administration or global bypass**. Do not place secrets in GitHub public repo, automation prompts, comments or private chat handoffs.
2. Verify the current ChatGPT GitHub connector **actually acts as** the new restricted principal before claiming an access change. Creating an app without connecting/using it does not fix identity separation.
3. Verify the new principal can read instructions and file a narrow issue/PR, but **cannot** edit repository settings, change rules, approve its own protected changes, or access unrelated repositories.
4. Preserve the single original worker. An external task or scheduler cannot be recreated as a shortcut to an access transition.

### B. Migrate direct writes before enforcement (separate owner-approved PR)

1. Choose a reviewable, least-privilege persistence path for each of the **five** existing GitHub Actions receipt writers. Options to evaluate include bounded branch+PR batches or durable workflow artifacts with reviewed promotion. Record retention and discovery tradeoffs; **do not silently drop canonical GitHub evidence** or approve limitless bot bypass.
2. Separately modify the existing hourly worker's **write route** to a reviewable PR/branch path while preserving its read-only research, source checks, current schedule and appropriately scoped issue comments. Changing its saved automation prompt is a **separate action and requires explicit owner approval**.
3. Before applying protection, test a real non-production receipt path and independently check the artifact exists in the expected durable location. Confirm latest substantive official-source reviews still produce a report, even when no change is found. Verify prior receipts survive.
4. Prepare rollback triggers: missing/late receipts, denied CI checks, duplicate or lost jobs, wrong permission actor, accidental secrets, or loss of risk gates. Stop rather than auto-weakening protected control files.

### C. Activate ruleset (separate owner action; NOT done)

Once A/B are independently accepted, use GitHub's actual available ruleset/branch-protection controls on `main`:

- Require a pull request before merge.
- Require at least **one approving review from a different accountable human**, including **CODEOWNERS** where supported.
- Block force pushes and deletion, including accidental alternate paths.
- Require stable, **always-present** relevant checks. The `Validate Humanity Loop ledger` workflow has an unfiltered `pull_request` trigger; confirm the exact job check name in current GitHub's UI. Do **not** blindly require path-filtered MCP, Foundry, manual-triage or PolicyEngine checks for unrelated PRs, because they may not run.
- Don't give the autonomous writer an owner/administrative bypass, and don't create unbounded bot direct-`main` exceptions under the guise of saving receipt pipelines.
- Confirm free/public repository support and the actual enforcement level before relying on it. A configured-looking but bypassable rule is not acceptance.

### D. Negative and positive proof (independently read back)

| Test | Expected |
|---|---|
| Agent attempts direct `main` push to `AUTOMATION-PROMPT.md`, `HOURLY-CONTINUITY-QUEUE.md`, `GOVERNANCE.md`, `.github/workflows/` | Explicit **denied**, with no partial file write |
| Agent attempts a settings/admin modification or out-of-scope repository operation | Explicit **denied** |
| Agent opens narrow PR to change a public-safe record | PR available to owner; agent cannot approve/merge its own protected change |
| Separate human reviews and merges compliant PR | Relevant required checks pass and owner approval enforced |
| Next existing hourly worker run | Exactly one original worker; normal task queue remains readable; evidence write does not silently fail |
| Each of the five scheduled detector workflows | Latest scheduled run has inspectable persisted, source-attributed receipt in the agreed durable location |
| GitHub API readback | `main.protected=true` (or equivalent actual protection) and active ruleset contents match approved policy |
| Recovery drill | Owner can deliberately pause/roll back a broken ruleset without exposing privileged content or fabricating missed receipts |

**Close #68 only after all criteria actually pass.** A green synthetic test, this document, a merged CODEOWNERS file, or a screenshot of a rule editor alone is insufficient.

## Current limitations, handoff and no-action boundary

- No distinct agent principal has been connected.
- No existing direct-push workflow has been changed; no alternate receipt pipeline or bypass has been activated.
- No branch rule, GitHub identity, secret, scheduler, automations, costs, AgentMail contact, website/production deployment, AppDeploy operation or external publishing is authorized by this planning draft.
- Creating a draft PR may cause routine, automatic third-party **preview checks/builds** through repository integrations; a preview check is not a merge or production release and must not be represented as one.
- The next implementation step is a **separately approved, narrowly scoped migration PR** with observable pass/fail tests. Preserve issue #14 and project privacy restrictions independently.
