# District of Columbia SNAP FY2027: internally inconsistent public eligibility guidance

**Review date:** 2026-11-10 UTC. **Cell:** `us-en-benefits`. **Status:** verified public-page editorial discrepancies; **UNSENT** correction recommendation. **Risk:** Tier 0, ordinary public-source reading only. No application, agency contact, account access, or eligibility decision.

## Original public sources checked

1. District of Columbia Department of Human Services (DHS), [SNAP Eligibility Requirements](https://dhs.dc.gov/service/snap-eligibility-requirements), publicly retrieved November 10, 2026. The page's main table is explicitly effective **October 1, 2026–September 30, 2027**, while some prose farther down retains older amounts.
2. USDA Food and Nutrition Administration, [FY2027 SNAP Cost-of-Living Adjustment tables](https://fns-prod.azureedge.us/snap/allotment/cola), publicly retrieved November 10, 2026, effective October 1, 2026–September 30, 2027. The tables expressly include the District of Columbia.
3. USDA, [Broad-Based Categorical Eligibility chart](https://fns-prod.azureedge.us/snap/broad-based-categorical-eligibility), updated June 29, 2026, publicly retrieved November 10. District of Columbia row says **200% gross income** and no asset limit for the qualifying TANF/MOE program.

## Reproducible findings

### A. The 200%-FPL column is mislabeled as NET income

The DC DHS general-eligibility table calls its second income column **“Maximum Net Monthly Income (200% FPL)”**, with $2,660 for one person and $5,500 for four. Immediately below the table, the footnote calls this **“200% FPL Gross income standard”** for expanded categorical eligibility. USDA's DC BBCE entry likewise calls the 200% threshold **gross income**. The page itself defines gross and net differently. **Correction candidate:** change only that column heading to “Maximum Gross Monthly Income (200% FPL; expanded categorical eligibility)” and retain the qualification/footnote. Do not imply everyone below this gross threshold is automatically approved; nonfinancial rules and benefit calculation still apply.

### B. The general-eligibility deduction paragraph retains amounts inconsistent with FY2027

| Item | DC DHS general section | USDA FY2027 DC standard | DC DHS elderly/disabled section |
|---|---:|---:|---:|
| Standard deduction, household size 1–3 | $204 | **$217** | $217 |
| Standard deduction, size 5 | $254 | **$268** | $268 |
| Standard deduction, size 6+ | $291 | **$308** | $308 |
| Maximum excess shelter deduction | $712 | **$769** | $769 |

These differences occur **within the same DC DHS page**: its elderly/disabled section contains the newer federal numbers, but the general section still displays older ones. The USDA FY2027 table additionally specifies **$229 for a four-person standard deduction**; the general paragraph does not explicitly give a four-person amount. **Correction candidate:** harmonize general deductions to FY2027 and include the size-four value to avoid ambiguity, while preserving applicable exceptions.

### C. Asset-limit discrepancy requires editorial confirmation

The general DC DHS section lists **$4,500** for households with an elderly/disabled member when a resource test applies. The same page's elderly/disabled section lists **$4,700**. USDA's FY2027 maximum asset limit is **$4,750** (and $3,000 otherwise). This is a three-way inconsistency. **Candidate:** verify controlling DC policy and any applicable state-specific eligibility rules before changing this line; do not assume federal limits determine all categorically eligible cases.

## Interpretation and limitations

The page's **FY2027 income rows and the separate SNAP Monthly Benefit page** are already updated; this is **not** a claim that all DC SNAP guidance is stale. The issue concerns the **misnamed 200%-gross column** and **older deduction/resource figures embedded in otherwise current guidance**. A public text reader showed the contradictions; an ordinary browser/mobile rendering and the exact page edit history were not independently captured. No evidence was collected of incorrect DHS eligibility calculations, applicant denial, benefit underpayment, or agency acknowledgement. The District's BBCE program has distinct criteria; do not substitute federal regular-income tests for categorical eligibility.

## Unsent, human-reviewable editorial suggestion

“On your current SNAP Eligibility Requirements page, could the 200%-FPL income column be labeled *gross* rather than *net*, consistent with the footnote and USDA BBCE chart? The general-eligibility deduction paragraph also lists $204/$254/$291 and $712, while the page's elderly/disabled section and USDA FY2027 tables list $217/$268/$308 and $769. The page shows $4,500 and $4,700 for the elderly/disabled resource limit in different sections, compared with USDA's $4,750 FY2027 figure. Please verify controlling DC policy and harmonize the public-facing text. No case-processing error is alleged.”

**Next unchecked:** independent ordinary-browser/mobile and qualified benefits-editorial verification, then separate owner approval before any DC DHS contact. **Review target:** November 17, 2026 UTC.

## Scout classification

- **Signal:** documented public-information inconsistency; not a proven agency processing defect.
- **STEEP+:** Social / Economic / Policy-Legal / Equity / public-service information integrity.
- **TIPPO:** transparency and public-policy implementation; potential eligibility self-screening confusion.
- **Three Horizons:** H1, maintain accurate existing benefit-access guidance.
- **Futures Triangle:** push = annual federal COLA changes; pull = clear applicant self-service; weight = partially updated agency pages.
- **Cross-impact:** mistaken gross/net terminology could confuse self-screening; actual behavior/outcomes unknown.
- **Heuristic novelty 0.35; usefulness 0.75; evidence quality 0.92; interpretation uncertainty 0.18.** These are triage estimates, not measurements.
- **Existing solutions:** the agency already has a current FY2027 benefit page and a partly updated eligibility page; targeted editorial correction is lower-cost than a new calculator.
- **Falsification:** ordinary-browser view does not display these labels/amounts, a dated authoritative DC policy supersedes the federal comparison, or a verified page revision removes the inconsistencies.
- **Escalation:** human editorial review only; no external sending without owner authorization.

**Impact accounting:** one independent AI-assisted public-source review and public-safe evidence artifact; **zero verified outside submissions, corrections, beneficiaries, human service hours, or agency contact**. No AppDeploy Foundry inference, deployment, paid API, production mutation or scheduling changes.
