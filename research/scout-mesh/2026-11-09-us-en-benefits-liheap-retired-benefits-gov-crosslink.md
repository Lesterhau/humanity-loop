# US benefits-access Scout: LIHEAP eligibility page still points to retired Benefits.gov (2026-11-09 UTC)

**Classification:** Tier-0 public-source **editorial correction candidate**; `global-en-science-integrity` / US public-service information-access cross-check. **Not a proven broken user-facing link, submitted report, accepted correction, or beneficiary outcome.** No personal data, credentials, accounts, form submission or external contact.

## Specific observation and primary-source comparison

1. **Current ACF LIHEAP Clearinghouse eligibility questionnaire**: https://liheapch.acf.gov/eligible/ . On November 9, 2026, the search engine's **same-day indexed rendering** of this official page includes a "You Might Be Eligible For Other Benefits" section instructing readers to use a "Benefits Finder questionnaire on benefits.gov" and describing "over 1,000 benefits." The separate indexed Cherokee version at https://liheapch.acf.gov/eligible/index-cherokee.php also contains the literal `Benefits Finder` / `benefits.gov` reference. The Cherokee-language content was **not** independently translated or checked for equivalence.
2. **USAGov official replacement announcement**: https://www.usa.gov/blog/2024/10/creating-the-new-benefits-experience-on-usa-gov-and-usagov-en-espanol (published October 1, 2024; page last updated June 9, 2026). GSA explicitly states that Benefits.gov, SSABest.Benefits.gov and GovLoans.gov closed and that the federal benefits discovery role moved to USAGov. It documents a redirect migration for more than 1,500 old pages.
3. **Current official replacement**: https://www.usa.gov/benefit-finder was directly retrieved November 9, 2026. Its current page is titled "Find government benefits and financial help," with 12 category selections and an "Apply selections" control. This is the correct federal destination to consider in a **human-reviewed copy update**; it is not a guaranteed eligibility determination.
4. **Related link-migration check, separate and not established as a failure**: https://www.usa.gov/help-with-energy-bills was directly retrieved and its LIHEAP office-finder link points to the legacy hostname `https://liheapch.acf.hhs.gov/search-tool/`; its disconnection-policy link points to `https://liheapch.acf.hhs.gov/Disconnect/disconnect.htm`. Both fetches from this automated reader timed out/returned 502, but the currently indexed official Clearinghouse has corresponding pages at https://liheapch.acf.gov/search-tool/ and https://liheapch.acf.gov/Disconnect/disconnect.htm. Old-host redirects may work in ordinary browsers; **automated fetch errors are not evidence of a broken public route**.

## Narrow, review-only editorial correction draft (NOT SENT)

For the ACF Clearinghouse page's "Other Benefits" section, replace the legacy `benefits.gov` reference with:

> To explore other federal assistance programs, visit USAGov's [Find government benefits and financial help](https://www.usa.gov/benefit-finder). Browse by category and follow the program's official instructions to check eligibility and apply.

Preserve the adjacent notice that the LIHEAP screening questionnaire is **not an official LIHEAP eligibility or approval decision**. Do not reuse the old claim of "over 1,000 benefits" without a current USAGov source supporting that exact count. A qualified editor should review accessible wording, translated variants, and the actual HTML href.

For USAGov's separate energy-bills page, **only after normal-browser redirect verification**, consider pointing the two LIHEAP references directly to their current `liheapch.acf.gov` URLs to reduce unnecessary redirect dependency. Do not claim users are blocked unless a real browser reproduces the problem.

## Verification gates / uncertainty

- **Verified:** USAGov's 2024 retirement/replacement statement, live textual USAGov benefit-finder destination, live USAGov energy-bills page's two link targets, same-day official LIHEAP page **indexed text** retaining the old name/domain.
- **Not verified:** current LIHEAP origin HTML or hyperlink `href`, ordinary-browser display, old `benefits.gov` redirect behavior, old LIHEAP hostname redirect chain, actual impact on applicants, Cherokee translation, other language versions, program eligibility or agency awareness. Direct LIHEAP pages timed out in this automated reader. An index can lag the live origin.
- **Falsification:** If an ordinary browser shows the LIHEAP page already updated to USAGov, or the indexed text is obsolete, close as **no live correction needed**. If legacy links redirect correctly, label them maintenance candidates rather than broken links.
- **Next unchecked action:** Obtain a dated ordinary-browser screenshot/HTML of https://liheapch.acf.gov/eligible/ and inspect the exact rendered text + link href; separately follow the two USA.gov legacy-host links. If the mismatch is confirmed, obtain human editorial approval for one factual agency contact. No outbound message, public accusation or production change is authorized by this note.

## Receipt / governance

Research completed November 9, 2026 UTC by the existing Humanity Loop coordinator; no Foundry/AppDeploy model calls, credit-consuming operations, deployments, independent contributor claims, external submissions or outreach. This is **one source-reviewed external public-information correction candidate**, not a report-to-correction win or verified public benefit.
