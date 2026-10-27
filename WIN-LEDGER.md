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
