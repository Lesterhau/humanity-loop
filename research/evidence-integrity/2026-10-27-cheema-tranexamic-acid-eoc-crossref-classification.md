# Evidence Integrity — Cheema 2023 tranexamic-acid review: expression of concern, not a verified retraction

**Source review:** 2026-10-27 UTC. **Owner:** Humanity Loop Evidence Integrity / main worker.  
**Decision:** `triaged_expression_of_concern_retraction_unverified` for nine *citation candidates*.  
**Public-outcome status:** No editorial correction attributable to Humanity Loop, no external outreach, no clinical or beneficiary effect.

## Trigger and precise discrepancy

The [2026-10-27 23:05:25Z backup receipt](../../runtime/evidence-integrity-backup/latest.json) lists nine Europe PMC citation records associated with DOI `10.1016/j.ajogmf.2023.101049`. The scanner found the DOI via Crossref's `update-type:retraction` filter and recorded `retractedDoi` and `noticeDoi` as the **same DOI**. That is a metadata triage signal, **not independently verified evidence of a retraction**.

Independent article-status sources establish a more limited state:

1. **Original article:** Cheema et al., *Tranexamic acid for the prevention of blood loss after cesarean section: an updated systematic review and meta-analysis of randomized controlled trials*, *AJOG MFM* (2023), DOI `10.1016/j.ajogmf.2023.101049`, PMID 37311484. PubMed continues to list it as a meta-analysis/systematic review. [PubMed original](https://pubmed.ncbi.nlm.nih.gov/37311484/) · [Publisher original](https://doi.org/10.1016/j.ajogmf.2023.101049).
2. **Erratum:** Cheema et al., *Erratum to ...*, published December 2023, DOI `10.1016/j.ajogmf.2023.101196`, PMID 37891123. An erratum is not automatically a retraction. [PubMed erratum](https://pubmed.ncbi.nlm.nih.gov/37891123/).
3. **Expression of concern:** *Expression of concern "Tranexamic acid for the prevention of blood loss after cesarean section..."*, dated July 20, 2026 online / September 2026 issue, DOI `10.1016/j.ajogmf.2026.102065`, PMID 42637285. PubMed explicitly classifies the notice as **Expression of Concern** and links it to the 2023 original. [PubMed notice](https://pubmed.ncbi.nlm.nih.gov/42637285/).

**Conclusion:** A publisher expression of concern is independently verified. A subsequent formal retraction of this specific article was **not established** in this review. Do not label it a retracted study, do not treat Crossref's relationship alone as dispositive, and do not assert that downstream reviews are invalid. The expression of concern is material context for evaluating downstream reliance, but this bounded review did **not** inspect each citing review's full text or reanalyze clinical results.

## Nine citation leads retained for audit, not promoted to impact claims

Europe PMC returned these citing records (PMIDs), all still requiring source-level context review if a publisher-status change makes one consequential:

| PMID | Citation title (shortened only for table) |
|---|---|
| 42564916 | Tranexamic acid in radical cystectomy: systematic review and meta-analysis |
| 42355800 | Prophylactic use in high-risk cesarean deliveries: systematic review |
| 41066405 | Prophylactic tranexamic acid in high-risk cesarean delivery: RCT review |
| 40891871 | Tranexamic acid in external dacryocystorhinostomy: systematic review |
| 40712613 | Prophylactic strategies for postpartum hemorrhage: Bayesian network meta-analysis |
| 40406479 | Tranexamic acid in gynecology and obstetrics: umbrella review |
| 39082365 | Prophylactic tranexamic acid in cesarean section: systematic review |
| 37928456 | Prehospital tranexamic acid in trauma patients: systematic review |
| 37601311 | Tranexamic acid for prevention of postpartum bleeding: review protocol |

**Limits:** Europe PMC citation metadata supports a bibliographic relationship, not a finding that the 2023 review's pooled estimates were reused, nor that the nine citing publications included a retracted trial. The 2023 paper is itself a systematic review, not one of its 50 underlying RCTs.

## Next action, uncertainty and closure

- **Review gate:** 2026-11-10, or earlier only on a substantive publisher/PubMed status change.
- **Owner:** Humanity Loop Evidence Integrity main worker.
- **Action:** Check whether the publisher has issued a formal retraction, updated the expression of concern, or clarified the Crossref relation. If a retraction is independently verified, separately review the exact dependence of any high-priority citing article before considering a neutral, human-reviewed editorial inquiry.
- **Falsification:** A verifiable publisher retraction notice would overturn today's 'retraction unverified' classification. Conversely, an official metadata correction could explain the Crossref mismatch.
- **No outreach:** No journal/author/clinical contact, public accusation, advice about tranexamic-acid treatment, or automatic warnings.
- **Operational insight:** The restored detector can surface valuable leads, but source-level notice-type verification is essential before using the word 'retracted'. A green GitHub workflow and a Crossref metadata relation are not evidence of clinical impact.

**Outcome accounting:** one independently source-reviewed notice-type classification, nine queue records retained, zero verified clinical outcomes.
