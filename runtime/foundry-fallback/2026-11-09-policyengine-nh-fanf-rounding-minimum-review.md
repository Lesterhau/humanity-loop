# New Hampshire FANF grant rounding and $10 minimum — review-only candidate

**Observed:** 2026-11-09 UTC. **External issue:** [PolicyEngine-US #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517), opened by PavelMakarchuk on 2026-10-27. This is an existing upstream finding, **not a Humanity Loop discovery**. **Status:** local candidate, not submitted or accepted upstream; no benefit award or person helped is claimed.

## Primary evidence and current implementation

1. [New Hampshire official administrative rules, He-W 670.03(b)(1)–(6)](https://gc.nh.gov/rules/state_agencies/he-w600.html): for FANF, the pre-adjustment monthly grant is the difference between the payment standard and net income, fractional cents are **rounded down to the whole dollar**, and grants below **$10** are not issued. This rule is distinct from the adult-category nearest-dollar rule in He-W 670.03(a), and from the separate post-adjustment $2 rule in (b)(6). Official page text was available through a fresh indexed government source; a later direct retrieval may require normal-browser confirmation.
2. [PolicyEngine-US current `nh_fanf.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py) returns `min_(max_(payment_standard - countable_income, 0), payment_standard)` with **neither rounding nor minimum**.
3. [Current `nh_fanf_payment_standard.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf_payment_standard.py) computes 60% of the annual poverty guideline divided by 12, which can produce fractional-dollar standards.
4. [Existing integration cases](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/integration.yaml) currently assert $582.50 for Case 16 and $384.50 for Case 20; these should become $582 and $384 **if** the new grant rule is implemented. Existing issue #10517 already identifies both cases.
5. [Upstream issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517) cites the rule's December 17, 2021 source note. Candidate parameter starts that date; independently confirm the official effective-date note and earlier historical applicability before merge. Search of related upstream pull requests found no clearly matching submitted fix at review time; this is **not** proof no PR exists.

## Candidate and checks

- [Four-file review-only patch](2026-11-09-policyengine-nh-fanf-rounding-minimum-review.patch): add a $10 `minimum_grant` parameter; cap the nonnegative calculated grant; round to cents to neutralize floating-point subtraction artifacts, then `np.floor` the **grant**, not the payment standard; issue zero below $10. Add ten NH unit-level YAML cases and adjust the two existing integration expectations. Existing eligibility remains governed by `defined_for`.
- [Isolated regression harness](2026-11-09-policyengine-nh-fanf-isolated-regression.test.py): 2 unittest methods **passed locally**, exercising 12 arithmetic subcases and reproducing two original-formula differences. This harness does **not** import the PolicyEngine package or execute its `Simulation`.
- The GitHub-published patch and test file were independently fetched. An in-memory patch application checked every context/removal line against the current upstream source and verified the old/new hunk counts for **all four changed paths**. This is stronger than arithmetic alone but **not** an upstream CI run or a local `git apply --check` in a full checkout.
- Local environment lacks `policyengine_us`; therefore full YAML policy tests, actual eligibility, vectorized array behavior, parameter loading, 2021 historical data and complete CI **have not been run**.

### Expected pre-adjustment arithmetic

| Payment standard | Countable income | Current model | Candidate | Why |
|---:|---:|---:|---:|---|
| $1,332.50 | $750.00 | $582.50 | $582 | floor grant |
| $1,332.50 | $1,327.00 | $5.50 | $0 | below $10 |
| $1,332.50 | $1,322.50 | $10.00 | $10 | exact threshold |
| $1,332.50 | $1,322.51 | $9.99 | $0 | below threshold |
| $1,332.50 | $1,322.49 | $10.01 | $10 | floor grant |
| $1,022.00 | $637.50 | $384.50 | $384 | integration Case 20 |

These are source-derived or isolated synthetic arithmetic examples, **not** verified household determinations. Actual awards depend on eligibility, income counting, adjustments, and agency decisions.

## Independent challenge / dissent

- Verify that `np.round(capped_benefit, 2)` is appropriate for all PolicyEngine input precision conventions. NH income-conversion rules generally retain two decimals, but floating-point edge cases and sub-cent data should be tested in actual simulations.
- Check whether the minimum should apply before any modelled sanctions/recoupments and whether existing `nh_fanf_eligible` should change (candidate intentionally does not alter eligibility).
- Confirm parameter start date against the official rule source note; the issue quotes 2021-12-17, but this review has not independently authenticated historical prior versions.
- Ensure no conflict with an upstream PR, and run 2024/2025/2026 tests including Case 16/20, zero income, 9.99/10.00/10.01, pre-effective-date regressions and vectorized results.
- An upstream change needs PolicyEngine maintainer review and authorization; do not submit a PR or imply the correction is deployed.

**Next unchecked action:** In a complete PolicyEngine-US checkout, apply this candidate, run actual policy YAML tests and `Simulation` regressions across relevant years, then obtain human review before separately authorized upstream contribution.

**Permission/cost:** Only public-source reads and authorized public-safe Humanity Loop evidence files. No external maintainer contact, agency correspondence, production changes, Foundry/AppDeploy AI use, purchase, or new scheduler.
