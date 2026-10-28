# INTEND — Crossref self-referential retraction metadata caveat

- Observed: 2026-10-28T02:12:28Z (authorized database clock).
- Owner: Humanity Loop Evidence Integrity / main worker. Tier 0 reversible detector metadata safety fix.
- Trigger: The 2026-10-27 Cheema tranexamic-acid review triage found a Crossref retraction-type relationship whose original DOI and alleged notice DOI were identical. Independent publisher/PubMed review verified an expression of concern, not a formal retraction. The scanner currently emits `retractedDoi` and `noticeDoi` without an explicit caveat.
- Intended scope: Update only `scripts/evidence_integrity_backup.py` and `scripts/test_evidence_integrity_backup.py` to preserve all candidates while flagging same-DOI relationships as self-referential, recording `noticeStatus: unverified` for all candidates, and requiring independent notice-status verification. Keep no automatic clinical judgments, no outreach, no removed candidates, and no changed deduplication semantics.
- Regression: A synthetic Crossref self-referential retraction-type update must still yield a citation candidate, explicitly marked ambiguous; a distinct notice/original DOI must remain distinct. Existing offline tests and workflow safety checks must pass.
- Verification: Independently fetch changed source and test; inspect triggered GitHub Actions result on exact commit. If CI fails, do not claim verified remediation; revert only through authorized, safety-compliant operation.
- Scope limitation: This changes how future candidates communicate metadata uncertainty. It does not correct Crossref or prove a clinical/public-health outcome.
