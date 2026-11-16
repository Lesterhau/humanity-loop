# New Hampshire FANF grant rounding — independent boundary-case test matrix (2026-11-16 UTC)

Status: public-safe research/test design; **not a code change, eligibility determination, verified production defect reproduction, or outside contribution**. No agency or PolicyEngine outreach.

## Primary authority

New Hampshire administrative rule [He-W 670.03(b)(1)-(6)](https://gc.nh.gov/rules/state_agencies/he-w600.html) (state legislative rules publication, reviewed 2026-11-16): for eligible FANF assistance groups, the difference between payment standard and net income is the monthly grant; fractional cents are **rounded down**, not nearest-dollar; the **pre-adjustment monthly** minimum is $10; grants below $10 are not paid. Clause (b)(6) concerns *post-adjustment* payments and is a distinct calculation. Importantly, **adult category** grants in (a)(3) instead round at $0.50 and use a $2 minimum: do not accidentally reuse adult-category logic for FANF. The source note for (b) includes rule #13308 effective 2021-12-17. He-W 658.02 establishes the payment standard as 60% of the applicable federal poverty guideline for the assistance group.

## Public implementation issue

[PolicyEngine-US #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517), read through GitHub connector 2026-11-16, remains **open** and documents a proposed discrepancy in `nh_fanf` and three example cases; issue text is an allegation, not an independently executed test result. The proposed remedy is to floor the **grant difference** and suppress pre-adjustment grants below $10, not to round the payment standard first.

## Independent pure-arithmetic edge cases for a developer's test fixture

Assume eligible FANF group, no subsequent adjustments, and a fixed illustrative payment standard of $1,332.50; amounts below are **hypothetical**, not verified benefit awards. Formula for the *pre-adjustment* monthly grant: `raw = max(standard - net_income, 0); rounded = floor(raw); expected = rounded if rounded >= 10 else 0`.

| Net income | Raw grant | Expected pre-adjustment FANF grant | Purpose |
|---:|---:|---:|---|
| $1,332.50 | $0.00 | $0 | zero boundary |
| $1,322.51 | $9.99 | $0 | immediately below minimum |
| $1,322.50 | $10.00 | $10 | minimum inclusive |
| $1,322.49 | $10.01 | $10 | floor after subtraction |
| $1,322.01 | $10.49 | $10 | **not** adult-category nearest-dollar rounding |
| $1,322.00 | $10.50 | $10 | **not** adult-category $0.50 round-up |
| $750.00 | $582.50 | $582 | published issue's fractional case |
| $1,333.00 | negative $0.50 | $0 | no negative grants |

The matrix verifies only arithmetic against the cited rule; it does **not** test current PolicyEngine source, 2026 payment-standard inputs, net-income disregards, household eligibility, sanctions, recoupment or semi-monthly issuance. The issue's 2025 $1,332.50 example is retained as an illustrative fixed standard, not claimed to be the 2026 standard.

## Next unchecked action

On a review branch, inspect current `nh_fanf.py` and existing YAML test conventions; reproduce #10517 against an exact current commit, add these edge cases and fix only the correct pre-adjustment grant calculation, run targeted tests, and obtain independent review. Do **not** submit upstream PR, publish eligibility advice, contact affected households, or deploy without separate authorization. This note alone establishes neither a corrected bug nor a beneficiary outcome.
