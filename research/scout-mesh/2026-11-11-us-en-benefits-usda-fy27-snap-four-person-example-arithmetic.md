# USDA FY2027 SNAP eligibility explainer: four-person deduction and worked-example arithmetic

**Observed:** 2026-11-11 UTC. **Scout:** US-English public-benefits information integrity. **Decision:** verified public-editorial discrepancy; human-review-only correction candidate. **Status:** not sent to USDA, not a real benefit calculation, no external correction/impact verified.

## Original primary sources (public)

1. USDA Food and Nutrition Administration, [SNAP Eligibility](https://fns-prod.azureedge.us/snap/recipient/eligibility), updated **2026-11-03** on the page, specifically Tables 2–5 and the four-person calculation example. Canonical public URL: https://www.fna.usda.gov/snap/recipient/eligibility . The official USDA content-delivery mirror was directly read on 2026-11-11.
2. USDA FNA, [FY2027 SNAP Cost-of-Living Adjustment](https://fns-prod.azureedge.us/snap/allotment/cola), updated **2026-11-04** on the page, especially Standard Deductions Table 2 and maximum-allotment Table 1. Canonical public URL: https://www.fna.usda.gov/snap/allotment/cola .
3. USDA FNA, [FY2027 FDPIR net monthly income standards](https://www.fna.usda.gov/fdpir/net-monthly-income-standards), independently publishes **$229** as the SNAP standard deduction for a four-person household in the contiguous US. This cross-reference is not itself the SNAP eligibility authority; the COLA table is.
4. [7 CFR 273.10(e)(1), (e)(2)(ii)](https://www.ecfr.gov/current/title-7/section-273.10), state rounding choices and benefit computation. Do not treat the simplified webpage example as a substitute for an actual state determination.

## Distinct, source-supported discrepancies

**F1 — Wrong standard deduction in the worked example.** The eligibility explainer explicitly models **four people**, but Table 3 subtracts **$217** from $1,750. USDA's **FY2027** COLA table lists **$229 for four people** in the 48 contiguous states/DC; $217 is for one to three people. The explainer's adjacent general deductions bullet correctly says $217 applies to sizes 1–3, making the example internally inconsistent.

**F2 — Separate copy/arithmetic defect.** The same example prints `$1,165 - $114.50 = $1,056.50`. The actual subtraction is **$1,050.50**. Under its own prior steps, the intended starting figure was **$1,171**, and $1,171 − $114.50 does equal $1,056.50. This is an independent transcription error, even if the standard-deduction issue were left unchanged.

**F3 — Derived illustrative allotment differs when FY2027 inputs are used.** The published example yields **$706**, but applying the FY2027 four-person deduction to the same fictional inputs and using the webpage's round-up-30%-of-net method yields **$711**. This is a **$5 illustrative difference**, not evidence that USDA or any state paid a real household $5 too little.

### Reproducible comparison (same fictional facts)

| Step | As published (uses $217) | FY2027 corrected worked example (uses $229) |
|---|---:|---:|
| Gross income | $2,050.00 | $2,050.00 |
| Earned-income deduction, 20% × $1,500 | −$300.00 | −$300.00 |
| Standard deduction for four people | −$217.00 | **−$229.00** |
| Dependent care | −$362.00 | −$362.00 |
| Adjusted income | $1,171.00 | **$1,159.00** |
| Half adjusted income | $585.50 | **$579.50** |
| Shelter expense | $700.00 | $700.00 |
| Excess shelter deduction | $114.50 | **$120.50** |
| Net income | $1,056.50 | **$1,038.50** |
| 30% of net, rounded up to dollar | $317 | **$312** |
| FY2027 four-person maximum allotment | $1,023 | $1,023 |
| Illustrative monthly allotment | **$706** | **$711** |

**Deterministic arithmetic check:** computed both columns independently using the supplied income/deduction facts and integer-dollar ceiling of 30% of net. For the printed F2 expression, $1,165 − $114.50 = $1,050.50, not $1,056.50. All are elementary arithmetic checks, **not an executed state SNAP eligibility engine**.

## Unsent, narrowly scoped editorial correction candidate

> The FY2027 four-person example on the SNAP Eligibility page appears to use the $217 standard deduction applicable to households of one to three, rather than the $229 four-person standard deduction in USDA's FY2027 COLA table. The worked example also prints $1,165 − $114.50 = $1,056.50, although that arithmetic uses $1,171 as the intended starting amount. Could the editorial team reconcile Tables 3 and 5 with the FY2027 four-person deduction and recheck the illustrative net income and allotment? With the currently stated fictional income, care and shelter expenses, the simplified worked example yields $1,038.50 net and a $711 allotment when using $229, subject to the applicable SNAP rounding procedure. Please preserve the caveat that real eligibility and awards are determined by state agencies.

**Do not send** without qualified benefits-policy/editorial review and separate owner authorization.

## Boundaries and next unchecked step

- This is a **federal public-information example defect**, not proof of a flawed benefit system, denied benefits, real underpayment, or an institutional admission.
- State-specific SNAP rounding and deductions may vary under 7 CFR 273.10; the $711 result is an illustrative result following the webpage's own method, not personal eligibility advice.
- Source was retrieved through USDA's official public delivery domain; independent uncached ordinary-browser verification of the canonical `www.fna.usda.gov` domain and any subsequently updated page is still needed.
- **Next by 2026-11-15 UTC:** independently recheck canonical page and COLA table, have a qualified SNAP policy/editorial reviewer validate the replacement example, then seek separate owner approval before any external contact. If already corrected, record the correction date and distinguish it from any causal claim.
- No contact, model-costly Foundry call, AppDeploy deployment/credit-consuming operation, production mutation, new scheduler, private information or synthetic contributor was involved.
