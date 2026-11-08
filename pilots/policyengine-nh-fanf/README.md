# Pilot: NH FANF grant rounding and minimum payment

**Status:** reviewed prototype; **NOT an upstream merge, production benefits calculation, or verified applicant outcome**. Prepared November 8, 2026 for Humanity Loop's first external-benefit engineering deliverable.

- External request: [PolicyEngine-US issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517), which describes a current calculation defect and upstream test cases.
- **Primary law:** [New Hampshire Administrative Rules He-W 670.03(b)(1)-(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html), which rounds fractional FANF grants *down* to whole dollars and makes grants below $10 unpayable. Note subsection (b)(6) discusses later adjustments NOT modeled here.
- Source inspected: `policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py` in PolicyEngine-US; its calculation currently returns `min_(max_(payment_standard - countable_income, 0), payment_standard)` without either whole-dollar rounding or $10 minimum.
- **Candidate:** `nh_fanf.py` is an isolated copy with `np.floor` and `where(... >= 10, ..., 0)`. `nh_fanf.yaml` supplies seven synthetic PolicyEngine-style cases. `test_formula_offline.py` supplies 12 pure-Python independent arithmetic cases (run locally: 12/12 pass on Nov 8).
- **Verified source-history note:** The official He-W 670.03 source note says the current section was superseded by filing #13308 effective **December 17, 2021**. This establishes the current section's effective date but does **not** establish that identical rules were in effect in every earlier simulation year. Cases below use 2024–2025 dates. Historical applicability must still be reviewed.
- **What remains unverified:** full PolicyEngine test suite/integration (policyengine_us not installed in this execution environment), complete rule history before December 17, 2021, whether to parameterize the $10 threshold, impact on existing fractional-result fixtures and related eligibility pipelines, code maintainer's preferred approach and review, upstream adoption.
- **Next:** obtain independent legal/policy and model review, run `policyengine_us` integration tests with the actual model/parameter registry and dates; update old affected test snapshots. Only then request the owner's permission for an external PR/issue reply. Never label this as an operational eligibility determination or a correction accepted by NH or PolicyEngine.
- **No applicant data / outreach:** all inputs are synthetic, no external organization contact, production systems or model billing changed by this pilot.

In addition to the 12 pure-arithmetic tests, `test_candidate_formula_offline.py` exercises the **actual candidate formula** under a minimal scalar stub of PolicyEngine's model API (10 separate test cases). The CI job also runs the pre-existing six NumPy/YAML contract tests (including vector arithmetic, metadata and fixture checks), for **28 offline test methods** in total. NumPy and PyYAML are pinned in CI; this uses no paid AI inference. This is **not a full PolicyEngine integration test**, including vector arrays and period handling.

Try offline tests:
```sh
python -m unittest discover -s pilots/policyengine-nh-fanf -p 'test*.py'
```

Acceptance is **not** just successful arithmetic: upstream full regression and an independent policy reviewer need to approve it. Measured public benefit requires observed integration/use rather than just a diff.
