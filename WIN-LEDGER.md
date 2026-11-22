# Humanity Loop Win Ledger

This ledger records **completed, independently verified real-world wins**.

A win is not:
- an email sent;
- a bug report filed;
- an app deployed;
- an agency saying "we'll look at it";
- an agent producing a promising draft.

A win requires a verified outcome such as:
- public guidance corrected;
- a defect fixed and shipped;
- a harmful/inaccessible process changed;
- an intervention adopted;
- a useful tool measurably used;
- an external organization implements a recommendation;
- a project produces a validated benefit.

## Win record

Each win should include:
- Win ID
- source Outcome Tracker item
- problem
- Humanity Loop action
- external actor(s)
- verified change
- evidence / receipt
- people or systems helped
- date verified
- attribution confidence
- follow-on monitoring if needed
- public MOTHER post status

## MOTHER signal

When an Outcome Tracker item changes to **resolved** or **partially resolved with verified material benefit**, the Outcome Tracker should emit a Win Event.

The MOTHER/Public Transparency Agent should:
1. check that the outcome is actually verified;
2. draft a celebration post;
3. credit the people/institution who made the fix;
4. link receipts;
5. invite people to #AddANode / #HelpWanted where relevant;
6. avoid exaggerating Humanity Loop's causal contribution.

Wins are evidence that the loop works and should be communicated accordingly.

---

## WIN-001 — Texas HHS corrected Medicaid Buy-In premium range
- **Source Outcome Tracker item:** OT-001
- **Problem:** Texas HHS Appendix XXXI listed the 150%–185% FPL earned-income premium range as beginning above $41,995, an impossible lower bound inconsistent with the preceding $1,995 ceiling.
- **Humanity Loop action:** Identified the contradiction and reported it to the Texas HHS Form and Handbook Unit on 2026-09-25.
- **External actor:** Texas Health and Human Services — Form and Handbook Unit.
- **Verified change:** On 2026-09-30 the unit replied that the error was corrected. Independent verification of the live page confirmed the range now reads “More than $1,995 up to and including $2,461.”
- **Evidence / receipt:** https://fhb.hhs.texas.gov/handbooks/medicaid-elderly-people-disabilities-handbook/appendix-xxxi-budget-reference-chart
- **People/systems helped:** Medicaid Buy-In applicants, eligibility workers, advocates, and anyone using the current MEPD handbook premium chart.
- **Date verified:** 2026-09-30
- **Attribution confidence:** high for contribution to detection/reporting; the agency implemented the correction.
- **Follow-on monitoring:** watch for regression at future annual FPL updates.
- **MOTHER post status:** candidate — not yet posted.


## WIN-002 — VA corrected Spanish-index links to current 2026 benefits-rate tables
- **Source Outcome Tracker item:** OT-002.
- **Problem:** The Veterans Benefits Administration's Spanish `Tasas Actuales` index labeled rate links as current, but Veterans compensation and DIC destinations still showed 2019 effective dates; the Parents DIC link also routed to a generic pension page at the October 20 check.
- **Humanity Loop action:** Reported the precise mismatch to VA on 2026-09-25, followed by a bounded new-evidence update on 2026-10-20 after the defect remained visible. No new outreach during verification.
- **External actor:** U.S. Department of Veterans Affairs / Veterans Benefits Administration web publishers.
- **Verified change:** On 2026-10-27, independent live navigation from the [original Spanish index](https://www.benefits.va.gov/Benefits/espanol/compensation_rates-index.asp) reached the VA.gov **2026** rate tables for Veterans compensation, SMC, survivor DIC and Parents DIC, effective December 1, 2025. The index displays a last-updated date of October 22, 2026; the precise time and cause of the change are unverified.
- **Evidence / receipt:** [Source-checked before/report/after case record](runtime/case-steward/ot002-2026-10-27-va-spanish-rates-corrected.md) with four official destination URLs and historical reports in [OT-002](OUTCOME-TRACKER.md).
- **People/systems helped:** The Spanish-language navigation path no longer directs readers of these four labels to the observed stale 2019 rates. Actual visitor usage and downstream benefits have not been measured; linked rate tables are in English, so full Spanish-language accessibility remains unverified.
- **Date verified:** 2026-10-27.
- **Attribution confidence:** High for the documented **report → subsequently verified correction** sequence. **No evidence of exclusive causation or agency credit to Humanity Loop.** The VA deserves credit for implementing the fix. Public wording: “We flagged this issue; it was subsequently corrected.”
- **Follow-on monitoring:** No routine follow-up; reopen on verified regression or a separately scoped new issue.
- **MOTHER post status:** Human-review candidate only; no automatic publication.


## WIN-003 — CMS corrected Medicare Prescription Payment Plan helper income limits
- **Source Outcome Tracker item:** OT-008.
- **Problem:** On 2026-09-19, the live Medicare.gov payment-plan decision helper asked whether an individual's annual income was below $22,590 (single) / $30,660 (married), the prior thresholds, while presenting other 2026 Medicare figures.
- **Humanity Loop action:** Sent a specific factual correction request to CMS Beneficiary Advocacy on 2026-09-19, identifying the page, obsolete thresholds and 2026 comparison values.
- **External actor:** Centers for Medicare & Medicaid Services (CMS), Medicare.gov publishing team.
- **Verified change:** The public helper now shows the 2026 income figures of $23,940 (single) / $32,460 (married). CMS's Medicare Ombudsman Group explicitly confirmed in dated 2026-10-29 correspondence that the page information was updated on 2026-09-30 and acknowledged the report's role.
- **Public verification:** https://www.medicare.gov/prescription-payment-plan/will-this-help-me (checked 2026-11-01); original report and CMS response were independently retrieved from authorized historical correspondence. The private email and attached letter are **not published**.
- **Date independently verified:** 2026-11-01.
- **Attribution confidence:** Direct agency acknowledgment of the report's contribution, stronger than a mere report-followed-by-correction temporal sequence. No exclusive causation or beneficiary usage quantity claimed.
- **People/systems potentially helped:** Medicare beneficiaries using the payment-plan helper, especially those near the outdated income cutoffs. Actual usage and downstream decisions have not been measured.
- **MOTHER post status:** Owner review required; no automatic publication of private correspondence.

## WIN-004 — IRS corrected tax-year-2025 EITC amounts in six translated public guidance pages
- **Source Outcome Tracker item:** OT-005 (**partial case outcome**, not whole-case closure).
- **Problem:** On September 18, 2026, the six translated IRS `Refundable tax credits` pages for Spanish, simplified/traditional Chinese, Korean, Vietnamese and Haitian Creole still displayed tax-year-2024 EITC thresholds while the English page and IRS table had 2025 values. The wrong figures included a **$11,600** investment-income ceiling versus **$11,950** for 2025 and 2024 income endpoints. The EITC partner outreach page separately labeled 2025 but showed the old `$11,600` amount and said **one in four** instead of the contemporary **one in five** unclaimed-credit estimate.
- **Humanity Loop action:** Identified and reported the exact IRS URLs and differing thresholds on **2026-09-18**, as verified by re-reading the contemporaneous original sent institutional correspondence (kept private).
- **External actor:** Internal Revenue Service, taxpayer guidance and multilingual web-content publishers. **No agency acknowledgment of Humanity Loop's report was located.**
- **Verified change:** The [2026-11-07 independent IRS-page check](runtime/case-steward/ot005-2026-11-07-irs-eitc-multilingual-correction-reconciliation.md) verified that all six pages now displayed the correct **2025** investment ceiling `$11,950`, EITC endpoints `$19,104–$68,675`, and child credit `$2,200`. Those same 2025 figures were independently rechecked on all six official `irs.gov` pages on **2026-11-22**. The outreach page also changed to **one in five**; by November 22 its numeric section had already advanced to tax-year-2026 `$12,200` rather than retaining the formerly corrected 2025 example.
- **Evidence / receipt:** [September report and November 7→22 source reconciliation](runtime/case-steward/ot005-2026-11-22-irs-outcome-adjudication.md) (public-safe), including original [IRS Spanish](https://www.irs.gov/es/credits-deductions/individuals/refundable-tax-credits), [simplified Chinese](https://www.irs.gov/zh-hans/credits-deductions/individuals/refundable-tax-credits), [traditional Chinese](https://www.irs.gov/zh-hant/credits-deductions/individuals/refundable-tax-credits), [Korean](https://www.irs.gov/ko/credits-deductions/individuals/refundable-tax-credits), [Vietnamese](https://www.irs.gov/vi/credits-deductions/individuals/refundable-tax-credits), and [Haitian Creole](https://www.irs.gov/ht/credits-deductions/individuals/refundable-tax-credits) public pages.
- **Date independently verified:** **2026-11-07** (first documented corrected state), **2026-11-22** (fresh six-language confirmation). The exact IRS publication/edit date is unknown.
- **Attribution confidence:** **Low / unproven causation.** A contemporaneous report preceded an independently verified agency correction, but the IRS did not acknowledge or attribute its change to Humanity Loop. Appropriate claim: **“We reported outdated 2025 IRS EITC guidance; those public pages were subsequently updated by the IRS.”** Neither exclusive causation nor taxpayer reliance should be suggested.
- **Potential public benefit:** Better-aligned 2025 eligibility information across six language routes; no evidence of actual reader decisions, dollars recovered or how many people accessed it.
- **Scope limitations:** This is **ONE** correction across six language variants, not six wins. Separate OT-005 EITC prior-year list and CP27 mailing instructions remain unresolved. By November 22 English IRS guidance had already advanced to 2026 while the translations remained on explicitly 2025 figures; that new cross-year difference is **unadjudicated**, not proof of a repeat correction or defect.
- **Follow-on monitoring:** Compare tax-year labeling and numeric parity on next targeted IRS update, rather than assuming all-year multilingual synchronization.
- **MOTHER post status:** Candidate only; external publication requires separate review, no automatic announcement.
