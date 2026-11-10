# NH FANF: source-exact formula boundary challenge and rule effective-date verification

**Observed:** 2026-11-10 UTC. **External upstream issue:** [PolicyEngine-US #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517), **open** at review. **Scope:** review-only, no upstream patch or beneficiary action.

## Primary-source crosscheck

- [New Hampshire official He-W 670.03(b)(1)-(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html) defines the pre-adjustment FANF monthly grant, requires downward whole-dollar rounding, and suppresses pre-adjustment grants below $10.
- The [NH official rule-filing history](https://www.gc.nh.gov/rules/filing_history/sourcehe-w.html) lists document **#13308, "Readopt w/Amend He-W 670.03 Determination of the Grant," effective 2021-12-17**. This corroborates the effective-date source note in upstream #10517, but does not establish how the rule operated before 2021-12-17. Historical 2020/2021 simulations still require a prior-version review.
- Current [upstream nh_fanf.py](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py) Git blob `96399f64ab4e3895630a24609be298d75150a972` has the original unrounded formula; [upstream Case 16/20 integration YAML](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/integration.yaml) still expects $582.50/$384.50. The underlying defect was **reported upstream before Humanity Loop's work**.

## New, distinct test: execute actual source-shaped class formula with stubbed model API

The 2026-11-09 Humanity Loop [review-only candidate patch](2026-11-09-policyengine-nh-fanf-rounding-minimum-review.patch) inserts `np.floor(np.round(capped_benefit, 2))`. To test its boundary semantics, a local Python 3.13 / NumPy test loaded the exact current upstream `nh_fanf.py` text via `compile(..., 'nh_fanf.py', 'exec')` after stubbing `policyengine_us.model_api` symbols (`Variable`, `SPMUnit`, `USD`, `MONTH`, `max_`, `min_`, `where`, `np`). It replaced only the original return statement with the prior candidate or a proposed corrected formula. The stub supplied payment-standard/countable-income arrays and a $10 parameter. This is **closer to actual formula execution than the Nov 9 isolated arithmetic helper**, but is **NOT** an installed PolicyEngine package/Simulation/registry or full YAML integration.

**Four unittest methods passed locally** after using tolerant floating-point comparison for the original fractional output; tests included scalar/vector shapes, original Case 16/20 arithmetic, payment cap, zero/negative benefits, $9.99/$10/$10.01, and synthetic sub-cent stress cases. The initial exact-equality assertion on original 9.99/10.01 failed by ~9e-15 floating-point representation; replacing it with `assert_allclose` resolved that test-harness assertion, not a PolicyEngine model failure.

| Pre-adjustment raw grant | Existing upstream | Nov 9 review candidate | Correct direct-floor candidate |
|---:|---:|---:|---:|
| $582.50 | $582.50 | $582 | $582 |
| $384.50 | $384.50 | $384 | $384 |
| $9.99 | $9.99 | $0 | $0 |
| $10.00 | $10.00 | $10 | $10 |
| $10.01 | $10.01 | $10 | $10 |
| **$9.999 (synthetic)** | $9.999 | **$10 (wrong if input valid)** | **$0** |
| **$10.999 (synthetic)** | $10.999 | **$11 (wrong if input valid)** | **$10** |

**New finding:** The extra `np.round(..., 2)` in *our own* Nov 9 review-only candidate can cross a whole-dollar or $10 boundary when a raw calculation has more than two decimal places. The source rule says **round down the grant**, not first round to cents. No evidence yet establishes that valid PolicyEngine FANF inputs actually reach sub-cent precision, so this is a **defensive candidate weakness**, not an observed real-world grant error.

**Proposed review-only correction** (retain the existing payment-standard cap):

```python
capped_benefit = min_(benefit, payment_standard)
rounded_grant = np.floor(capped_benefit)
minimum_grant = parameters(period).gov.states.nh.dhhs.fanf.minimum_grant
return where(rounded_grant >= minimum_grant, rounded_grant, 0)
```

## Unchecked acceptance gates

1. Confirm model input precision conventions and floating-point boundary behavior with an actual PolicyEngine install, including sub-cent and negative-income handling.
2. Apply the candidate in a full upstream checkout; run NH baseline YAML and 2024/2025/2026 `Simulation` cases including Cases 16/20, eligibility, cap and parameter date.
3. Confirm any pre-2021 historical behavior before backfilling the 2021-12-17 parameter start date.
4. Obtain qualified independent code/policy review and **separate authorization** before any upstream PR/comment.

**Environment limitation:** The local sandbox had no `policyengine_us` installation and could not resolve github.com for `git ls-remote`. Upstream source/issue were independently read through the authorized GitHub connector. **No upstream issue comment, PR, production code, institution contact, Foundry AI call, AppDeploy deployment, paid operation, or real eligibility determination.**
