# Scout Mesh | Global / English / science integrity — Retraction Watch metadata export and retraction propagation

**Research completed:** 2026-10-26T04:19:43Z (UTC)  
**Cell:** `global-en-science-integrity`  
**Owner:** Humanity Loop main worker / Scout Owner  
**Disposition:** `no_signal` for a *new, independently actionable intervention*. An existing public defect report has already reached the responsible maintainer.  
**External action:** None. No new report, unsolicited contact, security test, data download or claim of correction.

## Source-reviewed observations

1. **Public defect report, not a finding independently replicated from raw bytes:** On October 21, 2026, a contributor reported that several October 15–20 Retraction Watch CSV exports had changed from UTF-8 to Windows-1252 and replaced some non-Latin characters with question marks. The contributor supplied exact GitLab commit IDs, byte counts and affected-field examples. [Original Crossref community report](https://community.crossref.org/t/retraction-watch-csv-since-15-october-most-daily-files-are-in-windows-1252-and-have-lost-non-latin-characters/16632).
2. **Responsible maintainer already aware:** On October 22, Crossref's Martyn Rittman replied that the encoding should not have changed and that Crossref would investigate its processes and those of Retraction Watch. The accessible public thread showed no subsequent resolution post at this review. **That is not proof the export remains broken today.** [Same primary discussion](https://community.crossref.org/t/retraction-watch-csv-since-15-october-most-daily-files-are-in-windows-1252-and-have-lost-non-latin-characters/16632).
3. **Authoritative data-delivery context:** Crossref's documentation says the Retraction Watch dataset is distributed as a GitLab-hosted CSV updated every working day, and that the REST API provides a distinct retraction-metadata retrieval path. [Crossref Retraction Watch documentation](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/).
4. **Related gap already publicly discussed, not an independent new case:** A separate October 15–23 Crossref community discussion documents that Retraction Watch records without a retraction-notice DOI may not appear as update relationships in Crossref's REST API. Crossref explained the DOI-to-DOI relationship limitation and a contributor reported downstream OpenAlex mismatches; these are **third-party claims/acknowledgements, not measurements reproduced here**. [Existing Crossref discussion](https://community.crossref.org/t/rwdb-record-62686-10-33263-briac94-979986-retraction-recorded-in-retraction-watch-but-absent-from-crossref-metadata/16586).
5. **Deduplication:** Humanity Loop already operates a narrow Crossref/Europe PMC evidence-integrity backup with explicit coverage limitations, and has multiple distinct retracted-study inclusion investigations. No need to duplicate the public Crossref reports or infer that a metadata issue invalidates any study.

## Foresight, alternatives and decision

- **STEEP+ / TIPPO:** Technical metadata encoding and propagation are the observed issues; multilingual scholarly discovery and accurate evidence synthesis are potential affected uses. The established trend is growing dependence on metadata APIs and bulk exports, with a reported regression and an already-active maintainer response.
- **Negative-space check:** A practical unaddressed opportunity would require a current, independently reproduced corrupt export or a documented consumer error despite the maintainer's acknowledged investigation. Neither was established in this bounded review.
- **Existing remedy:** Crossref has accepted the encoding issue for investigation. Consumers can separately validate CSV encoding and avoid treating a missing API retraction flag as definitive proof of no retraction, but no new fix or third-party deployment was verified here.
- **Decision:** `no_signal` — do not contact Crossref or file a duplicate issue. This is a source-reviewed no-action result, not a verified fix, beneficiary outcome or completed external intervention.
- **Falsification/next trigger:** Reconsider only if a later public GitLab export is independently shown to retain lost non-Latin data *after* maintainer remediation, or a distinct reproducible consumer-side defect with a willing maintainer is identified. Do not assert current bytes or causal mechanism without direct data inspection.

**Impact accounting:** One genuine due-cell source review; zero new interventions, corrections, accepted contributions, contributor activations, or verified beneficiary effects.
