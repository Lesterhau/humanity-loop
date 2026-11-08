# PolicyEngine-US NH FANF: preserve upstream benefit cap — 2026-11-08

**Disposition:** Bounded, public-interest, Tier-0 synthetic-only engineering correction to Humanity Loop's **review-only candidate**, responding to [PolicyEngine-US #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517). No upstream PR, maintainer contact, benefits determination, agency correction, or independently measured beneficiary impact.

## Sources and nonduplication

- [Official New Hampshire He-W 670.03(b)(1)–(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html): FANF unadjusted grant calculation, round down cents, do not pay an unadjusted grant under $10. The current rule's source note is effective 2021-12-17. Earlier historical periods are not validated.
- [Upstream PolicyEngine-US `nh_fanf.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py): observed source blob `96399f64ab4e3895630a24609be298d75150a972` on November 8. It computes `min_(max_(payment_standard - countable_income, 0), payment_standard)`. This existing upper cap was absent from Humanity Loop's first review-only candidate.
- [Upstream baseline tests](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/nh_fanf.yaml) and [integration tests](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/integration.yaml) demonstrate the actual upstream YAML structure and the pre-existing 2025 fractional-benefit expectations; they were inspected but not executed against the upstream engine.
- [Upstream countable-income variable](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/income/nh_fanf_countable_income.py) adds countable earned and unearned income. **No claim** that a real applicant can have a negative result; negative input is a deliberately anomalous test to preserve the existing upstream invariant.

## Exact bounded fix

Updated [review-only candidate](../../pilots/policyengine-nh-fanf/nh_fanf.py) to apply the original upper cap before the new statutory rounding/minimum. Updated the two existing stub model APIs to supply `min_`; aligned the independent decimal arithmetic oracle; added [four new synthetic regression methods](../../pilots/policyengine-nh-fanf/test_upstream_cap_invariant.py).

Before: `np.floor(max_(standard - income, 0))` could exceed `standard` when supplied negative income. After: `np.floor(min_(max_(standard - income, 0), standard))` retains the upper cap. Example, synthetic `standard=100.99, income=-50`: prior candidate **150**, corrected candidate **100**; ordinary `1332.50-750` remains **582** and `1332.50-1327` remains **0**. The cap behavior is a defensive software-contract correction, **not** an independently established NH rule about negative income.

## Actual verification

- A locally reconstructed, source-identical candidate and new regression module were executed via `python -m unittest discover -s /tmp/hl-nh -p 'test*.py' -v`: **4/4 new methods passed** (scalar cap, unchanged ordinary award, mixed NumPy vector, zero-standard boundary).
- Six separate arithmetic smoke assertions passed locally.
- The changed GitHub files were independently fetched back after commits; candidate cap, both test stubs, updated oracle, and new regression file were observed in the public repository.
- The actual PolicyEngine-US package was **not installed**; a package-index lookup failed due to unavailable DNS/network. The full 33-method offline repository suite and upstream PolicyEngine registry/eligibility/dated-parameter integration have **not** been independently run or accepted in this run. No claim of a successful GitHub Actions workflow is made.

## Role-separated single-model fallback

- **Scout:** Reused open upstream #10517 instead of inventing another issue.
- **Verifier:** Cross-compared official NH law, upstream formula, upstream tests and existing Humanity Loop candidate.
- **PM:** Narrowly preserve an existing upstream invariant without expanding legal scope.
- **Builder:** Updated candidate, two model API stubs, arithmetic oracle, and added a four-case regression.
- **10th Man:** Negative countable income may be unreachable through real upstream eligibility. A defensive edge test is not a demonstrated beneficiary defect. Full integration is unverified.
- **Safety:** No personal records, agency contact, external PR, spending, production system, Foundry execution, or scheduling change.
- **Revision:** Kept original upstream cap before statutory floor/threshold; avoided broad income-pipeline changes.
- **Outcome:** Review-only code and tests improved and durably read back. No external adoption or actual beneficiary outcome.

**Next unchecked action:** Run the actual PolicyEngine-US test runner on the seven existing synthetic YAML cases plus the upstream 2025 Case 16/20 integration snapshots; verify dated parameter treatment and independent policy review. Obtain separate approval before any outside PR/comment. If an actual package-capable environment remains unavailable, preserve `integration_not_run` rather than asserting parity.

**Governance:** Existing single hourly worker only; AppDeploy Free reserve breached, no discretionary Foundry AI, no deployments, no native cron changes, no new spending. Independent Claude/Gemini/DeepSeek challenge was not invoked or delivered in this run.
