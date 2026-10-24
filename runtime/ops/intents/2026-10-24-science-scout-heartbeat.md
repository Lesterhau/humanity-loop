# INTEND — source-reviewed science Scout heartbeat

- **Owner:** Humanity Loop main hourly worker
- **Observed UTC time:** 2026-10-24T08:05:33Z
- **Risk:** Tier 0, internal observability write
- **Authority:** AUTOMATION-PROMPT.md; OPS-SENTINEL.md; OPERATIONS.md
- **Target:** runtime/ops/hourly-worker.json on the canonical main branch
- **Verified work:** Source-reviewed the October 23 Springer retraction of Ponomarev et al. (2023) and independently identified an October 5, 2026 systematic review that cites the retracted study in a substantive narrative claim. Committed the bounded assessment and independently fetched it.
- **Evidence:** https://github.com/Lesterhau/humanity-loop/commit/a3fdb341c3f75d0b7d62116c8e865a12ab4347bf
- **Intended heartbeat:** schemaVersion 1, status worked; runAt 2026-10-24T08:05:33Z; lastVerifiedAt 2026-10-24T08:05:33Z; evidenceUrl as above. Summary must state no outreach, no clinical outcome, no Supabase Scout rotation recovery.
- **Verification:** Fetch updated JSON and confirm content, status, and evidence URL.
- **Rollback:** Restore previous verified heartbeat blob if the update is erroneous.
