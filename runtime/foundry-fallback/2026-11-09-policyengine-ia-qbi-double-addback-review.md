# Iowa modified-income QBI double addback — review-only correction candidate

**Observed:** 2026-11-09 UTC. **External owner:** PolicyEngine-US. **Upstream issue:** [#10512](https://github.com/PolicyEngine/policyengine-us/issues/10512), open when checked. **Output:** [candidate unified patch](2026-11-09-policyengine-ia-qbi-double-addback-candidate.patch). **Risk:** Tier-0 public-source/code research only; no taxpayer data, external PR, deployment or outreach. **Method:** single-model Foundry-style fallback with independent primary-source/code checks; **not** independent multi-LLM review.

## Scout / Verifier

The existing upstream issue already identifies a specific Iowa 2023+ model error; this is a **tested candidate for that existing issue**, not a newly discovered bug or a claim of model adoption. The current default-branch [Iowa modified-income source list](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/parameters/gov/states/ia/tax/income/modified_income/sources.yaml) contains both `taxable_income_deductions` and `qualified_business_income_deduction` after 2023. The [model variable](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/ia/tax/income/ia_modified_income.py) adds that list. Both the [itemizing](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/parameters/gov/irs/deductions/deductions_if_itemizing.yaml) and [nonitemizing](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/parameters/gov/irs/deductions/deductions_if_not_itemizing.yaml) federal deduction lists already include the QBI deduction. The [taxable-income deduction variable](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/irs/income/taxable_income/deductions/taxable_income_deductions.py) selects one of those lists.

**Independent official legal cross-check:** [Iowa Code 2024, §422.5(3)(a)](https://www.legis.iowa.gov/docs/code/2024/422.html) directs the applicable federal deductions, including qualified business income, to be added back in computing the low-income exemption's net income. The statute does not direct a *second* addback of the same QBI amount. The upstream issue also cites [Iowa Department of Revenue's 2024 worksheets](https://revenue.iowa.gov/forms) and detailed reproduction, which were not independently executed here.

## Project manager / Builder

Smallest patch: remove only the duplicate explicit `qualified_business_income_deduction` entry from the **2023-01-01** Iowa modified-income list. Leave 2021 sources untouched. Add three YAML regression cases for 2024 QBI, 2024 zero-QBI and 2022 historical source behavior. No changes to the federal deduction definition, eligibility thresholds, or other states.

**Local deterministic checks performed against a fixture reconstructed from the fetched upstream YAML (not the complete upstream checkout):**
- `git apply --check`: PASS; `git apply`: PASS.
- Three added test cases parsed as YAML; arithmetic/source-list oracle: **3/3 PASS**.
- Verified the 2024 federal itemizing and nonitemizing parameter lists each contain QBI as an included deduction. These checks inspect fetched source content; they do not execute the PolicyEngine simulation engine.
- Issue #10512 example A, using the displayed rounded inputs: old `5,718.79 + 17,979.70 + 1,429.70 = 25,128.19`; candidate `5,718.79 + 17,979.70 = 23,698.49`, below the statute's $24,000 threshold for a qualifying older single filer. The issue's full-simulation expected result is $23,698.48 due to underlying unrounded quantities; **we did not independently reproduce that full-simulation output**.
- Issue #10512 example B, using rounded inputs: old $38,148.91; candidate $37,174.09. This is a formula check, not an independently verified tax return.

## 10th Man / Safety / Revision

**Strongest objection:** This may be mathematically correct for 2024 while still failing full PolicyEngine integration. Direct input overrides in YAML tests can miss entity/year/rounding effects. The 2025+ federal deduction lists also include OBBBA deductions beyond standard/itemized and QBI; whether Iowa should add those back is a **separate unresolved statutory/worksheet question**. Do not generalize this patch into a complete 2025+ Iowa tax-law correction. The upstream issue already suggested the one-line fix; the incremental contribution is a reproducible, independently reviewed patch with local test evidence, not novelty or maintainer endorsement.

**Safety verdict:** GO for internal public review artifact; HOLD on upstream PR, taxpayer guidance, deployments, or model-output accuracy claims pending complete package tests and human/maintainer review. No real applicant/taxpayer benefit, institutional acceptance, or independent multi-model validation is claimed.

## Outcome / next unchecked action

1. In a complete PolicyEngine-US checkout, apply the patch and run the actual YAML policy tests and full 2024 issue reproduction for exemption and Iowa tax; verify itemizing and nonitemizing cases, and no 2021–22 regression.
2. Independently evaluate 2025+ OBBBA addback semantics separately; do not bundle speculative changes.
3. If upstream issue remains open and integration passes, request appropriate human review and separate authorization before any external PR.

**Source provenance:** upstream issue #10512 checked Nov 9; current fetched blob SHA for Iowa sources `f938a7d2bffe774e2fe7161e7b6d385374c492b3`; itemizing/nonitemizing lists and variable fetched Nov 9. No external maintainer contacted. No Foundry/AppDeploy model calls, credits, production writes or schedule changes.
