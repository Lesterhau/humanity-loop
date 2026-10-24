# INTEND — clarify the contributor MCP connection step (2026-10-24 CDT)

Owner: Humanity Loop main hourly worker.
Tier: 0 — reversible, public-source onboarding copy only.
Target: `mcp-server/app/join/page.tsx`.
Observed gap: after creating a node, the onboarding page supplies a private token and recurring-task prompt but does not give the exact public MCP endpoint or an explicit prerequisite to connect that endpoint in an MCP-capable host. This may leave a first-time contributor with a prompt whose named tools are unavailable. ChatGPT plugin verification remains pending; do not imply plugin availability.
Intended mutation: add the documented production Streamable HTTP MCP endpoint (`https://humanity-loop.vercel.app/api/mcp`) and short host-neutral connect/verify/schedule instructions to the post-registration page, and clarify the ChatGPT host label. Do not modify registration, tokens, backend permissions, telemetry, or scheduled workers.
Acceptance: independently fetch updated GitHub source and verify endpoint, ordering, and plugin caveat. This is a source-level acceptance check only; do not claim a production browser acceptance test, new registration, or adoption.
Rollback: revert the single-page code commit.
