# Virginia WIC French-language income table: search-index false positive, current source parity (NO SIGNAL)

**Observed:** 2026-11-13 UTC. **Scope:** public-source-only, read-only comparison; no applicant data, outreach, site changes, eligibility decisions or verified beneficiary outcome.

## Why this was checked
A public search result for the Virginia Department of Health's French-language *Nouveaux participants* page surfaced an older indexed snapshot with **2025–26** WIC income limits (one-person monthly $2,413; two-person $3,261; four-person $4,957), apparently conflicting with the English 2026–27 page. Treating that snippet as live evidence would have produced a false public discrepancy report.

## Direct primary-source readback on November 13
1. **VDH French page:** https://vdh.fr.virginia.gov/wic-participants/new-participants/ — direct web-reader open returned the **2026–27** table, effective **June 29, 2026–June 30, 2027**, with monthly limits **$2,461 / $3,337 / $4,212 / $5,088** for households 1–4, and an on-page **November 2, 2026** update label. The observed direct page **does not** show the older 2025 table.
2. **VDH English page:** https://www.vdh.virginia.gov/wic-participants/new-participants/ — direct web-reader open returned the **same** effective dates and monthly limits, with the same November 2 update label.
3. **Independent VDH French district page:** https://vdh.fr.virginia.gov/rappahannock-rapidan/wic/ — directly opened and shows the 2026–27 table with the same figures, supporting current-language parity. This is a separate district page, not proof of every translated VDH page.
4. **USDA WIC 2026–27 notice:** https://www.fna.usda.gov/wic/fr-042926 — published April 29, effective July 1, 2026, lists the same federal 185%-poverty monthly figures. The direct USDA page returned 403 to one reader in this run; its current official search-index text was retrieved, and the VDH English/French original pages were opened directly. Do not call the USDA origin independently opened in this run.

| Household size | Older search-index snapshot (2025–26) | Direct French & English VDH pages (2026–27) |
|---|---:|---:|
| 1 | $2,413 | $2,461 |
| 2 | $3,261 | $3,337 |
| 3 | $4,109 | $4,212 |
| 4 | $4,957 | $5,088 |

## Disposition and limits
**NO SIGNAL / rejected candidate.** The apparent language-access defect is **not reproduced** in the directly opened current French page. The old search snippet is stale relative to the page opened during this review. The exact date the site changed is unknown; the page's November 2 label is not independent proof of when the table was edited. This is a web-reader origin retrieval, **not** an uncached human GUI-browser test; no claim is made about every client or every VDH translation.

**Do not send a correction request, create an alleged VDH defect, or count a resolved institutional case based on this search-index snapshot.** This was not a previously reported Humanity Loop issue, so it is not a report→correction outcome.

**Next step:** Close this candidate as a documented false positive. Reopen only if a dated ordinary-browser capture or new official VDH source contradicts the current 2026–27 table. For future multilingual Scouts, always open the exact translated page before treating an indexed snippet as live.

**Accounting:** One independent source-reviewed negative Scout finding. No formal Supabase Scout Mesh completion receipt, contributor submission, agency contact, correction, applicant benefit, Foundry/AppDeploy credit spend, production mutation, or scheduling change.
