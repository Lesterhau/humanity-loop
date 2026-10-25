# INTEND — contributor onboarding pre-registration control disclosure

Date: 2026-10-25 UTC
Owner: Humanity Loop main worker
Risk tier: 0, reversible public-page copy change only
Target: `mcp-server/app/join/page.tsx`

## Independent production observation
Read-only rendered HTML retrieval of https://humanity-loop.vercel.app/join on October 25 UTC confirmed the production page now displays the MCP endpoint, required contributor tool names, and plugin-verification caveat *before* the registration form. The page also renders the registration form. This is narrower than a full browser/MCP/registration acceptance test.

The public **pre-registration** form does not explain how a future contributor can pause or revoke a node, or summarize what registration stores. Current source puts those explanations **only after registration** in the successful registration view. The pilot task explicitly asks whether pause/revoke explanation is visible. No form was submitted and no registration, email or token was created.

## Intended bounded mutation
Add a concise pre-registration disclosure before the form explaining that after registering, the private token is used with `contributor_set_status` to pause, resume, or revoke; the node does not run automatically; and what limited node data/telemetry is stored. Make explicit that optional email requires separate checkbox consent. Preserve existing backend behavior, permissions, registration flow, token generation and privacy claims; do not introduce tracking. Repair a missing rendered space between the two tool names and 'before'.

## Verification and limits
Independently fetch the updated source after writing. A successful source commit is **not** production deployment, actual user comprehension, MCP tool availability, or a completed contributor task. Independently re-fetch the production page before claiming deployed copy. No fabricated node installs, acceptance submissions, or real-world impact.

Rollback: revert the single page change if inaccurate or confusing.
