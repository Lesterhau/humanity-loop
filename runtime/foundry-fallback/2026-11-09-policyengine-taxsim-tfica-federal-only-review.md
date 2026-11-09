# PolicyEngine-US #9952 — federal-only TAXSIM taxpayer FICA candidate (2026-11-09 UTC)

**Status:** review-only external public-interest software candidate; no upstream PR, merge, release, taxpayer outcome, or maintainer acceptance. **Risk:** Tier-0 source analysis, local simulation, public-safe code artifact. **Executor:** original Humanity Loop hourly coordinator, single-model Foundry-style fallback (NOT independently executed multi-LLM Foundry).

## Scout — concrete problem and ownership

- Existing upstream [PolicyEngine-US issue #9952](https://github.com/PolicyEngine/policyengine-us/issues/9952), filed October 7, already identifies a taxpayer FICA output contaminated by state payroll contributions. **Humanity Loop did not discover this defect.**
- The live default-branch [`taxsim_tfica.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/contrib/taxsim/taxsim_tfica.py) still defines `adds = ["self_employment_tax", "employee_payroll_tax"]` on November 9. The adjacent [`taxsim_fica.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/contrib/taxsim/taxsim_fica.py) explicitly uses federal OASDI, HI, Additional Medicare, and self-employment components.
- Primary upstream definition: [NBER TAXSIM35 documentation](https://taxsim.nber.org/taxsim35/) distinguishes `fica` (employer plus employee OASDI/HI) from `tfica` (taxpayer liability). The NBER page states its then-supported federal law extends through **2023**; 2026 amounts below are *PolicyEngine issue-reproduction fixtures*, not independently verified NBER 2026 outputs.

## Verifier — proceed narrowly

**PROCEED** with a source-list-only candidate and dependency-free regression test. The existing issue's proposed component list matches the separate federal-only `taxsim_fica` variable. No matching fix PR was identified in the targeted GitHub PR search, but search coverage does not prove none exists. No external contact or production modification authorized.

## Project Manager — acceptance criteria

1. Replace only the broad `employee_payroll_tax` alias in `taxsim_tfica`; preserve self-employment and Additional Medicare.
2. Prove state employee premiums do not change a federal taxpayer FICA output.
3. Preserve no-state-payroll TX behavior and separate SECA/Additional Medicare terms.
4. Leave integration/maintainer review and any upstream contribution for separately authorized work.

## Builder — tested artifacts

- [Review-only candidate patch](2026-11-09-policyengine-taxsim-tfica-federal-only.patch).
- [Seven offline source-list regression tests](2026-11-09-policyengine-taxsim-tfica-regression.test.py).

The patch changes the component list to:
```python
adds = [
    "employee_social_security_tax",
    "employee_medicare_tax",
    "additional_medicare_tax",
    "self_employment_tax",
]
```

Local minimal exact-source fixture:
- `git apply --check`: **PASS**; `git apply`: **PASS**.
- Candidate source AST plus synthetic component-sum tests: **7/7 PASS**.
- Original unpatched source under the same tests: **5 failures out of 7**, demonstrating the test distinguishes the current defect from the proposed fix.
- Three sample wage-only outputs, using values supplied by the existing upstream issue: CA $5,370 → $4,590; NY $4,880.40 → $4,590; TX $4,590 → $4,590. These are **fixture calculations**, not full PolicyEngine model runs.
- SECA and Additional Medicare checks used explicitly synthetic component values to guard preservation, not official tax calculations.

## 10th Man — dissent and failure modes

- **Material:** `tfica` definition and state contribution exclusion are supported by NBER documentation, but NBER's posted TAXSIM35 page is dated 2022 and does not independently establish 2026 state tax outputs. Keep 2026 examples labeled as upstream PolicyEngine fixtures.
- **Material:** AST/source-list checks do not test variable registration, tax-unit aggregation, year-specific parameters, self-employment limits, or all TAXSIM integration consumers. A passing offline check does not prove the full engine works.
- **Manageable:** `taxsim_fica` already lists the proposed federal components, reducing naming risk, but this is not an independent external model review.
- **Uncertain:** Other open PRs could change related payroll variables. Rebase and deduplicate before upstream submission.

## Safety Governor — GO for local candidate, HOLD upstream

**GO** for publication inside the owner-authorized public Humanity Loop repository as a reversible review-only artifact. **HOLD** external PolicyEngine PR, outreach, releases, real tax advice, production changes, or claims of financial benefit until full model tests and applicable separate approval. No private inputs or user financial data used.

## Revision

Kept the patch to one variable and left all `employee_payroll_tax` semantics elsewhere unchanged. Tests include a deliberate state-premium-invariance assertion and preserve the two federal terms that a simplistic subtraction might drop.

## Outcome Tracker — next unchecked

Apply the patch to a complete PolicyEngine-US checkout; run actual 2024–2026 CA/NY/TX `Simulation` tests, self-employment and Additional Medicare cases, and existing TAXSIM regression suites. Confirm the candidate against the current upstream PR list and NBER's supported-year behavior; then seek human review and separate authorization for upstream submission. The local runtime did **not** have `policyengine_us` installed; no full engine or NBER API was run. **Verified outcome today:** two public review artifacts and isolated reproducibility only. No institutional acceptance, taxpayer correction, model release, AppDeploy credit use, Foundry execution, production mutation, or new scheduler.
