# Production contributor onboarding: read-only public-page acceptance

**Observed:** 2026-10-25 UTC
**Owner:** Humanity Loop main worker / contributor onboarding lane
**Risk:** Tier 0; unauthenticated public-page read only
**Target:** https://humanity-loop.vercel.app/join
**Source change:** https://github.com/Lesterhau/humanity-loop/commit/60470b251488e7ea006fcce20c4db84895b78368
**INTEND:** https://github.com/Lesterhau/humanity-loop/blob/main/runtime/ops/intents/2026-10-25-contributor-pre-registration-consent-controls.md

## Independently observed production HTML

A fresh read-only retrieval of the rendered public `/join` page, scoped to its `main` element, returned the new exact heading **“Before registering: control and privacy”** after the source change was independently fetched. This confirms the new public-page copy reached the production response; it does **not** establish a successful registration or end-to-end node workflow.

| Narrow check | Result | Evidence |
|---|---|---|
| Public onboarding page returns visible HTML and registration form | PASS | `/join` response includes “Create my node” form |
| Public MCP endpoint and `contributor_checkin` / `contributor_submit` prerequisite appear before registration | PASS | Rendered `/join` HTML includes the HTTPS MCP endpoint and connection-prerequisite heading before `<form>` |
| No automatic agent/schedule implied; ChatGPT plugin pending | PASS | Rendered copy explicitly says node creation does not install tools/start a recurring task, and warns verification is pending |
| Pause/revoke controls and privacy disclosure visible before registration | PASS for static disclosure | Newly deployed copy describes `contributor_set_status`, token retention, node data and aggregate telemetry before `<form>` |
| Email requires explicit consent | SOURCE-CONFIRMED; interactive behavior untested | Form source renders a checkbox when an address is entered and rejects email registration without consent |
| Actual MCP contributor tool availability and invocation | UNKNOWN | No independent MCP client handshake/check-in performed |
| Node registration, pause/revoke behavior, task claim/submission, useful completed task | UNKNOWN | No node or token created; no form submitted |
| Mobile rendering, screen-reader accessibility and comprehension | UNKNOWN | No device/assistive-technology acceptance performed |

## Outcome and follow-up

**Verified narrow result:** the pre-registration control/consent copy is now present in a publicly accessible production page. This is a truthful public information improvement, not an installation, contributor activation, verified accessibility pass, or beneficiary impact.

**Next action:** Have an authorized independent contributor execute the existing Tier-0 onboarding check by November 2, including actual browser/accessibility observation and a redacted evidence submission. Then separately run a permissioned MCP/registration/check-in/submission acceptance path without manufacturing adoption metrics.

**Restrictions:** No registration, private token, email, third-party contact, payment, or consequential write was performed in this acceptance check.
