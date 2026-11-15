# South Carolina Family Independence: need-standard rounding and $10 payment threshold — source check

Observed 2026-11-15 UTC. Status: **independent primary-source review / unpublished Tier-0 software-quality evidence**, not a corrected upstream defect or actual benefit determination.

## Source evidence
1. South Carolina General Assembly's official [Department of Social Services regulations, Chapter 114](https://www.scstatehouse.gov/coderegs/Chapter%20114.pdf), PDF page 210 (zero-indexed page 209), §114-1140(A)(2)-(6): the need standard is set at 50% of federal poverty guidelines and updated annually following the appropriations act; the ratable reduction determines payment standard; fractional need standard and payment amounts are rounded **down** to whole dollars; application-month proration precedes rounding; no monthly FI assistance is paid when the amount before adjustments is below $10. A unit denied a payment due to this threshold or rounding remains a recipient for other purposes, and a zero-payment month does not count against the time limit.
2. [PolicyEngine/policyengine-us issue #10497](https://github.com/PolicyEngine/policyengine-us/issues/10497), open as observed, identifies South Carolina TANF and Michigan FIP rounding implementation gaps and provides a January 2025 South Carolina two-person hypothetical near the threshold. This is an upstream maintainer's allegation/reproduction, **not** an independent execution of PolicyEngine.
3. Distinct from [New Hampshire FANF #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517): South Carolina explicitly rounds the **need standard as well as the payment**, whereas New Hampshire's FANF rule rounds the computed grant. Do not reuse a single state-agnostic rounding stage.

## Independently checked numerical example
Using the *issue's historical hypothetical* 2025 two-person fractional need standard $851.67, South Carolina's stated rule first yields $851. With countable income $826.80 and issue's illustrative reduction factor 0.4046, the unrounded grant is (851 - 826.80) × 0.4046 = $9.79132, then $9 after flooring; the below-$10 payment rule gives $0. Using $851.67 before flooring would instead produce approximately $10.06, illustrating a potentially material threshold boundary. This arithmetic is an illustration conditional on the historical inputs, not verification of the current state's rate, household eligibility, or an actual paid amount.

## Review-ready checks, not executed
- Confirm 2025 and 2026 ratable factors/payment standards against an authoritative DSS policy manual or contemporaneous state notice before claiming current-dollar outcomes.
- Add fixtures for need-standard floor before subtraction, benefit floor before $10 test, exact $9.99/$10.00 threshold, and application-month **proration before** rounding.
- Add a nonpayment case ensuring zero-payment months are not counted toward the FI time limit, if the relevant model exposes that variable.
- Keep Michigan's BEM 520 case separate; its mixed cents instructions require a distinct source-level interpretation.
- Request qualified reviewer signoff before any upstream patch or outreach. No upstream comment, deployment, paid operation, or institutional contact was made.

**Outcome classification:** verified primary-source implementation requirement and candidate regression coverage; no verified correction, upstream adoption, affected person, or beneficiary effect.
