# INTEND — Correct public README operational claims

Owner: Humanity Loop main hourly worker.
Date: 2026-10-24.
Risk: Tier-0, public documentation only. No runtime, secrets, permissions, automation, spending, external messaging, or user accounts.

## Evidence checked
- Current `AUTOMATION-PROMPT.md` and `PROJECT-STATE.md` state the dedicated ChatGPT Foundry worker is disabled and native AppDeploy Foundry/Evidence Integrity crons were disabled for exhausted credits.
- Open issue #16 documents the native cron shutdown and missing verified Foundry execution.
- `runtime/evidence-integrity-backup/latest.json` at 2026-10-24T12:18:08Z records Europe PMC HTTP 503 and no completed citation coverage on that run.
- Open issue #17 says MOTHER unattended inbox triage, real-human field trial and mobile plugin onboarding remain unverified.
- `mcp-server/app/join/page.tsx` has a source-level MCP connection instruction improvement; deployment/browser acceptance and real contributor first useful task remain unverified.

## Intended action
Update only `README.md` to correct inaccurate present-tense assertions that the dedicated Foundry worker is running, native Evidence Integrity scheduler is healthy, onboarding is end-to-end validated, and unattended MOTHER or contributor task completion is established. Preserve valid verified milestones and existing links. Distinguish live website/source-level functionality from independently proven scheduled execution, adoption and outcomes.

## Acceptance / rollback
Fetch the updated README independently, compare the corrected claims, verify no contradictory active-scheduler assertions remain, and cite the resulting GitHub commit. Revert the single README change if incorrect. Do not infer live production deployment from GitHub source.
