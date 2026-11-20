# New Hampshire FANF grant threshold — independent regression matrix (2026-11-20)

**Status:** proposed test cases for human review; no code change, external submission, agency contact, or verified beneficiary outcome.

Primary legal source: New Hampshire He-W 670.03(b)(1)–(5), https://gc.nh.gov/rules/state_agencies/he-w600.html (rechecked 2026-11-20). The rule determines the pre-adjustment FANF grant from the difference between payment standard and net income, floors fractional grant cents to whole dollars, and disallows payment when the pre-adjustment amount is under $10. The rule's (b)(6) adjusted-payment exception is a separate concern.

External issue: https://github.com/PolicyEngine/policyengine-us/issues/10517 (open at 2026-11-20 readback). That issue documents a model mismatch; the rows below are additional *boundary tests*, not independently executed PolicyEngine outputs.

| Payment standard | Net income | Raw difference | Expected unadjusted monthly grant | Rationale |
|---:|---:|---:|---:|---|
| $100.00 | $90.01 | $9.99 | $0 | Below $10, even if only one cent short |
| $100.00 | $90.00 | $10.00 | $10 | Exact minimum |
| $100.00 | $89.99 | $10.01 | $10 | Floor fractional cents after subtracting |
| $100.00 | $89.01 | $10.99 | $10 | Floor, do not round nearest |
| $100.00 | $89.00 | $11.00 | $11 | Whole-dollar grant unchanged |
| $100.00 | $100.00 | $0.00 | $0 | No positive difference |
| $100.00 | $100.01 | -$0.01 | $0 | Clamp negative difference |
| $100.50 | $90.00 | $10.50 | $10 | Floor **grant**, not payment standard |

These are isolated arithmetic fixtures, not full household eligibility scenarios. Implementers must additionally test realistic family composition, payment-standard year, net-income disregards, adjustment order and negative amounts using the actual PolicyEngine test harness. Do not treat this matrix as legal advice or a validated patch. No external outreach authorized by this document.
