# New Hampshire FANF — source-traced annual-wages path reaches sub-cent grant arithmetic

**Observed:** 2026-11-11 UTC. **Status:** independent read-only upstream source trace plus locally executed standalone arithmetic. Review-only; no PolicyEngine Simulation or upstream contribution.

## Why this is a new finding

The prior November 11 precision review could not establish whether sub-cent amounts are reachable through a plausible PolicyEngine FANF input. The current upstream source **does not explicitly round intermediate monthly income to cents**. It accepts an annual USD floating-point earned-income input, converts that input to monthly TANF gross income, applies the NH 50% earned-income disregard, and subtracts from a monthly payment standard. Consequently, annual income supplied to the cent can yield repeating sub-cent monthly countable income. This is a **source-supported modeled path**, not proof of the exact full-engine period-conversion implementation or a real household award.

## Exact primary-source chain (GitHub main inspected Nov 11)

1. [`employment_income_before_lsr.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/input/employment_income_before_lsr.py) declares a **YEAR**, USD, float person input. The [TANF earned-income sources parameter](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/parameters/gov/hhs/tanf/cash/income/sources/earned.yaml) includes that annual variable.
2. [`tanf_gross_earned_income.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/hhs/tanf/cash/income/tanf_gross_earned_income.py) is a **MONTH** person variable with `adds = "gov.hhs.tanf.cash.income.sources.earned"`. Upstream [NH integration Case 2](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/integration.yaml) demonstrates annual $12,000 becoming monthly $1,000 in the expected model calculations. This corroborates 12-month allocation for that test; the underlying core period-conversion implementation remains to be inspected.
3. [`nh_fanf_countable_earned_income.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/income/nh_fanf_countable_earned_income.py) multiplies gross earned income by `1 - p.recipient_rate`, then subtracts any child-care deduction, with no explicit cents rounding. [NH recipient_rate parameter](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/parameters/gov/states/nh/dhhs/fanf/income/earned_income_disregard/recipient_rate.yaml) is **0.5**.
4. [`nh_fanf_countable_income.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/income/nh_fanf_countable_income.py) adds countable earned and TANF gross unearned income. [`nh_fanf_payment_standard.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf_payment_standard.py) uses annual FPG × 0.6 / 12. [`nh_fanf.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py) subtracts countable income, clamps at zero and caps at standard, currently without whole-dollar rounding/minimum.
5. [NH He-W 670.03(b)(3)–(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html) requires whole-dollar **downward** rounding of the grant and suppresses pre-adjustment grants below $10. [Upstream issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517) identified the original missing-rounding defect before Humanity Loop.

## New deterministic hypothetical, no personal data

Use the 2024 two-person NH FANF example from upstream integration Case 2 (payment standard **$1,022**, no child-care or unearned income, otherwise eligible), but supply annual employment income **$12,000.10** rather than $12,000.00. Using exact Decimal arithmetic to represent the source-shaped annual-to-monthly and 50% disregard path:

| Step | Exact mathematical result (approx.) |
|---|---:|
| Annual earned income | $12,000.10 |
| Monthly gross, divide by 12 | $1,000.008333333… |
| Applicant eligibility test at 80% | $800.006666667… < $1,022 |
| Countable earned income at 50% | $500.004166667… |
| Pre-rounding grant | $521.995833333… |
| Correct down-to-whole-dollar grant, if these inputs flow unchanged | **$521** |
| Humanity Loop's older `floor(round(raw, 2))` review candidate | **$522** |
| Direct binary-float `floor(raw)` in this example | $521 (but previously shown to fail other exact-integer boundaries) |

A standalone deterministic reproduction in [`2026-11-11-nh-fanf-annual-wages-subcent-regression.py`](2026-11-11-nh-fanf-annual-wages-subcent-regression.py) was executed locally. It checks the annual cents case, an even-dollar control, and the separate $1,129.61−$211.61 binary-float underfloor example. **These are source-shaped isolated calculations, not a full PolicyEngine simulation.**

## Decision / limitations

- The old cents-rounding candidate is **not safe to promote** without verifying a mandatory intermediate-cent rounding rule; the upstream NH formulas examined contain none. The direct-floor alternative also remains unsafe at exact-dollar binary-float boundaries, as documented in the prior receipt.
- This finding **narrows the earlier uncertainty**: sub-cent precision is arithmetically reachable through ordinary annual-cent inputs under the source-shaped pathway. It does **not prove** how the actual OpenFisca/PolicyEngine period conversion, input normalization or optional preprocessing handles the annual $12,000.10 value.
- Next by **November 17 UTC**: inspect the installed model's actual period conversion and NH FPG source, run a full 2024 Simulation/YAML case with annual $12,000.10 and exact-dollar cancellation examples, inspect upstream rounding conventions, and obtain qualified code/benefits-policy review. Choose an integer-unit/Decimal or rigorously justified tolerance strategy only after that evidence.
- No upstream PR/comment, agency contact, benefit change, registered node, Foundry AI call, AppDeploy spend, production mutation or scheduling change. This is **engineering review**, not an accepted public benefit.
