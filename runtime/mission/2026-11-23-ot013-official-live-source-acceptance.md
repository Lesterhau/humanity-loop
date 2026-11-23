# G3 live official-source acquisition — OT-013 Pakistan
**One-shot date:** 2026-11-23 00:16 UTC (Nov 22 U.S. Central).  
**Executor:** GitHub Actions repository-native public runner, no external participant or model.  
**Case:** OT-013; **source:** https://city.lums.edu.pk/what-we-do/city-research/dare-rc/  
**Provenance:** [CI run #45087747120](https://github.com/Lesterhau/humanity-loop/actions/runs/45087747120), job `137410104671`, ephemeral three-day [source-snapshot artifact](https://github.com/Lesterhau/humanity-loop/actions/runs/45087747120/artifacts/14779857530).

## INTEND → EXECUTE → VERIFY → RECORD
- **INTEND:** demonstrate a real G3 official-source acquisition (not merely an operator-entered source snippet) while G2 waits for its external respondents. One bounded GET; the approved case/locale/source URL are hard-coded, same as reviewed manifest, with DNS/TLS validation, no redirects, no private IP resolution, no proxy, no cookies and no credentials.
- **EXECUTE:** temporary, uniquely PR #108-scoped GitHub CI acceptance step called `scripts/public_source_snapshot.py --case OT-013 --task foundry-lite/fixtures/ot013-pk-climate-review.json --allow-live-get`. The runner completed successfully, performed a single official HTTPS GET, no scheduled task and zero paid AI/AppDeploy calls.
- **VERIFY:** GitHub returned `success` for the actual one-off step and archived a one-page JSON result. The archived ZIP was downloaded via the GitHub connector and its embedded JSON was **independently inspected**, rather than accepting the workflow log alone.
- **RECORD:** response `HTTP 200`, `text/html`, `95,675` raw bytes, `12,845` normalized visible-text characters. Exact raw-body SHA-256: `5d6ec6ba6dd7e1eadcab550c040249aa049aacef20fcbdca756c52a470878a95`. Snapshot timestamp `2026-11-23T00:16:07.103715Z`. The digest fingerprints the raw HTML **as retrieved by this one runner**; it does not authenticate the underlying research dataset or prove the site never changed.
- **Relevant source findings:** `103 (0.2%)` compounding-high-risk statistic, `84 of the 117 schools`, displayed `81.6%`, and `117` in the district chart text were all matched in normalized public HTML. The calculator derived `84/117 = 71.8%` to one decimal, not the displayed 81.6. Separately accessing the same original public source via public web retrieval corroborated these *displayed text facts* in the same timeframe.
- **Scope boundary:** which of 103/117 is the correct underlying cohort remains **unknown**; no underlying school-level dataset audit, academic methodology review, qualified Pakistan-domain adjudication or direct institution correction occurred. The result is a **source-acquisition and arithmetic candidate**, `independently_reviewed=false`, `eligible_for_win_ledger=false`. No win, global adoption or case-cycle completion claimed.

## Next release-relevant step

The durable artifact proves **one instance of reproducible source acquisition**, not G3 model execution or canonical lease and spending guarantees. Keep the normal CI network-free; after validating the temporary acceptance result, remove the PR-specific live-fetch step before merge. Retain a strictly **manual** `workflow_dispatch` source recheck with explicit operator opt-in. Never auto-poll this institution, which has already received a bounded source-specific follow-up.

**Existing requirements still OPEN:** genuine eight-role model-produced artifact and independent review, exact provider spend control, canonical single-writer lease across hosts, and eventual verified correction outside the United States for G4.
