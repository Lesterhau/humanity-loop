# Scout Mesh — Global / English / Science integrity: retraction-metadata resilience

**Review completed:** 2026-10-31 07:44 UTC (source review; not a claimed autonomous specialist run)  
**Cell:** `global-en-science-integrity`  
**Decision:** `no_signal` — documented external defect and partial recovery, no newly unreported actionable gap independently established  
**Owner:** Humanity Loop main worker / Scout Owner  
**Risk:** Tier 0 read-only review; no external outreach, no author allegation, no medical recommendation.

## INTEND / scope
Review a genuinely due completion-based Scout cell. Test whether October 2026 changes to open retraction metadata create a *new*, specific, independently supportable intervention not already owned by Crossref, Retraction Watch, or other maintainers. Record a bounded no-signal result rather than duplicate existing reports.

## Primary-source findings (retrieved October 31, 2026)
1. Crossref's official Retraction Watch documentation states the open database is updated each working day, is accessible as a GitLab CSV and through the Crossref REST API, and contains correction and expression-of-concern records with less comprehensive coverage than retractions. Source: https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/
2. A public Crossref support thread opened **October 21** documents that some daily CSV exports since October 15 were Windows-1252 and had lost non-Latin text. The original reporter quantified potential damage and named affected scripts; these are **the reporter's measurements**, not independently replicated by Humanity Loop. On **October 26**, the reporter checked October 22–23 exports and observed UTF-8 and restored Cyrillic/Chinese names. On **October 29**, Crossref staff explicitly said upstream data-delivery changes **had been reverted**, with robust ingestion a future roadmap item. Source: https://community.crossref.org/t/retraction-watch-csv-since-15-october-most-daily-files-are-in-windows-1252-and-have-lost-non-latin-characters/16632
3. A separate Crossref thread dated **October 15–24** documents a known limitation: Retraction Watch records without a separate retraction-notice DOI may not surface as retraction relationships in Crossref. Staff explicitly acknowledged the design limitation, explained the two-DOI linkage rule, and stated no current plan to import notice-less Retraction Watch rows as self-referential updates. A third-party citation tool developer publicly described implementing a CSV-based fallback on October 24. Claims about the number of affected records in the thread have multiple corrections and **were not independently reproduced** here. Source: https://community.crossref.org/t/rwdb-record-62686-10-33263-briac94-979986-retraction-recorded-in-retraction-watch-but-absent-from-crossref-metadata/16586
4. Crossref's May 29, 2026 deprecation notice says the experimental Labs API stopped receiving new Retraction Watch annotations, directing consumers to the production API or GitLab dataset. Source: https://community.crossref.org/t/deprecating-retraction-watch-annotations-in-the-labs-api/15884

## Novelty / existing-solution check
**No newly unreported incident identified.** The encoding incident was reported by another researcher, acknowledged by staff and described as reverted; a fresh byte-level test of the latest ~68MB CSV was **not** completed in this run, so no independently verified current-file recovery claim is made. The missing-notice-DOI problem is already under active public discussion with a documented upstream policy rationale and at least one downstream fallback. Do not claim Humanity Loop flagged or caused either change.

**Practical defensible insight:** Any future Humanity Loop reference-integrity consumer should not infer `not retracted` solely from an empty Crossref `update-to` field; provenance-aware checks against the Retraction Watch dataset and the publisher's current article page may be needed. This is a design caution, **not** a verified new correction or proof that any specific paper is invalid.

## STEEP+ / foresight
- **T:** Encoding/format drift can silently degrade global metadata and downstream alerts.
- **S/V:** Non-Latin scholarship bears disproportionate discoverability and name-integrity risks.
- **E:** Publicly available datasets lower the cost of cross-checks; duplicate ingestion work remains a cost.
- **P/L:** Editorial responsibility and correction practices differ across publishers; do not infer misconduct from missing metadata.
- **TIPPO:** Trend: more open correction feeds. Obstacle: heterogeneous notice identifiers and exports. Plan: maintainers' more robust ingestion roadmap. 
- **Three horizons:** H1 maintain CSV/API integrity; H2 provenance-aware downstream checks; H3 interoperable correction relationships.
- **Falsification / escalation:** Reopen only if a *fresh*, independently reproduced UTF-8 regression or an unreported specific record-level mismatch is found, or a maintainer explicitly requests an outside contribution.

## Outcome and next action
**No new signal, agency contact, code change, correction attributable to Humanity Loop, contributor activity or beneficiary outcome.** The relevant maintainers and external reporters deserve credit. Do not post to the Crossref forum automatically; its staff have discussed AI-agent participation restrictions. Next ordinary review only on a new authoritative incident, maintainer invitation or documented downstream defect. This source review does not replace issue #25's separate November 6 editorial-data gate.
