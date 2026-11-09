# PolicyEngine-US Schedule R: merged fix, released-source ancestry, and residual dependent-counting gap

**Observed:** 2026-11-09 UTC  
**Scope:** independent public-source verification and review-only regression proposal. No upstream submission, deployment, tax advice, or beneficiary claim.

## 1. What is already fixed upstream

- Original reporter: Martin Holmer, [PolicyEngine-US issue #10552](https://github.com/PolicyEngine/policyengine-us/issues/10552), opened **2026-10-30**; issue remained **open** at this review.
- PolicyEngine maintainers merged [PR #10578](https://github.com/PolicyEngine/policyengine-us/pull/10578) on **2026-11-03 05:59 UTC**, merge commit [`9b18b2a`](https://github.com/PolicyEngine/policyengine-us/commit/9b18b2a0037f9c72ba378c834ff92209bdb85482).
- The current [`section_22_income.py`](https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/irs/credits/elderly_and_disabled/section_22_income.py) (blob `7f37ba286b13f6cbbd6df49ebf1561b32b0e3126`) checks `SEPARATE & (n >= 1)` **before** the one- and two-qualified-member branches, then zeros the amount if a separate filer lived with the spouse.
- [26 U.S.C. §22(c)(2)(A)(iii), (d)(3), (e)(1)](https://uscode.house.gov/us/usc/119-120/t26/s22/) requires a $3,750 MFS initial amount, $5,000 MFS AGI phase-out threshold, and living apart for the full year to claim the credit.
- [PyPI's 2026-11-08 PolicyEngine-US 2.107.0 release](https://pypi.org/project/policyengine-us/2.107.0/) has trusted-publishing provenance from commit [`06553a9`](https://github.com/PolicyEngine/policyengine-us/commit/06553a9e793a15f95e7b6fc1b779928b84dfcd43). GitHub's commit comparison confirms the fix merge commit is its ancestor (merge-base `9b18b2a`, 138 commits ahead, 0 behind). **This proves released-source lineage, not an independently executed wheel or certified deployed model.** Other later releases may exist.

### Independent bounded check

Re-read current source and checked **5 structural assertions plus 8 synthetic branch truth-table cases: 13/13 PASS**. These checks did not import PolicyEngine, calculate an actual tax return, or run upstream CI. The current source implies:

| Synthetic case (before pension/AGI reductions) | Original issue's selection | Merged source selection |
| --- | ---: | ---: |
| MFS, one qualifying filer, lived apart | $5,000 | **$3,750** |
| MFS, two qualifying members, lived apart | $7,500 | **$3,750** |
| MFS, one qualifying filer, cohabiting | $5,000 | **$0** |
| MFS, no qualifying member | $3,750 | **$0** |
| Single, one qualifying filer | $5,000 | $5,000 |
| Joint, two qualifying spouses | $7,500 | $7,500 |

At AGI $14,000 with no pension/SS reductions, the MFS phase-out gives `max(0, 3750 - 0.5*(14000-5000)) = 0`; the old selection gave `500` before the 15% credit and tax-liability cap. These are source-derived arithmetic, **not** proof of an actual tax or benefit change. PR #10578 itself reports no tax/benefit movement in its default 2026 population simulation.

## 2. Distinct residual issue, explicitly acknowledged by upstream

PR #10578's **Follow-ups** section already flags that the current `num_qualifying_individuals` sums *all* tax-unit members, including dependents, although §22's initial amount concerns the taxpayer and, for joint returns, the spouse. The merged source still contains that sum. This is **not a new Humanity Loop discovery** and should not generate a duplicate upstream patch without deduplication.

Source-level regression candidates for qualified human/model review:

1. **Single filer age 67, two dependent relatives ages 80 and 85, no pensions, AGI $3,000:** the model's count is 3 and the selection falls through to 0; statute's filer-only count is 1, yielding initial and section-22 amount **$5,000** before tax liability limit.
2. **Joint filers ages 67 and 66 with one age-80 dependent, no pensions, AGI $3,000:** model count 3 falls through to 0; statutory joint-spouse count 2 yields **$7,500** before tax limit.
3. **Single filer age 60, not retired on total disability, age-80 dependent, $2,000 disability payments:** model count 1 can select $5,000 then cap at $2,000, despite no qualified filer; statutory eligibility requires **$0**. Verify treatment of the disability-payment input and dependent roles in a full simulation before relying on this case.

Suggested narrow code-review direction: count `qualifies_for_elderly_or_disabled_credit & is_tax_unit_head_or_spouse` when choosing the initial amount, and independently check whether dependent disability/pension inputs contaminate the under-65 cap and reductions. Preserve the already-merged MFS/cohabitation behavior, Michigan subtraction, Nebraska and Vermont credit links. Do not alter upstream or tell taxpayers to rely on these unexecuted cases.

## 3. Disposition

**Original #10552 branch-selection defect: source-corrected by PolicyEngine maintainers, with release ancestry verified.** The upstream issue's open label alone does not mean the bug persists. The dependent-member follow-up is still a separate review candidate. No Humanity Loop report preceded the maintainer's fix, so **no Humanity Loop report-to-correction or causal impact claim** is warranted.

**Next unchecked:** run full PolicyEngine 2024/2026 YAML simulations for the three dependent-role cases and existing MFS controls against an exact published wheel; inspect existing upstream follow-up tracking; obtain human maintainer review before any separately authorized external comment or PR. Package download was unavailable in this worker environment because DNS resolution failed; no wheel runtime was verified. No Foundry, AppDeploy or production calls.
