# Humanity Loop public ChatGPT plugin — publisher recovery

**Prepared November 9, 2026. Status: local plugin package and public MCP server ready for renewed verification, NOT directory-published. No paid subscription, account connection, private review portal operation or public installation claimed.**

## Why volunteer onboarding is blocked

As of Nov 9, **ordinary ChatGPT Free/Go/Plus users cannot rely on adding arbitrary full-write remote MCP servers**. The current official [Connecting custom MCP servers in ChatGPT](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) documentation limits workspace-level full MCP custom plugin creation to Business and Enterprise/Edu administrators and permitted developers, on web. Published plugins can be installed by eligible users once approved. Until our public plugin is approved, offer [the no-connector manual volunteer path](https://humanity-loop.vercel.app/try), which DOES NOT register a node.

## Verified local evidence

- The public server is `https://humanity-loop.vercel.app/api/mcp`. Existing GitHub CI tests the official MCP TypeScript client and an independent raw Streamable HTTP client.
- OpenAI domain verification requires the **currently displayed portal token**, served as **exact plain text bytes** from `https://<challenge-origin>/.well-known/openai-apps-challenge`. We currently track the challenge token in `mcp-server/public/.well-known/openai-apps-challenge`, the app route, and a Vercel rewrite. These copies matched on Nov 9.
- A read-only public fetch on Nov 9 confirmed the expected token was returned at the canonical well-known path. This does NOT prove the publisher portal is testing the same hostname or challenge token; the alternate bare `/openai-apps-challenge` path was not reachable through that fetch service.
- New CI `mcp-server/scripts/test-domain-challenge.mjs` checks **both** routes under the built Next.js server: HTTP 200 without redirect, `text/plain`, exact raw bytes, no newline, and the five required positive/three negative plugin review cases. It prints no token. Any CI failure is a concrete compatibility defect to fix.
- Public plugin manifest v0.2.5 and onboarding skill now match Stage-0: a single manual Tier-0 task, quarantined result, no recurring runs; personal ChatGPT alternative `/try`.

## Publication blocker and owner action

GitHub [issue #37](https://github.com/Lesterhau/humanity-loop/issues/37) records OpenAI Support cases **#16350435, #17565572, #18377012**. As of its Oct 28 record, support asked for current **exact token**, raw challenge response including newline, Incognito and alternate-network checks. We cannot confirm those portal-specific checks were completed or that the publisher status has changed. No fresh reply is sent from this file.

Owner (or an authorized human logged into the verified publisher organization) should:
1. Open the **existing** Humanity Loop draft in the ChatGPT Plugins publisher portal (don't create an unlinked duplicate).
2. Under `MCPs → Connect`, copy the **current challenge URL, exact token, and any issue codes**, including the verified developer identity and domain; do **not** share account passwords or API secrets.
3. Verify hostname exactly matches the URL where the token is hosted and that production returns only current token bytes, HTTP 200 `text/plain`, no redirects or newline. If the portal challenges a different hostname, update the actual matched origin rather than assuming the old `vercel.app` host passes.
4. Click `Reconnect` or `Rescan` only after the checks pass; inspect discovered tool list and any held tool metadata findings. The published connection may require review of risky `contributor_register` / `contributor_submit` write scopes.
5. If publisher still denies domain proof while live response and token match, send **one precise support reply** with current screenshot, anonymized request/response headers, exact URL, status, challenge token match and timestamp, plus the three existing case IDs; request a human engineering review.
6. Finish plugin review, including five positive and three negative cases and optional walkthrough, with accurate manual-only scopes. After approval, the owner explicitly publishes; don't imply automatic directory approval or a public listing.

## Cannot conclude from current evidence

- That the OpenAI directory accepted Humanity Loop, or that any Facebook volunteer can already install it.
- That the previous verifier is stuck due to a server bug (host/token mismatch or portal-side review is still possible).
- That a local MCP registry `server.json` publish equals an OpenAI-approved ChatGPT plugin.
- That token count is carbon impact or that a projected environmental payback proves any real-world benefit.

**Until directory approval:** the short `/try` manual pilot is the practical participation path for personal ChatGPT users. Manual results must be labeled separately from registered nodes and independently reviewed.
