# Upstream submission preparation — NH FANF grant #10517

**Status:** Prepared in Humanity Loop, **not submitted** to PolicyEngine-US or The Axiom Foundation. All cases are synthetic. No applicant records, benefit determinations or outside writes.

## Verified recipient and source facts (November 8, 2026)

- [PolicyEngine-US issue #10517](https://github.com/PolicyEngine/policyengine-us/issues/10517) is **open** and requests `np.floor` on monthly FANF grants and **no pre-adjustment grant under $10**, using N.H. Admin. Rules [He-W 670.03(b)(3)-(5)](https://gc.nh.gov/rules/state_agencies/he-w600.html).
- Current upstream `nh_fanf.py` still lacks those two rules and caps benefit at its payment standard with `min_`. Humanity Loop preserved that invariant.
- Candidate `nh_fanf.py` + `policyengine_us/parameters/gov/states/nh/dhhs/fanf/minimum_grant.yaml` + seven synthetic new YAML cases reside in the parent pilot directory. Parameter starts **2021-12-17** because the current rule section's source note specifies that effective date. **That date must not be assumed to establish earlier-year policy.**
- The `uv`-locked full upstream package was installed in disposable GitHub Actions at upstream commit `92caead63eea36b15c6ca86edf3d79214459e7a9`; original five baseline and new seven synthetic cases **12/12 passed** in PR #74. Later full NH folder suite is exercised by the expanded workflow; check current CI evidence before claiming those results.
- PolicyEngine `pyproject.toml` uses **Towncrier** with directory `changelog.d` and a `fixed` type. A proposed short fragment is staged here at [`upstream/changelog.d/10517.fixed.md`](upstream/changelog.d/10517.fixed.md); the file belongs under the **recipient repository's** `changelog.d` when an owner-authorized upstream PR is prepared.
- Source note for Axiom: [TheAxiomFoundation/rulespec-us](https://github.com/TheAxiomFoundation/rulespec-us) includes `us-nh/policies/income_tax` and `us-nh/regulations/he-w-700`, but the inspected NH directories **do not currently contain a FANF implementation**. Therefore there is no existing NH FANF Axiom mirror to claim cross-engine parity with. If contributing a new RuleSpec module later, that is a separate licensed/scoped upstream project, requiring a legal source and executable oracle; **do not count Axiom model parity as verified**.

## Before making an external PR

1. Full PolicyEngine NH FANF directory regression, **especially** `integration.yaml`, income/disregard and eligibility, must be green in the real upstream package. A dedicated workflow runs all `policyengine_us/tests/policy/baseline/gov/states/nh/dhhs/fanf/*.yaml`, not just two individual files.
2. Re-check official New Hampshire He-W 670.03 source and its date history. Ensure `nh_fanf.minimum_grant` is a legitimate, existing-namespace PolicyEngine parameter and that prior-year simulation queries behave correctly (do not silently project 2021 rules onto earlier years). Obtain a qualified welfare-policy reviewer for any materially consequential interpretation.
3. Verify no other U.S. tests in the recipient repo assert obsolete .50 outcomes. Upstream issue #10517 explicitly flags fractional expectations linked to #10251 (Cases 16 and 20), which may appear outside `nh_fanf.yaml`. Search and update the minimal affected fixtures with official evidence; do not run a broad snapshot rebaseline blindly.
4. Include the recipient-standard changelog fragment, update formula and parameter, add effective-date and fractional tests, and cite legal text. Do not insert Humanity Loop project branding into a recipient's production benefits code.
5. Confirm the user explicitly authorizes any *external* PolicyEngine issue reply or PR; all current work is confined to Humanity Loop and a disposable public-source CI checkout.
6. Track later upstream maintainer review, acceptance and deployments distinctly. A merged patch is an upstream improvement, **not** proof that residents' benefits were correctly determined or beneficiaries reached.

## Independent review responsibilities

- Engineering reviewer: checks edge cases, vector/array handling, source pin, historical parameter namespace, CI green, adjacent regression expectations.
- Policy-domain reviewer: checks statutory dates, rule interpretation and applicability, eligibility context, $10 minimum and any other adjustment semantics.
- Owner: decides whether/when to submit the external PR, without claiming an external institutional endorsement.

## Related long-term work

The first genuine independent Humanity Loop node still requires register → checkin/claim → submit/quarantine → independent reviewer disposition, and later verified adoption. This benefits-code candidate was produced and tested by the authorized owner/assistant team, **not** by one of the yet-unregistered volunteer nodes.
