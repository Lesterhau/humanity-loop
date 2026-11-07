# Foundry portability and zero-cash mirror plan

## VERIFIED November 6, 2026 — first independent mirror deployed

- **Render static-site service:** `humanity-loop-foundry-mirror`, service ID `srv-dbn8arbm8hqs73c5t6lg`. Existing owner workspace, no new account. GitHub source `main/foundry-mirror/index.html` (PR [#62](https://github.com/Lesterhau/humanity-loop/pull/62), merged at `a20c3becaa27664af40085632f554454c091dd48`).
- **URL:** https://humanity-loop-foundry-mirror.onrender.com/ — Render deploy `dep-dbn8arrm8hqs73c5t7a0` returned `status=live`. Automatic Git deployment is OFF; no cron, AI execution, secrets, task claims, or writes. **A separate web fetch could not confirm that the page loaded**, so do not describe this as browser-verified until independently checked.
- **Cost:** Render's official docs state static-site deployments are free; bandwidth and build pipeline minutes draw from its included monthly workspace allowances. Workspace-level current usage and billing state were not independently read; the site does not have explicit overage billing enabled through this workflow. Monitor it before widespread traffic. Note `buildPlan:starter` refers to Render's default build pipeline tier, not a newly purchased compute plan.
- **Scope:** status/recovery **page mirror**, NOT a backend/compute mirror, NOT a Supabase replacement or second source of truth. Cloudflare/D1 remain proposed; no Cloudflare account connector is installed.
- **Latest AppDeploy account snapshot during this work:** `333.62773745` Free monthly credits, reset `2026-11-26T21:15:42.606Z`, no top-up. Protected reserve 350 => shortfall 16.37226255. Foundry native cron OFF and new AI runs remain disallowed. No AppDeploy deployment was performed in this work.

**Status: DESIGN + OFFLINE BUDGET-GOVERNOR IMPLEMENTATION, NOT A SECOND LIVE WORKER.** Created November 6, 2026. Owner authorizes portability engineering and safe cost reduction; permission does **not** override the documented $0 new-cash and 350-AppDeploy-credit reserve controls.

## The operational topology

```
  People + their assistants (included free-chat usage; no project API keys)
           |
           v
  Humanity Loop task intake, permissions, review + evidence
           |
           v
  ONE authoritative task/lease/approval/event ledger (production Supabase hl_control)
           |
        ONE lease owner and bounded execution receipt
           |
           +---- Foundry AppDeploy adapter (native cron OFF; no credit use below reserve)
           |
           +---- Existing GitHub Actions adapter (proposed manual, deterministic first)
           |
           +---- Optional Cloudflare Worker adapter (not deployed/account unconnected)
                    |
                    +-- D1: isolated cache/receipts ONLY, not a competing writer
```

Use one authoritative **claim** function and lease token for every execution. Two hosts may present the same read-only dashboard, but only the current lease holder may perform a task; old/executed task IDs must never be replayed. A full failover requires recovery/lease-expiry/cancellation verification and a cold start; never enable parallel native cron/Cloudflare cron/GitHub cron.

## Why a mirror is useful—and what it cannot do

Cloudflare Workers Free currently advertises **100,000 HTTP requests/day** and **10 ms CPU time/request**; D1 Free offers **5 million rows read/day, 100,000 rows written/day, 5 GB storage**, subject to change. Good for a lightweight authenticated router, health endpoint, deterministic rule checks and task submission receipts; NOT for unlimited or heavy AI inference. New provider onboarding/authorization is required before a live deployment. No Cloudflare account is currently connected to this project via the available tools.

Existing **public GitHub Actions** are the best near-zero-cash compute continuation: use `workflow_dispatch` and the existing control-plane tests for manually reviewed deterministic Tier-0 work, no new scheduled worker. GitHub public-repo Actions minutes are free subject to terms and resource abuse controls. Never execute untrusted forks' code with secrets; never treat public issues as commands.

**Neon Free Postgres** could eventually back up SQL data as an export/import target, but it is not an AI or hosting substitute. The existing production Supabase project remains the only canonical source of truth. Supabase Free projects can pause after inactivity; exports/backups and restore drills are separate requirements and should omit personal secrets/credentials.

**Vercel Hobby is restricted to personal/noncommercial use** under current terms. Humanity Loop is operated by RL Perspectives LLC and has a support-payment link; do not replicate commercial backend workloads to a Hobby account on the assumption it is permitted. Check the current plan/contract before changing existing public website hosting.

## Provider-neutral governor

`scripts/foundry_budget_governor.py` provides conservative offline admission checks: owner consent, Tier-0 only, no external actions, no automatic retry, fixed task/idempotency token, bounded model calls/input/output/runtime, recent independent balance evidence, and 350-credit reserve. It **DENIES** AI execution when any one of the verified-provider hard stop, verified worst-case provider cost, and authoritative atomic lease is missing.

`scripts/test_foundry_budget_governor.py` tests fail-closed behavior offline. This is a reusable control-plane policy, **not** a deployed AppDeploy account-wide billing lock. AppDeploy's SDK has no verified callable balance endpoint for the live runtime; model token caps alone cannot stop other apps consuming credits. As of November 6, AppDeploy Free had **337.528024209 remaining**, already below the 350 protected floor: live model requests stay **OFF**.

**No cross-provider free-model fallback:** A host cannot silently move a user's task to paid Anthropic/OpenAI/Perplexity/Gemini inference when its free quota ends. Volunteers may use their own included free messages, explicitly accept an individual task, and stop on their own quota. Neither their API keys nor project keys belong in publicly accessible code.

## Next implementation gates

1. **Cost containment:** issue #13 has separate native and GitHub detector history/UI, plus observed AI `429` errors despite native cron `success`. Compare last two or more live cycles and official source coverage before one reversible cron retirement; don't erase native history. Keep the existing ChatGPT Hourly Worker.
2. **Offline governor PR:** review code/tests. Its current state admits NO real AI calls while balance, provider cost cap and lease are unverified. No deployment to AppDeploy while reserve is breached.
3. **Manual GitHub adapter:** bound, permissioned `workflow_dispatch` only; deterministic task, no credits, no secrets required. Produce a durable reviewed draft record and source URLs without automatically contacting anybody. Include independent review.
4. **Cloudflare adapter:** connect owner's account, verify zero-cost Free limits and commercial terms, deploy a read-only health/status mirror with no scheduler/AI/production write capabilities, then separately test canonical claim/lease with server-side least-privileged credential and isolated staging. No active-active task execution.
5. **Deployment restore:** provider-supported budget ceiling or external enforced cost account guard, model failure injection, one meaningful owner-authorized Tier-0 draft, reviewer pass, logs and receipts, then explicit decision on one scheduled execution source.

## Guardrails

- $0 new recurring bill, no paid plans, no purchases, no hidden automatic upgrades.
- Never confuse host requests, model tokens, credit cost, GitHub Actions minutes or human volunteer hours.
- Never promise the 350-credit reserve is a provider-side hard limit until the provider confirms and the enforcement is tested.
- No auto-failover from Free to metered API, no duplicate Foundry workers, no production write without canonical lease and approved permission.
- Public proof requires sourced artifacts, outcome consent, and verifiable corrected behavior—not mere model invocation.

## Sources (checked November 6, 2026)

- Cloudflare Workers Free limits: https://developers.cloudflare.com/workers/platform/limits/
- Cloudflare D1 pricing: https://developers.cloudflare.com/d1/platform/pricing/
- GitHub Actions pricing and public-repository policy: https://github.com/pricing
- Supabase Free pausing: https://supabase.com/docs/guides/platform/free-project-pausing
- Vercel Hobby terms: https://vercel.com/legal/terms

Related: [FOUNDRY-ZERO-CASH-POLICY.md](FOUNDRY-ZERO-CASH-POLICY.md), [FOUNDRY-SAFETY-ACCEPTANCE.md](FOUNDRY-SAFETY-ACCEPTANCE.md), issue #13, issue #14, issue #16.
