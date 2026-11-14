# New Hampshire FANF grant boundary regression matrix — independent source review (2026-11-14 UTC)

Status: UNSENT, research-only, no executed PolicyEngine tests or benefit determinations.

## Primary evidence
- New Hampshire He-W 670.03(b)(1)-(5): https://gc.nh.gov/rules/state_agencies/he-w600.html (official rules; directly inspected November 14).
- Federal 45 CFR 233.20: https://www.ecfr.gov/current/title-45/subtitle-B/chapter-II/part-233/section-233.20 (official eCFR; section inspected).
- Upstream open defect: https://github.com/PolicyEngine/policyengine-us/issues/10517 (directly fetched November 14).

## Distinct action: boundary-condition regression design
For a **hypothetical, otherwise eligible** NH FANF household, let G be the *unadjusted* positive grant computed as payment standard minus countable income, before any separate recoupment or adjustment. He-W 670.03(b)(3)-(5) requires whole-dollar truncation and no payment for pre-adjustment grant below $10.

| Raw G | Expected unadjusted FANF payment | Test intent |
|---:|---:|---|
| $0.00 | $0 | zero baseline |
| $9.99 | $0 | immediately below threshold |
| $10.00 | $10 | inclusive threshold |
| $10.01 | $10 | cents above threshold |
| $10.50 | $10 | reject nearest-dollar rounding |
| $10.99 | $10 | reject nearest-dollar rounding |
| $11.00 | $11 | integer preservation |
| $582.50 | $582 | upstream issue reproduction |

Do not round the *payment standard* before subtracting countable income. The adult-category nearest-dollar rule in He-W 670.03(a) is distinct from FANF (b). This matrix tests grant arithmetic only; it does not assert that each raw G corresponds to an actually eligible case, nor model adjusted payments under (b)(6).

## Verification and limits
The official New Hampshire rule and upstream issue were inspected; no patch checkout, unit-test execution, PR review, government contact, or upstream submission occurred. The upstream issue was open when read. This matrix is a proposed independent regression checklist, not a verified software fix or actual benefit payment.

Next unchecked: map these cases to actual PolicyEngine test fixtures and execute pinned tests on a reviewed patch, then seek qualified upstream review. No external publication beyond this public-safe project research receipt.
