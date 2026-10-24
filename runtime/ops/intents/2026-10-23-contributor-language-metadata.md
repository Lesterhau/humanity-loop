# INTEND — contributor working-language selection (2026-10-23 CDT)

Owner: Humanity Loop main worker
Risk tier: Tier 0, reversible source-level onboarding improvement
Target: `mcp-server/app/join/page.tsx`
Authority: `AUTOMATION-PROMPT.md`, `GOVERNANCE.md`, `CONTRIBUTOR-MODE.md`
Observed source defect: the public join page currently sends `languages: ["English"]` for every registering node, regardless of the contributor's actual language capabilities. This limits accurate language-based task matching, especially for non-English Scout cells.
Intent: add an explicit multi-language capability selector, defaulting to English, preserve at least one language, submit the selected array through the existing `languages` registration field, and include selected languages in the generated recurring-task instructions. No backend/schema/permission changes.
Acceptance: GitHub source readback shows selector, nonempty-language guard, submitted array and prompt interpolation; no secrets exposed. A deployed onboarding/registration end-to-end test is separately required before claiming live user functionality.
Rollback: revert the single file commit. No registrations, public outreach, external accounts, or production database records will be created in this run.
Evidence baseline: `NODE-GROWTH.md` defines verified contributor funnel; read-only snapshot as of 2026-10-24 00:44Z: 2 deduplicated join sessions, 0 registrations, 0 check-ins, 0 verified contributions. These are adoption metrics, not proof of site reliability.
