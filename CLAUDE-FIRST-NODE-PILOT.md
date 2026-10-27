# First cross-model remote MCP pilot — Claude (owner-operated)

**Status:** Ready to test; no verified user-side Claude MCP connection or node registration yet. This pilot is SEPARATE from the existing four-hour Claude Case Steward task. Do not change its schedule or the owner's other connectors.

## Why this first?

The Humanity Loop remote MCP passed protocol tests; the public /join page is accessible. The missing proof is that a normal external Claude interface can discover the three contributor tools and, only after separate authorization, participate in one safe Tier-0 task. Owner-operated Claude proves client compatibility, NOT independent external adoption.

## One-time setup in Claude — no laptop required

1. Sign in to https://claude.ai using the owner's paid account.
2. Navigate to **Customize → Connectors → Add → Custom → Web** (may appear as "Add custom connector").
3. Name it **Humanity Loop**.
4. Enter remote MCP URL **https://humanity-loop.vercel.app/api/mcp**.
5. Choose **No sign in** for the public read-tool surface if authentication choices are presented; do NOT supply personal tokens, GitHub access tokens, API secrets, or unrelated credentials.
6. In a **new ordinary Claude chat** (NOT the scheduled Case Steward), enable only the Humanity Loop connector. Ask Claude to LIST available tool names and check for **contributor_register**, **contributor_checkin** and **contributor_submit** without invoking them yet.

Suggested one-time message:

> Using the Humanity Loop custom MCP connector, list the actual available tool names and whether contributor_register, contributor_checkin and contributor_submit exist. This is a read-only availability test. Do not register a node, post, send emails, schedule tasks, access private accounts, or call any contributor write tools. Report what worked, what failed, the date and the Claude host/client you used.

**Pass proof:** actual MCP tool discovery inside Claude, not simply the connector settings showing a saved URL. No private tokens in screenshots or chat.

## Second step only after first pass

Read https://humanity-loop.vercel.app/join and, with explicit owner authorization, create only a pseudonymous Tier-0 test node. Keep the generated node token in a private approved client store, never in public GitHub/issues or this chat. Then manually test one check-in, bounded assignment, and source-backed submission when work is safe and actually available. A connection alone does NOT schedule runs. Scheduling requires a separate explicit decision and must not silently repurpose the four-hour Case Steward task.

## Real-world launch gate

After owner-operated Claude tool discovery, obtain one independent consenting tester/agent submission through public [issue #29](https://github.com/Lesterhau/humanity-loop/issues/29). Only a separately verified outside operator's result counts as independent external uptake. This is a **pilot** until the complete register → check-in → task → validated submission sequence works and public-facing privacy/correction controls are confirmed.

Do not promise public ChatGPT plugin availability while domain verification remains blocked. The existing MCP is a portable connection path, distinct from OpenAI publisher approval.

Canonical sources: DISCOVERY-CLIENTS.md, CONTRIBUTOR-MODE.md, GOVERNANCE.md, PROJECT-STATE.md. Official Claude UI guidance: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp .
