# INTEND — Hourly Worker verified evidence-triage heartbeat (2026-10-23 CDT)

Owner: Humanity Loop main worker
Risk tier: Tier 0 (internal observability update)
Authority: `AUTOMATION-PROMPT.md`, `OPS-SENTINEL.md`, `OPERATIONS.md`

Target: `runtime/ops/hourly-worker.json` on canonical GitHub main branch.

Verified work: Read-only review of publisher's 2025 pediatric orthodontics systematic-review bibliography and a purported Crossref retraction notice. Changed one evidence-integrity candidate from unreviewed to low-priority triaged with explicit uncertainty and follow-up; canonical queue readback confirmed. Evidence commit: `86aa94f3bdabc7cfb2b15bbd645d2369f963e429`.

Intended heartbeat: status `worked`; summary explicitly limits result to triage and does not claim editorial action, clinical correction, beneficiary outcome, autonomous Scout rotation, or verified publisher retraction; `lastVerifiedAt` uses the time the queue was independently verified and `evidenceUrl` links to the verified commit.

Acceptance: independently fetch heartbeat JSON and confirm all fields match intended verified work. Rollback: restore previous blob. No outreach, new schedules, spending, or third-party changes.
