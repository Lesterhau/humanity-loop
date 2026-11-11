# New Hampshire FANF — floating-point boundary regression in review-only candidates

**Observed:** 2026-11-11 UTC. **Status:** review-only safety finding; no upstream submission, no installed PolicyEngine test, no benefit determination.

## Primary sources and provenance

- **Governing rule:** [New Hampshire He-W 670.03(b)(1)–(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html), independently retrieved November 11. The FANF pre-adjustment grant is the payment standard minus net income, fractional dollars are rounded **down** to a whole dollar, and a pre-adjustment grant below **$10** is not paid. Subsection (b)(6) concerns separate later adjustments.
- **Upstream source:** [PolicyEngine-US `nh_fanf.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py), blob `96399f64ab4e3895630a24609be298d75150a972`, retains an unrounded `min_(max_(payment_standard - countable_income, 0), payment_standard)`.
- **Original upstream discovery:** [PolicyEngine issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517), opened October 27, identifies the grant-rounding/$10-minimum omission. **Humanity Loop did not discover the original upstream defect.**
- **Our two earlier review-only implementations disagree:** [November 9 patch](2026-11-09-policyengine-nh-fanf-rounding-minimum-review.patch) uses `np.floor(np.round(capped_benefit, 2))`, while [the local pilot](../../pilots/policyengine-nh-fanf/nh_fanf.py) and [November 10 challenge](2026-11-10-policyengine-nh-fanf-source-formula-boundary-challenge.md) favor `np.floor(capped_benefit)`.

## New independently executed finding

**Direct floating-point floor can understate a mathematically whole-dollar grant, even when both inputs are ordinary two-decimal dollar amounts.** Example: in Python/NumPy binary floats, `1129.61 - 211.61` evaluates to approximately `917.9999999999999`, and `np.floor` produces **917** instead of the exact-decimal **918**. Other reproduced examples: `2453.66 - 1048.66` gives 1404 rather than 1405, and `2067.47 - 1318.47` gives 748 rather than 749. These are synthetic numerical examples, not actual NH benefit records.

Conversely, the earlier `np.round(..., 2)` approach can incorrectly **increase** a grant when sub-cent intermediate values are considered valid: a raw 9.999 rounds to 10.00 and would be paid instead of suppressed; 10.999 rounds to 11 rather than 10. **Whether the PolicyEngine FANF income pipeline can legitimately produce such sub-cent amounts remains unverified.** The regulation's dollar/cents language does not itself establish the software's intermediate-precision convention.

### Reproducible numerical experiment

[Standalone NumPy/Decimal regression](2026-11-11-nh-fanf-precision-boundary-regression.py) was executed locally under Python 3.13 and NumPy. Seed `20261111`, 100,000 independent synthetic integer-unit pairs per input precision (two, three, and four decimal places), standards below $3,000, including 500 synthetic negative-income stress cases per group. The oracle computes in integer units before flooring, avoiding binary-float cancellation.

| Input precision | Direct `floor` mismatches | Round to cents then `floor` mismatches | Round to 9 decimals then `floor` mismatches |
|---|---:|---:|---:|
| 2 decimal places | 46 / 100,000 | 0 | 0 |
| 3 decimal places | 9 / 100,000 | 263 | 0 |
| 4 decimal places | 1 / 100,000 | 253 | 0 |

Ten hand-selected boundary examples also matched the Decimal oracle with the **provisional** `np.floor(np.round(capped_benefit, 9))` strategy. This is a **numerical tolerance candidate, not an approved policy implementation**. A true value within 0.0000000005 of a whole-dollar threshold could be changed by nine-decimal rounding; no universal correctness or valid input precision is proven. A principled integer-unit/Decimal implementation, upstream money-precision convention or validated tolerance policy may be preferable.

## Disposition and next unchecked action

1. **Do not submit either existing candidate as a validated fix.** The original upstream omission is real; both of our competing review-only rounding implementations have independently reproduced numerical edge failures under different precision assumptions.
2. **Next by November 17 UTC:** inspect PolicyEngine's actual money precision and NH monthly income conversion path; test real `Simulation` and 2024–2026 YAML cases with exact-cent and sub-cent inputs, payment cap and $10 boundary. Choose and justify one numeric strategy with independent code and qualified benefits-policy review.
3. Before any upstream PR/comment or external publication, obtain separate owner approval and check for overlapping upstream changes.

**No outside maintainer contacted, no real applicant data used, no benefit changed, no registered node activity claimed, no Foundry/AppDeploy model calls or deployments, no production or schedule changes.** This is an internal/public-safe engineering evidence receipt only.
