# Mississippi TANF SSI-recipient resources: bounded, review-only correction candidate

**Date:** 2026-11-09 UTC. **Upstream:** [PolicyEngine-US #10516](https://github.com/PolicyEngine/policyengine-us/issues/10516). **Risk:** Tier-0 source research and local simulation. **Status:** candidate only; no upstream PR, agency contact, production deployment, real applicant correction, or verified beneficiary outcome.

## Source and specific finding

Mississippi's official [TANF Policy Manual](https://www.sos.ms.gov/adminsearch/ACCode/00000330c.pdf) excludes SSI recipients from TANF assistance units and disregards their income and resources (Chapter 3, PDF pp. 192–193; Chapter 6, PDF p. 458). Its resource rules also contain joint-asset attribution details (PDF p. 421). This is a finding about PolicyEngine's model, **not an allegation that Mississippi's agency miscalculates real benefits**.

Upstream issue #10516 already identifies the general SSI-member defect. It says resources cannot be separated because the model uses aggregated `spm_unit_cash_assets`. But PolicyEngine's [definition of that variable](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/household/assets/spm_unit_cash_assets.py) aggregates three **person-level** inputs: [bank](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/household/assets/bank_account_assets.py), [stock](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/household/assets/stock_assets.py), and [bond](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/household/assets/bond_assets.py) assets. When person components are available and reconcile to the aggregate, the SSI-recipient portion can be separated. This is a narrower candidate implementation insight, not a claim of discovering the existing general defect.

## Deliverables and local verification

- [candidate.patch](candidate.patch) adds a Mississippi-specific monthly SSI membership mask and excludes person-attributed SSI assets from the resource test **only when** all person assets reconcile to the aggregate within $0.01. If an aggregate is overridden without corresponding person ownership, it retains the full aggregate, avoiding silent undercounting.
- [regression.py](regression.py) reconstructs the exact original and proposed source from the full-context patch and executes them against synthetic numpy-backed entity mocks. Local result: **2 unittest methods PASS, covering 11 resource cases plus one four-person mask case**. Three resource cases deliberately produce different outcomes under the original and candidate. This is isolated structural/arithmetic evidence, not full model integration.
- Local source-matched `git apply --check`, application, and byte-for-byte candidate-file comparisons passed on a synthetic fixture. No complete PolicyEngine checkout or upstream CI was run.

## Single-model role review (not independent multi-LLM Foundry)

**Scout:** SSI resource exclusion matters to modeled eligibility for families with disabled members. **Verifier:** Official state manual and current upstream code read; issue #10516 predates this work. **PM:** Restrict scope to resource attribution. **Builder:** Two-file patch and exact-source regression. **10th Man:** Jointly owned resources, incomplete person-level inputs, source-version changes, and potential SSI/TANF calculation dependencies can invalidate simple attribution. **Safety:** GO for review-only Tier-0 artifact; HOLD external submission or use in consequential decisions until qualified review. **Revision:** Conservative aggregate fallback when ownership cannot be reconciled. **Outcome:** No benefit or acceptance claimed; await integrated tests and review.

## Limitations and next unchecked action

This is a **partial fix**. It does not correct assistance-unit size, gross/earned/unearned income, payment amount, converted ineligible spouse rules, or other exclusions in #10516. Aggregate-only overrides may still overcount SSI resources. The $0.01 reconciliation tolerance is a modeling choice. Joint property ownership and historical rules require further interpretation. The `policyengine_us` package was unavailable locally, so **no actual PolicyEngine simulation, YAML test suite, or CI was run**.

**Next:** In an authorized complete checkout, test existing Mississippi TANF resource YAML and parent/child SSI scenarios in 2024–2026 with per-person bank/stock/bond assets, aggregate overrides, jointly owned property, and non-SSI controls; check for circular dependencies and upstream duplicate work. Obtain human code and policy review before any separately authorized upstream PR/comment.

**No new cash or operational change:** No AppDeploy or Foundry model call, deployment, purchase, external outreach, production mutation, or schedule change.
