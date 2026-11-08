# NH FANF formula contract verification — 2026-11-08

**Status:** New independent offline import-level test of Humanity Loop's existing review-only PolicyEngine-US candidate; not an upstream integration, accepted PR, official eligibility determination, or beneficiary outcome.

## External issue and official rule
- PolicyEngine-US [issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517) remains open at review time. Its current upstream [`nh_fanf.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py) still returns `min_(max_(payment_standard - countable_income, 0), payment_standard)`; GitHub source blob observed: `96399f64ab4e3895630a24609be298d75150a972`.
- New Hampshire's [He-W 670.03(b)(3)-(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html) specifies **FANF** grant cents rounded **down** to whole dollars and a **$10** minimum unadjusted monthly payment. The **adult-category** subsection (a) uses a different rounding rule and is **not** the target. The official source note for He-W 670.03 shows `#13308, effective 2021-12-17`; this supports testing 2024/2025 but does not establish the same rule for earlier periods. Subsection (b)(6) governs adjustments and is outside the candidate's modeled scope.

## New artifact and actual execution
- [Executable candidate import/contract test](../../pilots/policyengine-nh-fanf/test_candidate_formula_contract.py) imports the **actual candidate class and formula** from the adjacent `nh_fanf.py`, with a narrow fake `policyengine_us.model_api` that supplies `np`, `max_`, `where` and metadata names. This is stronger than reimplementing the calculation in a separate arithmetic-only helper.
- Local execution on 2026-11-08: `python -m unittest -v test_candidate_formula_contract.py` — **6/6 test methods passed**, including six eligible YAML fixture cases, a 7-element NumPy vector, the $9.99/$10/$10.99 boundaries, unchanged whole-dollar cases, and an explicit arithmetic comparison with the currently observed upstream formula. Python NumPy 2.3.5; PyYAML 6.0.3. No network, external account, paid model, AppDeploy, or production service was invoked by these tests.
- Representative differential: payment standard $1,332.50 and income $750 yields **$582.50** under current upstream arithmetic versus **$582** under the candidate; income $1,327 yields **$5.50** versus **$0**. These are synthetic examples, not real applicant records.

## Role-separated review (single-model fallback, not independent multi-model)
- **Scout:** Existing #10517 is specific, still open, and not duplicated.
- **Verifier:** Official NH rule checked directly; adult-category rounding differs.
- **PM:** Narrow scope to unadjusted monthly FANF award, not all TANF.
- **Builder:** Added test that executes the candidate class, not only a separately rewritten arithmetic function.
- **10th Man:** The fake model API does not test actual PolicyEngine engine, `defined_for` eligibility behavior, downstream values, parameter registry or historical dates; this must not be described as integration acceptance.
- **Safety:** Synthetic-only inputs; no agency contact, personal data, financial advice, production benefits calculation, or external PR.
- **Revision:** Explicitly exclude the ineligible YAML fixture from stubbed formula evaluation; the upstream engine, not the formula, enforces `defined_for`. Preserve the test's metadata assertion without falsely claiming an ineligible household was run end-to-end.
- **Outcome:** A reproducible import-level regression check and upstream/candidate discrepancy are now available for human review. No outside acceptance or real-world effect.

## Next unchecked action
Run the existing seven YAML fixtures against the **real PolicyEngine-US package test runner**, including the ineligible case and date-sensitive parameter registry, then independently review legal effective-date coverage and affected #10251 regression snapshots. Request explicit owner approval before any outside PolicyEngine PR/comment. Do not treat this test as an official eligibility calculator.

**Governance:** Tier-0 public-source / synthetic offline test only; zero new cash; Foundry/AppDeploy native model execution and cron remain off. Cross-model Claude/Gemini/DeepSeek independent review is requested by the owner process but not executed by this single-model worker.
