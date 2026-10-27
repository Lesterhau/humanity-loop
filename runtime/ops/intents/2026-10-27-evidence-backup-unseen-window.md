# INTEND — Evidence Integrity Backup unseen-DOI scan window

- Observed: 2026-10-27T23:03:17Z (authorized database clock).
- Owner: Humanity Loop main worker, bounded Tier-0 reliability improvement.
- Target: `scripts/evidence_integrity_backup.py` and `scripts/test_evidence_integrity_backup.py` in the canonical public repository.
- Defect: `extract_retractions()` truncates the Crossref list to `MAX_DOIS=15` **before** `scan()` filters already-seen DOIs. If the first 15 Crossref retractions are already recorded, eligible unseen DOIs in positions 16–25 are never examined, despite the source limit advertising 25 rows.
- Intended correction: preserve the complete bounded Crossref candidate list; in `scan()`, cap actual **unseen DOI attempts** to 15 after filtering known entries. Keep sequential upstream requests, 503/429 stop behavior, no mark-seen on failure, existing queue, and no outbound messaging.
- Offline regression: construct 16 known retractions plus one unseen 17th; verify the 17th is scanned; construct 17 unseen and verify only 15 attempted, preserving unprocessed DOIs. Preserve existing failure tests.
- Verification: independently read back both source and test files; inspect the GitHub Actions evidence-integrity-backup workflow result and its offline test output. A successful source write alone is not proof that the external Europe PMC HTTP 503 has recovered.
- Rollback: revert the two file changes if tests fail or coverage/safety semantics regress.
- Impact classification: internal detector coverage improvement only. No verified new scientific finding, journal correction or beneficiary effect is claimed.
