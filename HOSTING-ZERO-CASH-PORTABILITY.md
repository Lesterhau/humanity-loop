# Humanity Loop — zero-cash hosting fallback and cutover gate

**Prepared November 8, 2026; read-only assessment. No migration, DNS change, subscription, signup, provider authorization, or paid plan approved.**

The live Humanity Loop site is a Next.js **16.4.3 App Router** application with its own remote MCP route (`mcp-server/app/api/mcp/route.ts`, `mcp-handler@2.2.0`) and public join pages. Supabase currently maintains private contributor state and the contributor gateway. A static-only hosting export would break the **live MCP route** unless the API is separately hosted and its protocol, CORS, authentication/metadata, absolute URLs and OAuth/client compatibility are safely restored.

## Current live-state evidence
- Public site: https://humanity-loop.vercel.app/
- Production Vercel project: `humanity-loop` (`prj_ezHtQiZXCoKGPVXxAGczArqAqwwq`); most recent sampled deployment `READY`.
- Connected Vercel project/team reads exposed **project/team names but no billing plan**. Team plan **UNKNOWN**, not confirmed Hobby and no proven contract violation. Owner uses RL Perspectives, LLC for project governance and there is a voluntary, non-tax-deductible support link.
- [Vercel Terms](https://vercel.com/legal/terms), section "Hobby Plan", limits it to personal/non-commercial use. [Vercel Fair Use Guidelines](https://vercel.com/docs/limits/fair-use-guidelines) include interpretation of financial benefit and nonprofit/donation exceptions; read the current text and obtain provider clarification about the user's exact LLC/support usage before declaring a violation.
- Do not move, break or take down the working site merely because the plan field is absent.

## Alternative A: Netlify Free, full Next.js
- [Official Netlify Free plan announcement](https://www.netlify.com/blog/introducing-netlify-free-plan/) expressly permits **commercial projects**, which is a concrete advantage if this is deemed commercial.
- [Current pricing](https://www.netlify.com/pricing/) and [credit documentation](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/): Free uses **300 credits/month, hard cap, no auto recharge**; usage can suspend service. Do **not** import the old plan's "100GB/300 build minutes" assumptions into the current credit system.
- [Netlify Next.js](https://docs.netlify.com/build/frameworks/framework-setup-guides/nextjs/overview/) supports full Next.js framework hosting but **this project's streaming MCP route has not been smoke-tested there**; verify HTTP protocol/multi-request session behavior and response timeouts, edge vs function handling, streaming and CORS with real MCP clients before considering cutover.
- Setup requires an owner-approved connected Netlify workspace or account. Do not create paid services, auto recharge or multiple production deployment loops.

## Alternative B: Cloudflare Workers, full Next.js
- [Cloudflare Next.js guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/) recommends **vinext**, a **beta** Vite/Next.js compatibility layer, and the non-destructive `npx vinext check` / `vinext init` path. The existing App Router and route handlers are listed as supported; that is **not proof** our full `mcp-handler` streaming endpoint works.
- [Cloudflare's Vercel-to-Workers migration guide](https://developers.cloudflare.com/workers/static-assets/migration-guides/vercel-to-workers/nextjs/) provides an official path for an existing app. Model vendor compatibility and plan limits are separate considerations; obtain current Workers free-tier/terms evidence and verify no prohibited payment-card collection before choosing.
- Worker runtime differs from Node/Vercel; require a non-production compatibility run pinned to reviewed dependency versions and check MCP streaming, SSE/Streamable HTTP, module dependencies, origin rewriting, auth/return URLs, source maps, and fail-safe timeouts. Never begin an unreviewed production `vinext init` / DNS switch.

## Non-disruptive cutover requirements

1. **Owner checks actual Vercel billing plan** in authorized dashboard (connector does not expose plan) and gets authoritative explanation of the permitted use if ambiguous. No speculation.
2. Choose a permitted $0 host, verify available no-card signup/account, usage/credit hard caps, build/requests/quota, legal commercial/LLC terms and data processing. Estimate 5-node beta and future growth separately. Owner authorizes any account connection.
3. Create **isolated preview only** with no real participant token/service secrets (use approved staging); test homepage, `/beta`, `/join`, `/api/mcp` tool discovery, manual checkin/claim/submission with **synthetic staging records**, pause/revoke, CORS/streaming, redirects, error paths and any health/SEO / sitemap links.
4. When preview works, obtain separate explicit owner approval for real routing/DNS + production secrets; stage a **reversible** cutover, maintain old host until new live flow verified and use a documented rollback window.
5. Monitor real 5xx/4xx, request latency, credit consumption and data correctness. Document honest public outcomes; do not pretend that a free host is a 1,000-node solution.

## Decision / blocker

**No migration recommended yet.** The correct next owner action is verifying the **actual current Vercel team plan** and permitted use. After that, Netlify Free is a plausible zero-cash fallback to test first; Cloudflare Workers/vinext is another option but currently beta and more technically disruptive. Both must preserve the live MCP endpoint and separate private Supabase gateway. This is issue [#57](https://github.com/Lesterhau/humanity-loop/issues/57), not a finding of actual policy breach.
