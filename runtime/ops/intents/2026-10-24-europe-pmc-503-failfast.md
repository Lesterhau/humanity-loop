# INTEND — Europe PMC upstream 503 containment (2026-10-24)
Owner: Humanity Loop main hourly worker. Tier: 0/1, reversible repository-only code/test change.

Observed evidence: runtime/evidence-integrity-backup/latest.json (2026-10-24T08:13:17Z) recorded 15 Europe PMC citation_lookup HTTP 503 failures; a fresh independent single DOI query on October 24 also returned HTTP 503. The current script retries the other DOI lookups despite an apparent provider-wide error. No claim is made about Europe PMC's root cause.

Exact intended mutation: in scripts/evidence_integrity_backup.py, stop the current scan after an HTTP 429/502/503/504 from Europe PMC, record a truthful provider-unavailable failure, and leave every unprocessed DOI unmarked so the next scheduled scan can retry. Add an offline regression to scripts/test_evidence_integrity_backup.py demonstrating no repeated lookup on a 503. Preserve all existing candidate queues, no email/outreach, no credentials, no changes to the provider or AppDeploy.

Verify: independently read back both GitHub files and run offline tests via the existing GitHub workflow (or equivalent read-only execution). Do not claim provider recovery or restored scientific coverage until a fresh successful receipt. Rollback: revert the code/test commits if tests fail or an unintended behavior is observed.
