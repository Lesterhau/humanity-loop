# NH FANF: four upstream-shaped grant-boundary regression candidates

**Observed and checked:** 2026-11-12 UTC. **Status:** public-safe review-only candidate; not submitted to PolicyEngine-US and not executed in a complete PolicyEngine/OpenFisca Simulation. No benefit payment or eligibility decision was made.

## Evidence and purpose

- [New Hampshire Administrative Rule He-W 670.03(b)(3)–(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html) (direct official page reviewed November 12): FANF monthly grant rounded **down** to the whole dollar; no pre-adjustment grant below **$10** is payable. Distinguish this from adult-category assistance in subsection (a), which has a different rounding rule.
- [PolicyEngine-US upstream issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517) already identified the missing grant-rounding and minimum-payment logic. Humanity Loop did **not** originate that finding.
- [Upstream NH FANF integration YAML](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/integration.yaml) provides the 2024 two-person recipient shape and the 2025 three-person Case 16. [Upstream `nh_fanf.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py) currently subtracts countable income without the rule's whole-dollar floor/minimum.
- [Previous Humanity Loop annual-wages trace](2026-11-11-nh-fanf-annual-wages-subcent-path-review.md) explains the annual-to-monthly / 50%-disregard pathway and warns that a cents-pre-rounding patch is unsafe for hypothetical sub-cent amounts.

## New bounded deliverable

[`2026-11-12-nh-fanf-10-dollar-boundary-candidates.yaml`](2026-11-12-nh-fanf-10-dollar-boundary-candidates.yaml) is a **four-case proposed integration fixture**, using upstream field names and model test structure. For these scenarios, use the existing upstream 2024 two-person payment standard **$1,022**, a current-recipient 50% earned-income disregard, and no child-care deduction/unearned income. Exact Decimal arithmetic is a *review oracle*, not evidence of the full model's float behavior.

| Case | Annual wages | Exact pre-adjustment grant | Rule-based proposed expected `nh_fanf` |
|---|---:|---:|---:|
| A — under minimum | $24,288.24 | $9.99 | **$0** |
| B — at minimum | $24,288.00 | $10.00 | **$10** |
| C — above minimum, cents | $24,287.76 | $10.01 | **$10** |
| D — upstream 2025 Case 16 | $18,000.00 | $582.50 | **$582** |

Derivation for A–C: countable monthly earned income = annual wages / 12 × 0.5 = annual wages / 24. Subtract from $1,022; the recipient's 50%-disregard eligibility amount remains below $1,022. For D, $1,332.50 − ($18,000 / 24) = $582.50. These scenarios avoid the *sub-cent* ambiguity from the separate $12,000.10 annual-wages example; that example remains a diagnostic requiring qualified interpretation, not a confidently asserted upstream integration expectation.

## What was actually verified

The four YAML objects were parsed with local PyYAML, and a separate Python `Decimal`/`ROUND_FLOOR` oracle reproduced all four expected grant values and the assumed countable-income-below-standard condition. **4/4 isolated arithmetic assertions passed**. This is neither a real full-engine integration pass nor confirmation of the state eligibility administration. The fixture is a review candidate only, and a future engine test might reveal other eligibility gates or input period conversion differences.

## Next unchecked action

Install or access an authorized, reproducible PolicyEngine-US checkout at a pinned commit, run the four fixture cases under the actual 2024/2025 simulation and compare upstream Cases 16/20, then inspect full-engine period normalization and rounding semantics. Qualified policy/code review must precede any upstream PR, issue comment or externally published claim of a fixed model. No outside contact or production change was authorized or attempted.
