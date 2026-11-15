# USDA FY2027 SNAP four-person example — November 15, 2026 source recheck

**Scope:** Read-only public-benefits accuracy check; follow-up to the November 11 evidence artifact, not a new finding or agency contact. **Review status:** Unsent; qualified federal SNAP editorial review required.

## Primary sources accessed November 15
- USDA/FNA SNAP Eligibility: https://fns-prod.azureedge.us/snap/recipient/eligibility (public page accessed; current FY2027 example)
- USDA/FNA SNAP FY2027 COLA: https://fns-prod.azureedge.us/snap/allotment/cola (FY2027 standard deductions table; page states updated November 4)

## Observed unresolved discrepancy
- The eligibility worked example explicitly identifies a four-person household and computes `$1,750 - $217 = $1,533` under “standard deduction.” Its subsequent dependent-care step produces `$1,171`.
- The controlling FY2027 COLA table lists **$229** for a four-person household in the contiguous 48 states/DC, and **$217** for sizes 1–3.
- The eligibility example later prints `$1,165 - $114.50 = $1,056.50`. The stated prior adjusted income is **$1,171**, not $1,165. Also, the displayed arithmetic is false: $1,165 − $114.50 = $1,050.50, whereas $1,171 − $114.50 = $1,056.50.
- This recheck confirms both discrepancies remain in the accessed public text. It does **not** establish the canonical fns.usda.gov page's uncached browser behavior: direct canonical fetch returned HTTP 403 in this environment. No newer superseding USDA notice was independently established.

## Significance and guardrails
A worked example may mislead applicants about the calculation; it does **not** prove a state agency is using the incorrect deduction, that any household was underpaid, or that the sample is a legally binding benefit calculation. Do not publish a proposed dollar correction as an actual entitlement without a qualified program reviewer applying all rounding and eligibility rules.

## Next unchecked action
Qualified federal SNAP program/editorial review and ordinary-browser uncached verification of the canonical USDA page. After confirmation, request separate owner authorization for a narrowly scoped, courteous agency correction submission. No external message, login, beneficiary claim, model-costly Foundry call, deployment, production mutation or scheduling change in this investigation.
