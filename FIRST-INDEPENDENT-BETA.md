# First independent contributor beta — invitation-only test packet

**Status:** Early pilot; not evidence of a working external contributor. **Scope:** one consenting, non-owner adult using their own MCP-capable host; start with a small group of **3–5** volunteers, not an open recruitment campaign. No stipend, school/service credit, or guaranteed Impact Passport credential is offered. This is separate from the owner's [Claude pilot](CLAUDE-FIRST-NODE-PILOT.md).

## What the tester should know first

- The public remote MCP endpoint is `https://humanity-loop.vercel.app/api/mcp`. The ChatGPT plugin/publisher verification is **not complete**; do not assume the plugin is available. Use only an MCP host that explicitly supports connecting to a remote server and displaying tool results.
- Connecting a tool **does not** authorize background work or create a recurring schedule. **Do not schedule anything for this one-time beta.**
- This test uses **Tier-0 read-only research**. No agency contact, account creation on external sites, form submissions, login, access-control bypass, payment, private documents, or automated public posting.
- The contributor token is a **bearer secret shown once** by registration. Tool responses may remain in your host's chat history. Use a private, trusted chat and **never** put the token in a public issue, screenshot, recording, email, or shared transcript. Do not give Humanity Loop unrelated account credentials.
- Participation is voluntary; stop any time. Do not send personal information or unredacted screenshots. You can pause or revoke the node with the `contributor_set_status` tool.

## One-time test (do not fabricate any step)

1. **Discover only.** In your own MCP host, connect to the URL above. Ask the host to list actual server tools. Confirm `contributor_register`, `contributor_checkin`, `contributor_submit`, and `contributor_set_status` are present. If the host cannot connect, record the exact error without sharing secrets and stop.
2. **Register only with consent.** Call `contributor_register` with `capabilities: ["web"]`, `languages: ["en"]`, a non-sensitive `host` label, and **`risk_permissions: ["tier0"]`**. Do **not** provide an email or consent to a setup email for this test. Keep the returned node token private. If the tool refuses, record the non-sensitive error and stop; do not create repeated test identities.
3. **Check in once.** Call `contributor_checkin` using your private `node_token` and `capabilities: ["web"]`. Record only the assigned `work_id`, task title, risk tier, and lease/expiry (not the token). If no work is offered, report `idle` truthfully and stop. Never invent a task.
4. **Do the assigned Tier-0 task.** The intended first useful task is the [Texas WIC legacy Spanish-page browser check](https://github.com/Lesterhau/humanity-loop/issues/46), if the gateway actually assigns it and it remains current. Read the issue's [source-checked task note](https://github.com/Lesterhau/humanity-loop/issues/46#issuecomment-6511904664). Use an ordinary browser only, without VPN/proxy tricks or bypasses. Capture UTC time, final URL, whether the page/redirect/error is visible, and the one- and two-person income amounts *only if visible*. A 403 or unclear result is `unknown/source_blocked`, **not** proof of a defect or correction. If a different legitimate Tier-0 assignment arrives, follow its exact safe scope instead.
5. **Submit once.** Call `contributor_submit` with the actual assigned `work_id`, your private `node_token`, a factual `result` object (observation/status, UTC timestamp, final URL, browser/device class), `evidence` containing only public-source URLs and redacted observations, and a candid `uncertainty` explanation. If submission fails, do not claim completion; retain the error privately for the reviewer.
6. **Stop and report the test outcome.** Do not create a recurring task. If you want to leave, call `contributor_set_status` with `action: "revoke"` using the token; if you want the maintainer to review your submitted result first, leave the node as-is or pause it. Do not publish the token or raw chat transcript.

## What the maintainer must verify

The reviewer for [acceptance issue #33](https://github.com/Lesterhau/humanity-loop/issues/33) must independently establish **(a)** genuine non-owner consent and host/tool discovery, **(b)** registration and check-in receipts, **(c)** a real eligible assignment and redacted submission, **(d)** independent review of the observation against official sources, and **(e)** pause/revoke behavior if exercised. A successful protocol-only CI test or a saved connector URL does **not** satisfy this. Public notes should contain only redacted evidence and status; store private receipts in an authorized private location. Count a useful completed contribution only after review, and beneficiary impact only after separate verification.

**Current limitations:** The first task is time-sensitive; the [#46](https://github.com/Lesterhau/humanity-loop/issues/46) assignment must be checked for validity before testing. The gateway may return a different task or no task. No independent human has yet passed this sequence as of the drafting date, October 30, 2026.

Sources: [Contributor Mode](CONTRIBUTOR-MODE.md), [MCP server implementation](mcp-server/app/api/mcp/route.ts), [governance](GOVERNANCE.md), [independent acceptance issue #33](https://github.com/Lesterhau/humanity-loop/issues/33).
