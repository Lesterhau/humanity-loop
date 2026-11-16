# NH FANF — current-main implementation versus administrative rule (read-only review)

Observed: 2026-11-16 UTC. Status: independently inspected source code; **not** an executed PolicyEngine simulation, merged fix, official eligibility determination, or external submission.

## Primary-source cross-check

- Official New Hampshire administrative rules, He-W 670.03(b)(3)–(5): https://gc.nh.gov/rules/state_agencies/he-w600.html — fractional FANF grants are rounded **down** to whole dollars, and pre-adjustment grants below $10 are not paid.
- PolicyEngine-US open issue #10517: https://github.com/PolicyEngine/policyengine-us/issues/10517 (read 2026-11-16; state open). Issue describes both missing transformations and proposes a minimum-grant parameter.
- Direct GitHub connector read of current default-branch `policyengine_us/variables/gov/states/nh/dhhs/fanf/nh_fanf.py`: blob SHA `96399f64ab4e3895630a24609be298d75150a972`. The formula currently computes `benefit = max_(payment_standard - countable_income, 0)` then `return min_(benefit, payment_standard)`. No rounding or $10 cutoff appears in this inspected formula.
- Direct GitHub connector lookup of `policyengine_us/parameters/gov/states/nh/dhhs/fanf/minimum_grant.yaml` returned 404. This only proves that **this exact path** was absent; it does not establish that no other minimum parameter exists.
- Previous Humanity Loop independent arithmetic boundary matrix: https://github.com/Lesterhau/humanity-loop/blob/main/research/benefits/2026-11-16-nh-fanf-grant-rounding-boundary-test-matrix.md

## Narrow result

The currently fetched implementation still visibly lacks the two rule transformations, consistent with open upstream issue #10517. That is stronger than merely restating the issue, but does not prove that all end-to-end outputs are wrong in the current released package: eligibility gates, downstream adjustments, test fixtures and release versions have not been executed or exhaustively reviewed.

For a hypothetical eligible group with a $1,332.50 standard and $750 countable income, this formula's unrounded intermediate is $582.50; the rule's pre-adjustment amount is $582. For $1,327 countable income, the intermediate is $5.50 and the rule's minimum suppresses the grant to $0. These are **static code-path arithmetic illustrations**, not production simulations.

## Next unchecked action

On an isolated review branch, inspect current test fixture conventions and upstream PRs, add rule-cited minimum parameter plus floor/cutoff logic and reproducible YAML tests, run the test suite, seek independent review. Do not contact upstream maintainers or submit a PR without separate authorization. No external outreach, benefits determination, deployment, production mutation, cost-bearing Foundry/AppDeploy call or participant claim occurred.
