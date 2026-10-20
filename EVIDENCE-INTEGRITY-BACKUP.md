# Evidence Integrity: no-credit backup (GitHub)

## Purpose and limits

The existing AppDeploy Evidence Integrity Sentinel website remains deployed, but its scheduled background job was disabled October 20, 2026 when the free-plan credits were exhausted. This **separate** GitHub Actions backup checks public Crossref retraction metadata and Europe PMC citation relationships without requiring AppDeploy credits or a private API key.

It detects **possible** downstream reuse of retracted articles in reviews, meta-analyses or clinical-guidance records. **It does not establish** that a guideline is scientifically invalid, that a paper must be retracted, or that someone acted improperly. Do not send complaints or warnings automatically. Any consequential finding requires manual confirmation of the original retraction, the exact citation context, publication status and scope.

## Where to click

1. [Evidence Integrity backup runs](https://github.com/Lesterhau/humanity-loop/actions/workflows/evidence-integrity-backup.yml) — green check means workflow finished, **not** that every public source was accessible.
2. [Latest saved report](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/evidence-integrity-backup/latest.json) — check `status`, `runAt`, `failuresCount`, `candidateFindingsCount`. Read every candidate's `status: unreviewed` literally.
3. [State file](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/evidence-integrity-backup/state.json) — public scholarly DOIs and deduplication keys; the scanner saves a DOI only after its Europe PMC lookup succeeds.
4. [Source code](https://github.com/Lesterhau/humanity-loop/blob/main/scripts/evidence_integrity_backup.py) and [offline tests](https://github.com/Lesterhau/humanity-loop/blob/main/scripts/test_evidence_integrity_backup.py).

## Coverage and reliability limitations

- Each execution queries the newest **25 Crossref retraction notices** and processes up to **15 new retracted article DOIs**.
- Europe PMC search is limited to articles indexed there; citation listing is capped at **1,000 citations per DOI**. When a result appears truncated, the DOI is **not** marked fully checked and will be eligible for retry. No false claim of complete literature coverage.
- Publications with no Europe PMC match are retried; their absence is **not** a negative safety finding.
- A completed DOI is deduplicated across runs; this means new citations appearing **later** for a previously handled retraction are not systematically rechecked. A future sliding-window rescan and cursor pagination would improve coverage.
- The GitHub backup stores public metadata in GitHub only. It **does not sync** the existing AppDeploy database, findings history or user interface. Do not claim two systems are interchangeable, and do not automatically reenable AppDeploy after credits reset.
- GitHub scheduled actions may execute late or skip a window; a green workflow status alone is not a reliable SLA. Use actual `runAt` from saved receipts.
- Failed Crossref or Europe PMC requests produce `failures` in the receipt. Partial results remain explicitly partial; failed DOIs aren't silently marked complete.
- Requests are rate-limited by sequential processing, fixed per-run limits and 25-second network timeouts; avoid frequent manual re-runs.

## Operating decision

This is a low-cost, read-only backup, not a cutover of the native app. The first live run, its offline tests, external source responses and canonical receipt must be verified before the system is described as restored.

When AppDeploy credits replenish, inspect [P1 outage issue #16](https://github.com/Lesterhau/humanity-loop/issues/16). Reconcile one owner, data histories and deduplication before enabling duplicate scanners.

## External reference sources
- Crossref official retraction metadata: https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/
- Europe PMC citations REST API: https://europepmc.org/RestfulWebService
