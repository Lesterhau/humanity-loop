# Review-only build: Iowa QBI double addback (PolicyEngine-US #10512)

**Date:** 2026-11-10 UTC. **Scope:** Tier-0 public-source review and local isolated tests. **Mode:** one ChatGPT model with logically separated Foundry roles, **not** eight independent LLMs or an active Foundry scheduler. **Status:** tested candidate, not upstream accepted.

## Scout → Verifier
- Upstream [PolicyEngine issue #10512](https://github.com/PolicyEngine/policyengine-us/issues/10512) **already identified** the problem. We did not discover it. Fresh main-branch read shows redundant QBI entry in `policyengine_us/parameters/gov/states/ia/tax/income/modified_income/sources.yaml`, blob `f938a7d2bffe774e2fe7161e7b6d385374c492b3`.
- Current `taxable_income_deductions` chooses itemizing/nonitemizing lists, **both of which already include** `qualified_business_income_deduction`. Upstream blobs: aggregate `37f7223e4c985e676e526abdb42d55004bbb9998`, itemizing `87159339586883ceda1619baf7e07087f2700d69`, nonitemizing `27e158096e0f6c2d4ec3d6d9fcc999d78e18408e`.
- [Iowa Code 422.5 (2024)](https://www.legis.iowa.gov/docs/code/2024/422.5.pdf) §§2(a), 3(a) provides a **single** QBI addback. [2024 Iowa Alternate Tax Worksheet 41-145](https://revenue.iowa.gov/media/4098/download?inline) has separate lines for federal Form 1040 line 12 and line 13 QBI. Software that aggregates both before the Iowa calculation must not add QBI again.
- Scoped PR searches for `#10512`, `ia_modified_income` + QBI, and Iowa modified income found no matching correction PR. Search incompleteness means concurrent work remains possible.
- **Verifier: PROCEED** with a review-only candidate; no tax advice or upstream contact.

## Project Manager → Builder
- Remove **only** the extra QBI line from Iowa's 2023+ parameter source list; leave the 2021 list intact. Add four pinned YAML test cases (2022 legacy; 2023 and 2024 positive QBI; 2024 zero QBI).
- Deliverables: [candidate.patch](candidate.patch) and [standalone isolated regression.py](regression.py). To reproduce: `python regression.py --pre` (expected failures), `python regression.py` (expected pass), or `python regression.py path/to/sources.yaml` in an upstream checkout.
- **Local actual test evidence:** original source list fails three checks (duplicate QBI plus two positive-QBI arithmetic cases); candidate passes all three unittest methods with four pinned arithmetic cases. `git apply --check`, `git apply`, and post-application source-byte comparison PASS in a minimal source-matched fixture tree.
- Pinned 2024 example: original source list yields **$25,128.19** modified income, candidate **$23,698.49**, a **$1,429.70** difference. This is an isolated arithmetic fixture, **not** a full PolicyEngine Simulation or measured taxpayer outcome.

## 10th Man → Safety Governor → Revision
- **Dissent:** 2025+ federal `taxable_income_deductions` also contains newer deductions (tips, overtime, additional senior and auto loan interest). Iowa's treatment of those items needs a **separate** legal/implementation audit. This QBI fix is not a comprehensive Iowa tax fix. Filing-status, tax-unit, alternate-tax, itemizing, model/YAML CI, and historical-year interactions remain untested.
- **If this wins, who loses?** An incorrect model patch can misstate taxes for real people. Mitigation: independent Iowa tax-policy and PolicyEngine maintainer review, real 2023–2026 model simulations and threshold tests before merge.
- **Safety:** GO for public-safe review artifact in Humanity Loop; **HOLD** on external upstream PR/comment, production deployment, tax advice or claims of impact. No external writes, accounts, secrets, model API, AppDeploy spending or schedule changes.
- **Revision:** retained only the minimal QBI correction and explicitly limited claims.

## Outcome Tracker
- **Current result:** reproducible, unsubmitted candidate. No upstream acceptance, real taxpayer benefit, institution correction or independent contributor node.
- **Next unchecked by 2026-11-17 UTC:** run full upstream model/YAML regression for 2023–2026 and 2025+ deduction interactions, check current Iowa worksheets and new PRs, obtain human review, then seek separate authorization before upstream submission.
