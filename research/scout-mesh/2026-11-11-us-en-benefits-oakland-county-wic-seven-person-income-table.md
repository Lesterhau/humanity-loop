# Oakland County 2026–27 WIC income chart: seven-person biweekly discrepancy

**Scout cell:** US-EN public-benefits / external public-information integrity (source-reviewed 2026-11-11 UTC). **Status:** verified difference between two official public documents; **not** a proven incorrect eligibility decision, state processing defect, or agency correction. No external contact.

## Exact primary-source crosswalk

1. Oakland County, Michigan, **June 26, 2026** official news item, "New WIC Income Guidelines Expand Food Assistance for Oakland County Families": https://www.oaklandcountymi.gov/news/2026/06/26/new-wic-income-guidelines-expand-food-assistance-for-oakland-county-families-2462 . Its embedded "Michigan WIC Eligibility Guidelines: 2026-2027" table lists household **7** as **$44.55 hourly / $1,781 weekly / $3,651 biweekly / $7,715 monthly / $92,574 annual**. This is a county *news release*, not evidence that an active applicant-screening system uses these figures.
2. The **Michigan Department of Health and Human Services (MDHHS)** reference sheet, "Michigan Women, Infants, and Children (WIC), Income Eligibility Guidelines 2026–2027," **updated June 1, 2026**, is linked directly from that county news item: https://www.michigan.gov/mdhhs/-/media/Project/Websites/mdhhs/Assistance-Programs/WIC-Media/Ref-Income-Calculation-Reference-sheet.pdf . The household-seven row states **$44.50 hourly / $1,781 weekly / $3,561 biweekly / $7,715 monthly / $92,574 annual**.
3. USDA's official **April 29, 2026** WIC income-eligibility publication, effective **July 1, 2026–June 30, 2027**, lists the seven-person 185%-FPL ceiling for the contiguous states as **$3,561 biweekly**, with the same $1,781 weekly, $7,715 monthly and $92,574 annual figures: https://fns-prod.azureedge.us/wic/fr-042926 . USDA does **not** specify an hourly value in that table; the hourly comparison above is between the county and the MDHHS sheet, not an independently computed federal hourly standard.

| Household seven | Oakland County June 26 release | MDHHS June 1 reference | USDA 2026–27 |
|---|---:|---:|---:|
| Hourly | $44.55 | **$44.50** | Not specified |
| Weekly | $1,781 | $1,781 | $1,781 |
| Biweekly | **$3,651** | **$3,561** | **$3,561** |
| Monthly | $7,715 | $7,715 | $7,715 |
| Annual | $92,574 | $92,574 | $92,574 |

**Difference:** County's biweekly row is **$90 higher** than both state and federal tables; county's hourly figure is **$0.05 higher** than the state reference. All other compared seven-person amounts agree. The county page directly links to the *correct* state sheet, making a county table transcription error plausible. The two dates alone do not establish an intervening policy change.

**Illustrative consequence, not an eligibility determination:** A seven-person household reporting $3,600 gross every two weeks would be under the county news table's displayed $3,651 figure but over the state/USDA $3,561 figure. WIC eligibility also depends on categorical/adjunctive eligibility, residence, nutrition-risk assessment and official income methodology; this illustration cannot establish an actual approval or denial.

## Reproduction and limitations

- The public county HTML, linked MDHHS PDF and USDA 2026–27 guidance were independently retrieved through a public web reader on **2026-11-11**. The county source was published June 26 and the MDHHS source updated June 1. A separate uncached ordinary-user browser check of the live county rendering has **not** been completed.
- A standalone **offline, standard-library-only** JSON income-table comparator is in `runtime/foundry-fallback/wic-income-table-compare.py`. Its self-test checks the two exact household-seven discrepancies, a matching control and a year-mismatch fail-closed condition. It does not scrape, contact agencies, access personal records or decide eligibility.
- No claim is made about how the actual Oakland County/MDHHS intake system computes income or whether a person relied on the news table.

## Human-review-only proposed correction (UNSENT)

> In the June 26, 2026 Oakland County WIC news release, could the seven-person row be checked against the Michigan WIC 2026–27 reference sheet linked in that release? The county table prints **$3,651 biweekly** and **$44.55 hourly**; the linked state sheet prints **$3,561 biweekly** and **$44.50 hourly**, while USDA's effective 2026–27 table confirms **$3,561 biweekly**. If the county values are transcription errors, please correct or annotate the archived release so families are not given conflicting eligibility illustrations. We have not assessed any applicant's eligibility or the county's live intake process.

**Next unchecked by 2026-11-18 UTC:** Independent uncached browser read of the county release and current state guidance; check whether a newer county clarification supersedes the release; obtain qualified Michigan WIC editorial review. Any institutional contact requires separate authorization. Count this as **one source-reviewed Scout finding and review-only correction draft**, not a verified institutional fix, adopted outside contribution or beneficiary outcome.
