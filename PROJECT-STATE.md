# Humanity Loop Project State

**State timestamp:** 2026-10-26 21:00 Central — AppDeploy credit reset, Foundry schedule safely paused, shared chats consolidated, launch blockers tracked

This is the compact restart snapshot. Detailed truth lives in the linked canonical files and ledgers.

## Mission

Build a vendor-neutral, distributed public-interest agent system that can:
- discover neglected problems and opportunities;
- verify evidence and novelty;
- build or coordinate useful interventions;
- connect promising external work to resources and people;
- track whether anything actually changed;
- learn from wins, failures, dead ends, and replications;
- help accelerate desirable H1→H2→H3 transitions while preserving human agency.

## Operating decision — October 20, 2026: execution leads

- **Mode:** verified, bounded public-interest **execution-first**, with maintenance as a safety/reliability floor and new building only when a real bottleneck warrants it. Working target ~60% direct execution/outcome verification, ~30% essential maintenance, ~10% targeted capability work; never treat these as measured quotas.
- Existing hourly worker's canonical `AUTOMATION-PROMPT.md` now enforces this choice while preserving human approvals for Tier-2 material impacts, limits on contact, truthful outcome accounting and mandatory security checks. The AppDeploy Foundry P1 and credit stoppage restrict THAT runner, not all authorized Tier-0/Tier-1 work.
- **First visible execution of the shift:** on Oct20 Humanity Loop independently reverified the VA Spanish current-rates mismatch (OT-002), sent a bounded new-evidence update in the existing project correspondence, and verified the outbound AgentMail message. No public correction yet verified; next outcome check Oct27. OT-004 Texas WIC was independently checked: the current Spanish entry page matches USDA 2026-27 guidelines, while a legacy URL currently returns HTTP403 to automated readers, so a claimed full correction or live misleading page would be premature.
- **Success definition:** independently confirmed corrected public guidance, useful accepted contributions, validated resource connections, or other beneficiary-level effects. Outreach/candidate creation/commits are intermediate outputs, not wins.

## MOTHER controlled intake pilot — October 21, 2026

- **Supervised synthetic email round trip independently PASSED:** a new, explicitly project-controlled test inbox sent a non-sensitive question about Spanish VA benefit-rate links into the approved MOTHER project mailbox. The receiver mailbox's original, source-checked supervised reply, handling of quoted prompt-injection content, and delivered reply in the independently queried sender mailbox were all verified, including `In-Reply-To` and two official current VA 2026 rate links.
- Canonical *sanitized* test receipt: `runtime/mother-pilot/2026-10-21-supervised-email.json`; detailed private send/readback receipts: Undermind `/humanity-loop/operations/2026-10-21-mother-supervised-pilot.md`; gate: GitHub [issue #17](https://github.com/Lesterhau/humanity-loop/issues/17).
- **Strict qualification:** This test was performed by the assistant in the active conversation. It did NOT demonstrate unattended hourly intake, autonomous triage/replies, responsiveness SLA, a consenting external adult tester, public X interaction, working Foundry, or mobile plugin onboarding. An internal synthetic sender is NOT an external beneficiary.
- Full MOTHER public launch stays **on HOLD**. Three X posts remain unpublished Airtable `Draft` records; no social publishing connector or consent to broadcast. Next proof: independent supervised intake flow that can surface a new incoming message *without this chat*, then separately a consenting real-person Tier-0 trial and a demonstrated response review queue.

## Research candidate — AI Epistemic Audit / Grok Science Accountability (October 21, 2026)

- The user supplied a conversation handoff proposing a neutral, scientific accountability audit of **public-facing @Grok answers on X**, specifically empirical claims on contested cultural/political subjects. This is NOT an effort to customize a private Grok account or a promise to change xAI's model training.
- **Current stage: Phase-0 research design; NOT an active public-correction campaign.** Canonical charter: [AI-EPISTEMIC-AUDIT.md](AI-EPISTEMIC-AUDIT.md); case-level data schema: [schemas/ai-epistemic-audit-case.schema.json](schemas/ai-epistemic-audit-case.schema.json); scoped [pilot issue #18](https://github.com/Lesterhau/humanity-loop/issues/18).
- First milestone is a pre-registered, read-only **12 contested plus 4 low-controversy** public Grok-claim observational sample, with source adjudication, controls, counterevidence, reviewer disagreements and evidence-calibrated scoring. **Zero actual claims or model corrections have been independently recorded yet** under this initiative; no empirical conclusion is authorized.
- **October 21 follow-on, TinyFish connected:** New [precommitted source-access amendment A2](research/ai-epistemic-audit/source-access-amendment-A2-2026-10-21.md) enabled direct, read-only original @grok post verification. Two authenticated-*source* (not signed-in account) public Grok posts were recorded as [AEA-2026-001](research/ai-epistemic-audit/cases/AEA-2026-001.json) and [AEA-2026-002](research/ai-epistemic-audit/cases/AEA-2026-002.json); the vaccine case is UNREVIEWED and the nuclear 80%+ global capacity-factor clause is **single-review provisional supported** against WNA's 2025 value 83.7%, with uncertainty and IAEA EAF-vs-capacity factor distinction. **2/16 posts captured, 0 public Grok challenges, no autonomous deployment; ECR undefined.** Direct public-source access is now feasible; unfilled and off-topic strata remain. See issue #18.
- **October 21 first collection cycle — documented access bottleneck:** Locked original [pre-registration](research/ai-epistemic-audit/preregistration-2026-10-21.md) before source searches; first public search returned unassigned unrelated results, recorded in [initial discovery log](research/ai-epistemic-audit/discovery-log-2026-10-21.json). Issued a prospective [source-access amendment A1](research/ai-epistemic-audit/source-access-amendment-2026-10-21.md) before a separately ranked fallback and stored all 72 returned positions in [A1 discovery log](research/ai-epistemic-audit/discovery-log-amendment-A1-2026-10-21.json). **None** corresponded to a `@grok` post ID within the original July 23–Oct 20 window by Snowflake-ID time inference; most were older, generic or off-topic. Exactly **0/16 accepted cases**, ECR **undefined**, no live challenges or X posts. Indexed search availability is **not** a measure of Grok accuracy. Public X advanced search requires a logged-in session; a permitted read-only browser/account connection or approved X data method is needed before the next *prospectively amended* collection method. See issue #18 for audit details.
- Long-term scope may include symmetric comparisons with other AI systems. The protocol measures claim correction and justified confidence, NOT adherence to a chosen political position or model-weight modification.
- X official automation rules require prior written permission for AI-powered public reply bots; no unsolicited, bulk or automated public replies. External challenges remain per-post human-review decisions under Governance and X rules. **MOTHER's public launch and Foundry safety holds are unchanged.** Avoid starting another persistent task or subscription solely to pursue this pilot; conduct research through existing authorized project capabilities.

## Live autonomous-growth audit — October 21, 2026, 10:20 PM Central

- **ChatGPT main Hourly Worker:** enabled, hourly; last invocation was `2026-10-22T02:38:47Z` (~9:38 PM CDT). This verifies the host triggered it, **not** that every instruction was carried out. Dedicated ChatGPT Foundry worker remains disabled; AppDeploy Foundry was last confirmed paused for `credits_exhausted` and its deployed P1 safety parser remains unverified as fixed.
- **Six Scout Mesh cells registered, no recent claims:** independent Supabase read-only query found all six `hl_control.scout_cells` active, last `last_run_at=2026-10-02T06:38:29Z`, next due October 3. Importantly the actual `hl_control.claim_due_scout_cell()` function **writes `last_run_at` at claim time**, not after research, so this field is **not an independent scan-completion receipt**. The sole `hl_control.scout_signals` entry is dated October 2, a verified data-center waterless cooling candidate; no independently verified October 3–21 Supabase mesh scan or new signal was found. **[P1 issue #19](https://github.com/Lesterhau/humanity-loop/issues/19)** tracks actual Scout recovery and claim-vs-complete redesign.
- **Specialist registrations are not proof of running bots:** 15 agent-role rows exist in `hl_control.agents`, including Scout/Verifier/PM/Builder/10thMan/Safety/Outcome and planetary specialists, but newest `last_heartbeat` was October 3. Four `hl_control.tasks` were marked complete by October 3. Zero active contributor-node registrations. Do **not** claim an independently growing bot fleet, successful spawning or contemporary Foundry execution from these stale rows.
- **Deterministic independent scan network works within bounds:** latest independent GitHub Ops Sentinel report `runtime/ops-sentinel/latest.json` `2026-10-22T01:48:57Z` has CAP, Federal Policy, Critical Guidance and Evidence Integrity Backup receipts all OK, but still warns missing `runtime/ops/hourly-worker.json`. These measure narrowly specified feeds, not full autonomous world-problem discovery.
- **Prompt correction performed:** canonical `AUTOMATION-PROMPT.md` updated Oct21 to prevent indefinite Scout starvation and to explicitly separate due-cell claim timestamps from verified research completion. Changes apply to subsequent scheduled worker runs when it successfully fetches GitHub; they do **not** establish a recovered Scout Mesh or guarantee that ChatGPT host executes every requested action. No automatic payments, further crons, uncontrolled recursive agents or unsafe Foundry restart authorized.
- **Database advisory:** Supabase schema inventory warns 14 private `hl_control` tables lack Row Level Security. Independent SQL checks of `anon`/`authenticated` roles found **no private-schema USAGE or SELECT** for sampled scout/tasks tables; public exposure is NOT independently established. Least-privilege review tracked under **[issue #20](https://github.com/Lesterhau/humanity-loop/issues/20)**. Do not bulk-enable RLS without safe policy/rollout checks.

## Humanity Loop ↔ Morrow reciprocal improvement (October 22, 2026)

- Owner explicitly authorized **independent, private-safe process comparison** between Humanity Loop (public) and Morrow Engine (PRIVATE). No merged operations, cross-repository token or private-data transfer. Canonical contract: `CROSS-PROJECT-RECIPROCITY.md`. Morrow's recent private GitHub commit metadata describes a separate read-only comparison implementation, but its independent scheduled run and receipt have **not** been verified here; never claim both directions operational from one project's run.
- **No new scheduler created:** Existing `.github/workflows/ops-sentinel.yml` invokes `scripts/reciprocal_audit.js --if-due` within its current watchdog schedule, bounded by a 7-day persisted receipt. Script reads only five allowlisted local PUBLIC Humanity Loop files and cannot access Morrow. Six `scripts/test_reciprocal_audit.js` regression tests cover no-op truth, due gate, status drift, Scout claim semantics, missing case handoff and no private access.
- **Initial tested run:** [GitHub Actions #77](https://github.com/Lesterhau/humanity-loop/actions/runs/39874749564) completed successfully October 22, including reciprocal audit step. Durable `runtime/reciprocal-audit/latest.json` at `2026-10-22T23:54:00Z` proposed `case-delegation-absent` (NOT an auto-executed fix). Actual separately verified repair: `CLAUDE-CASE-STEWARD.md` + Case Steward ownership and realistic trigger/cost gates in `AUTOMATION-PROMPT.md`, logged `runtime/reciprocal-audit/resolutions/2026-10-22.json`. Earlier commit `0823d8c963ecd593e035819291b883814f343232` fixed three stale native detector status assertions. Technical process improvements, not public-benefit outcomes.
- **Claude handoff state:** ready-to-configure **hourly lightweight scheduled task** with review of cases only when due (normally no more than one substantive rereview per case in four hours). No independent Claude connection or scheduled first run has been verified. Claude's paid chat plan does NOT establish metered API access or off-platform agent authority.
- Next reciprocal audit is **eligible** no earlier than ~`2026-10-29T23:54Z`, but GitHub scheduled runs can be delayed or skipped. The first run validates the implementation, **not recurring weekly reliability**. A genuinely bidirectional flow of new nonproprietary methods requires approved sanitized Morrow-to-Humanity-Loop proposals before publication.

## October 23: Claude coordination and defensive security scouting

- **Owner decision:** Keep Claude's existing **four-hour** scheduled Case Steward active. Do not pause the task, disable globally useful Claude connectors or change the owner's other services. Claude previously reported broad connector auto-approval, so read-only behavior remains an **instruction boundary rather than verified technical least privilege**. We are tracking this honestly without overriding the owner's chosen workflow.
- **GitHub outbound command channel created:** [CLAUDE-STEWARD-DIRECTIVES.md](CLAUDE-STEWARD-DIRECTIVES.md), revision `HL-CS-2026-10-23-01`, is the public-safe run-start dispatch that ChatGPT/Humanity Loop can edit and independently read back. The [CLAUDE-CASE-STEWARD.md](CLAUDE-CASE-STEWARD.md) specification now tells Claude to read it before every run, to check the CURRENT tracker (OT-010/011 closed, OT-003 review November 6), and to avoid use of unrelated write-capable connectors. **No direct API execution inside Claude, no proved Claude fetch/ack, and no verified Claude→GitHub case-result delivery yet.** One scheduled-task prompt update in Claude is needed to bootstrap the pull pattern; ordinary later commands can be updated through GitHub.
- **Defensive AI-swarm security Scout priority:** [AI-INFRASTRUCTURE-DEFENSE-SCOUT.md](AI-INFRASTRUCTURE-DEFENSE-SCOUT.md) now maps public CISA/ACSC, BIS, FS-ISAC and OWASP defensive initiatives and defines a scope for finding, verifying and responsibly supporting protection for critical infrastructure, banking and essential digital systems. Read-only starter landscape includes OWASP Agentic Security, the AI Security Solutions Landscape and crosswalk, plus financial-sector advisories, **none yet a verified support gap/partnership**. [Scout issue #21](https://github.com/Lesterhau/humanity-loop/issues/21) tracks the first completed, evidence-backed evaluation and possible connection. `SCOUTING.md`, `SCOUT-MESH.md` and `AUTOMATION-PROMPT.md` now incorporate it as a **cross-cutting lens**, not a new idle seventh Scout or paid cron. Respect six-cell recovery issue #19 and protect live infrastructure against unauthorized scanning or testing.
- **Audit truth:** GitHub Actions Case Steward receipt guard's first run [#40031977618](https://github.com/Lesterhau/humanity-loop/actions/runs/40031977618) passed validator/unit tests. That is **receiving-side preparation**, not confirmation Claude completed a case or transmitted it. Do not create placeholder receipts or claim MOTHER content was triggered.

## October 24 — Claude cloud setup verified by owner; trusted-base GitHub PR guard tested

- Owner's Claude screenshots report the external Case Steward task remains scheduled **every four hours**, and cloud setup successfully read the current public GitHub directive revision `HL-CS-2026-10-23-01`. Claude reports task safety rules fixed to **read-only, no connector tools, no pushes/PRs, no new repo access, and no scheduled-task changes**. These are task-instruction boundaries rather than independently proven connector-level enforcement. Claude reported earlier runs ended without errors but **could not access their transcripts to verify any completed case review**. The next scheduled review must prove actual case evidence and the fetched revision. Case results remain **session-only, not delivered** to Humanity Loop.
- Canonical [CLAUDE-STEWARD-DIRECTIVES.md](CLAUDE-STEWARD-DIRECTIVES.md) advanced to `HL-CS-2026-10-24-02`. GitHub delivers evolving case instructions only after Claude demonstrably fetches them in a scheduled run; the most recent revision has **not yet been independently acknowledged**. No additional owner-to-Claude chat prompt required for ordinary in-scope directions.
- **Security correction:** Claude identified a self-validation bypass: an untrusted receipt PR could modify the script that checked it. Fixed `.github/workflows/case-steward-receipt-guard.yml` to use a **trusted BASE** `pull_request_target` workflow, immutable BASE SHA checkout, read-only API token, and `scripts/check_case_steward_pr.js` verifying exactly one allowed PR file, `runtime/case-steward/latest.json`, plus strict receipt validation; PR-authored code is never executed. Includes seven adversarial PR gate tests plus six original receipt tests. Verified [GitHub Actions run #40091101957](https://github.com/Lesterhau/humanity-loop/actions/runs/40091101957) PASS; verified **actual PR-triggered** [run #40091262755](https://github.com/Lesterhau/humanity-loop/actions/runs/40091262755) PASS on explicitly synthetic [draft PR #24](https://github.com/Lesterhau/humanity-loop/pull/24), then **closed it unmerged**. No fake Claude receipt or external beneficiary impact.
- **Open gate:** The guard's actual PR verification works, but GitHub branch protection / rulesets requiring PR review, this check, and prevention of unreviewed direct pushes to `main` have **not** been independently verified or configured via the available tools. The current Claude task has **no write route**, so there is still **no end-to-end automated Claude→Humanity Loop handoff**. Do not grant broadly scoped GitHub push access or claim ingestion succeeded. [Issue #17](https://github.com/Lesterhau/humanity-loop/issues/17) tracks real integration.

## Current operational snapshot — October 26, 2026 (supersedes older incident statuses below)

**LIVE priority truth, independently checked Oct26 evening:**

- **AppDeploy reset confirmed:** Free monthly credit balance **934.738622052** as observed after reset; next reset **November 26, 2026, 21:15:42 UTC**. No credit purchase. Credit balance is dynamic; do not treat this number as continuously current. During the reset all **five** native schedules automatically reenabled; *earlier October 20 statements below describing all five disabled are historical snapshots, not current status*.
- **Foundry protected and source patch deployed:** Existing Foundry app `humanity-loop-foundry-alpha-0wls2s` safety-hold snapshot `1793066649944` disabled the cron, and subsequent source patch snapshot **`1793067626398`** deployed **ready**, with first-line-only verifier `VERDICT = PROCEED` and governor `GO` tests replacing multiline fail-open checks. Caught model errors now rethrow after failed-run persistence instead of returning misleading HTTP200. The deployed source was independently read back. Root `cron.json` remains **`[]`**, and current status lists no active Foundry cron. Dashboard displays PAUSED. **Issue #14 remains OPEN pending independent live-model/adversarial acceptance and reliable rollback before any intentional restart**. A code-level fix is not proof of safe unattended execution. Main ChatGPT hourly worker is independent.
- **Four other native AppDeploy detector schedules remain ENABLED** (CAP, Federal Policy, Critical Guidance, Evidence Integrity) and GitHub detectors run too. Their native app data/UI and GitHub fallback implementations are not automatically interchangeable; parity/single-scheduler ownership and credit-efficiency decision remain unresolved **issue #13 / #16**. Do not blindly disable a unique data source or claim parity is established. Compare coverage, independent receipts and impact before cutover.
- **GitHub hourly/scanners currently healthy:** latest `runtime/ops/hourly-worker.json` runAt `2026-10-26T23:23:57Z` records a documented South Asia education no-signal research cycle; the independent Ops Sentinel `runtime/ops-sentinel/latest.json` at `2026-10-27T00:03:58Z` reports `healthy` and fresh CAP/Federal/Critical/Evidence receipts. **Issue #15 is CLOSED**. Heartbeat proves a read-back record, not autonomous beneficiary impact.
- **Claude Case Steward:** owner has reported cloud schedule every 4h and live GitHub instruction retrieval; **no proven Claude→GitHub return receipt** at `runtime/case-steward/latest.json` (404 as of this check). Trusted-base PR handoff guard passed a synthetic PR test; branch protections and external delivery remain to verify. Case work stays co-owned by main worker until actual receiving path verified.
- **ChatGPT plugin:** Existing v0.2.4 submission domain verification **unresolved**; do not resubmit duplicate. Connected personal Gmail support chain now covers #16350435, #17565572 and fresh bot-created **#18377012** (Oct26 evening Central), without confirmed case merge or specialist resolution. Support follow-up already sent; newest AI support reply asked for exact private challenge token/raw response and Incognito/hotspot results. Never publish credentials/tokens in repo. See [shared-chat consolidation](operations/2026-10-26-chat-consolidation.md), issue #2.
- **MOTHER:** Controlled internal email pilot passed; social accounts and mobile installed plugin still unverified. Do not promise an open autonomous service; prepare limited, consent-based, accurate impact-based launch. Do not auto-post unsolicited replies.
- **Two prior chats:** both supplied shared pages were read and their unique information preserved in [operations/2026-10-26-chat-consolidation.md](operations/2026-10-26-chat-consolidation.md); there is no reason for future agents to re-read those threads for routine execution. Original private support attachments remain in Gmail, not the public repo.

## Current operating components

### Current automation truth
- As independently checked 2026-10-20, **Humanity Loop — Hourly Worker** remains enabled and the separate ChatGPT **Humanity Loop — Foundry** task remains disabled. All five native AppDeploy crons are now **disabled** due to exhausted credits, including Foundry; the three GitHub-based detectors still save canonical receipts. Old native last-status `success` does not verify full model work. See Ops Sentinel warning issue #15 for the missing worker heartbeat.
- Its scheduled-task wrapper reads `AUTOMATION-PROMPT.md` at the start of every run.
- Unrelated personal automations are outside Humanity Loop state and should not be modified by project maintenance.

### Main hourly worker
- Title: **Humanity Loop — Hourly Worker**
- Cadence: hourly
- Canonical prompt: `AUTOMATION-PROMPT.md`
- Chat output is telemetry, not institutional memory.

### Planetary worker division
- Always-warm `planetary_accountant` plus five demand-activated Planetary specialist families are live in Supabase.
- Review ledger: `hl_control.planetary_reviews`.
- Self-footprint gate: `hl_control.planetary_self_footprint_snapshot()`.
- Current telemetry status is insufficient; this explicitly blocks environmental-benefit claims/unbounded expansion rather than treating missing data as zero footprint.
- First Scout→Planetary handoff completed for water-free megawatt-rack cooling; decision is RESEARCH, not scale, pending lifecycle/production evidence.
- Canonical runtime: `PLANETARY-WORKERS.md`.

### STEEP+ Scout Mesh
- Live Supabase tables: `hl_control.scout_cells` and `hl_control.scout_signals`.
- Six-cell initial geography × language × domain matrix is active.
- One-cell transactional claim function is live and regression-tested after an initial ambiguous-column bug was repaired before accepted output.
- First verified signal recorded from the global English AI-infrastructure cell.
- Canonical runtime: `SCOUT-MESH.md`.
- Main hourly worker rotates at most one due cell per eligible Scout cycle; no-signal outcomes are valid.

### Passive contributor nodes
- Live onboarding path: `https://humanity-loop.vercel.app/join`.
- Supabase Edge Function `contributor-node` is deployed and active.
- Public node model: one-time registration + owner-approved recurring task + automatic scheduled check-ins.
- Installation alone does not self-start an LLM.
- Public nodes default to full bounded autonomy: authorized Tier-0 and Tier-1 work may run automatically with evidence/audit receipts; Tier-2 candidates require explicit human approval before execution; Tier-3 remains prohibited or specialist-controlled. Results still enter review before becoming canonical Humanity Loop state.
- MCP contributor tools are live and validated in the public server build; contributor onboarding now includes ChatGPT, Claude, Gemini, Kimi, Qwen, Perplexity, Grok, Mistral, DeepSeek-via-host, Z.ai/GLM-via-host, GitHub Copilot, and generic MCP-capable agents; issue #6 is closed completed.
- Optional setup email requires explicit one-message consent and is processed by the hourly worker.

### Contributor growth telemetry
- Privacy-safe node funnel telemetry is live in Supabase.
- Canonical spec: `NODE-GROWTH.md`.
- Funnel: join session → registration → scheduled check-in → task claim → submission → verified contribution.
- `/join` records one HMAC-hashed browser session plus coarse mobile/desktop classification; raw IPs, full user-agent strings, emails, and node tokens are not stored in funnel events.
- Registration/check-in/claim/submission/acceptance metrics come from server-side database transitions.
- Initial production baseline at activation: **0 external nodes / 0 verified contributions**.
- Transactional rollback test passed every post-registration stage without leaving test data.
- Contributor Node Edge Function version 3 is active; Vercel deployment containing the instrumented join page is green.

### Transactional control plane
- Supabase/Postgres project **Humanity Loop Control Plane** is live and healthy in `us-east-1`.
- Project ref: `jxtcccrlnhkcjfnwlfea`.
- Cost at creation: **$0/month**.
- Private schema: `hl_control`.
- Live tables: agents, tasks, approvals, events, dead letters, usage.
- Transactional task claiming uses `FOR UPDATE SKIP LOCKED`; heartbeat and expired-lease recovery primitives are live.
- Initial rollback self-test successfully claimed a task and established agent heartbeat/lease state.
- Supabase Security Advisor: **zero findings** after initialization.
- Canonical spec: `CONTROL-PLANE.md`.
- The Supabase control-plane reference implementation is live and tested. Source audit of the separately deployed AppDeploy Foundry worker on 2026-10-09 found it writes run records to its own AppDeploy database, not to the canonical Supabase control plane. Do not infer worker completion from absent Supabase events or scheduler success alone.

### Foundry Alpha
- Live bounded multi-agent app surface:
  https://humanity-loop-foundry-alpha-0wls2s.v2.appdeploy.ai/
- The Foundry app remains deployed/ready, but its independent native hourly cron is **DISABLED (credits_exhausted)** as of 2026-10-20. The separate ChatGPT Foundry task is still disabled. Actual bounded Foundry model execution and canonical receipt continuity are **NOT VERIFIED**. The deployed code still has fail-open decision parsing and returns HTTP 200 for caught model errors; do not blindly restart it. See issue #14.
- Core live roles include Scout, Verifier, PM, Builder, 10th Man, Safety Governor, Revision, Outcome Tracker, and always-warm Planetary Accountant. Role state/permissions/budgets are persisted in the Supabase control plane.
- Specialist catalog: `ROLE-CATALOG.md`
- Do not claim unverified runtime enhancements are live.
- Do not wholesale-migrate the model-dependent Foundry to GitHub Actions; separate deterministic orchestration from provider-dependent execution first.
- Continuity playbook: `FOUNDRY-RUNTIME.md`. The independent AppDeploy scheduler is **disabled by credit exhaustion**. Bounded fallback is permitted only with verified nonduplication, safety controls and durable completion evidence; do not reactivate insecure Foundry or a duplicate unsupervised worker. No working replacement is independently verified.

### Live independent apps
- Critical Guidance Delta UI/API:
  https://critical-guidance-delta-y7nzmd.v2.appdeploy.ai/
  - AppDeploy native `guidance-scan` cron is **disabled (credits_exhausted)** as of 2026-10-20. Independent GitHub Actions `.github/workflows/critical-guidance-delta.yml` still saves receipts. Implementations/baselines differ; do not casually reenable duplicate native scanning.
  - Canonical detector receipts: `runtime/critical-guidance-delta/`.
- Evidence Integrity Sentinel:
  https://evidence-integrity-sentinel-uip4nx.v2.appdeploy.ai/
  - Native `integrity-scan` cron is **disabled (credits_exhausted)** as of 2026-10-20; UI remains deployed but native AppDeploy database/history are not being updated. A separate **credit-free, public-metadata triage backup** now runs on GitHub Actions (`.github/workflows/evidence-integrity-backup.yml`), verified in live runs, using Crossref retraction metadata and Europe PMC citation links. Its latest saved report is `runtime/evidence-integrity-backup/latest.json`, and the durable unreviewed lead queue is `runtime/evidence-integrity-backup/review-queue.json`. This is partial coverage and does NOT synchronize with the AppDeploy UI/DB.
- CAP Clarity Check:
  https://cap-clarity-check-0jbjid.v2.appdeploy.ai/
  - Browser tool; no cron by design.
- CAP Daily Audit UI/API:
  https://cap-daily-audit-s0a2he.v2.appdeploy.ai/
  - AppDeploy native `daily-cap-audit` cron is **disabled (credits_exhausted)** as of 2026-10-20. GitHub Actions `.github/workflows/cap-daily-audit.yml` remains active and saved its latest verified 2026-10-20 receipt. Preserve separate native history/baseline during any future deliberate cutover.
  - Canonical audit receipts: `runtime/cap-daily-audit/`.
- Federal Policy Delta UI/API:
  https://federal-policy-delta-p49z0b.v2.appdeploy.ai/
  - AppDeploy native `daily-policy-scan` cron is **disabled (credits_exhausted)** as of 2026-10-20. GitHub Actions `.github/workflows/federal-policy-delta.yml` remains active and saved a 2026-10-20 canonical receipt. Its GPO/LOC source differs from the native AppDeploy Congress.gov scanner; preserve UI/history and reconcile before cutover.
  - Canonical detector receipts: `runtime/federal-policy-delta/`.
  - Detection is intentionally separate from neutral legal-authority analysis.

### Durable research
- Undermind workspace configured.
- Humanity Loop folders include mental health, planetary systems, inner development, scientific integrity, and operations.
- Use `TOOLING.md` for research-stack routing.

### Outcome tracking / agency correspondence
- Durable tracker: `OUTCOME-TRACKER.md`.
- Verified wins: `WIN-LEDGER.md`.
- New Humanity Loop government/public-agency outreach uses the project inbox with sender identity **Ryan Lester | Humanity Loop** and signature **Ryan Lester, Founder, Humanity Loop** rather than the MOTHER social persona or Ryan's personal Gmail.
- Ryan's personal Gmail is authorized only for retrieving legacy Humanity Loop agency replies unless separately authorized.
- Claimed fixes must be independently verified before closure/win status.

### Project correspondence
- MOTHER project inbox: `mother.humanityloop@agentmail.to`
- Email display identity: **Ryan Lester | Humanity Loop**
- Social/public narrative persona: **MOTHER**
- Use for neutral project correspondence, contributor coordination, external responses, and failover alerts.
- Financial/legal commitments still require human handling.

### Current operational workers
- Main hourly command worker: broad orchestration and maintenance.
- Dedicated ChatGPT Foundry automation: currently disabled; the independent AppDeploy scheduler is enabled, with productive execution not yet independently verified.
- Issue Steward: contract in `ISSUE-STEWARDSHIP.md`, executed by the hourly worker at least every 6 hours.
- Connector/Amplifier: contract in `CONNECTOR-BOT.md`, executed by the hourly worker at least twice daily.
- Agency Reply Steward: daily MOTHER + authorized legacy Gmail reconciliation inside the hourly worker.

### Connector execution state
- Executable contract: `CONNECTOR-BOT.md`.
- **OT-010:** Clarvia ASBL → NLnet Open Internet Stack funding call. Receipt: `runtime/connector/2026-09-30-clarvia-nlnet.json`. Outcome pending; next review 2026-10-07; stale threshold 2026-10-14.
- **OT-011:** GestureLabs/A3CP → GitHub Open Source Accessibility community + 2026 Accessibility Summit. Receipt: `runtime/connector/2026-10-02-gesturelabs-github-accessibility.json`. Targeted email sent/read-back verified; next review 2026-10-07; stale threshold 2026-10-14.
- Neither outbound connection counts as a win unless measurable useful downstream value is verified.

### Ranked GitHub issue execution
- Open issues are ranked before work by safety/risk reduction, architectural blocking value, live-outcome impact, completion leverage, tractability, evidence, and reversibility.
- #1 remote MCP: **closed completed** — public HTTPS MCP + JSON fallback, pinned/security-gated build, two independent local clients, and two-client live-endpoint acceptance.
- #3 bounded Foundry/control plane: **closed completed** — transactional Supabase runtime, leases/heartbeats/recovery/DLQ, persistent role identities, bounded inheritance, full role-path acceptance, durable receipts.
- #4 STEEP+ Scout Mesh: **closed completed** — six-cell geography × language × domain matrix, one-cell claim primitive, structured signals, first verified real signal, recurrence wired to hourly worker.
- #5 Planetary Systems workers: **closed completed** — always-warm Planetary Accountant, five demand-activated specialist families, review ledger, self-footprint gate, first real Scout→Planetary lifecycle review.
- #6 Contributor Mode onboarding: **closed completed** — live /join page, Supabase node gateway, owner-approved recurring automatic check-ins, bounded Tier-0 and Tier-1 automatic work within owner permissions, Tier-2 human review, quarantine, pause/revoke, one-setup-email consent, MCP contributor tools.
- #7 governance gates and #10 environmental break-even: **closed completed** from the prior pass.
- #2 discovery/publication: **open at the human-review boundary** — production MCP is live and two-client tested; official MCP Registry publication succeeded; portable Agent Plugin packaging and cross-client setup docs are committed; release **v0.2.4** is live with `humanity-loop-plugin-0.2.4.zip` attached. Remaining blockers are host-specific manual UI validation plus OpenAI publisher/domain verification, icon/demo assets, submission, review, and publication.
- #12 Connector/Amplifier: remains open pending independently verified useful external outcomes. Both OT-010 Clarvia→NLnet and OT-011 GestureLabs→GitHub Accessibility have sent exactly one factual follow-up each, independently verified 2026-10-10 UTC; both one-follow-up allowances are **exhausted**. Next outcome review/stale threshold 2026-10-14. Outbound correspondence alone is not a win. See `OUTCOME-TRACKER.md`.
- #11 Fork Watch remains intentionally open as the canonical notification thread. The scheduled Fork Network Scan succeeded on 2026-10-02 and found no new public forks.
- #13 Detector scheduler reconciliation: **open P1 operations**. AppDeploy native CAP/Federal/Critical crons and independent GitHub Actions schedules both remain enabled; preserving public UI/history and canonical receipts requires a tested cutover. GitHub CAP test-message/optional-instruction and WHO cosmetic-header fixes are committed and verified, but native AppDeploy scanner source parity remains pending.
- #14 Foundry safety-parser and truthful model-error status: **open P1 runtime safety**. Deployed parser remains fail-open and returns HTTP 200 on caught model failures; exact-source-matched repair passed 16 local parser regressions but is **not deployed** owing to existing AppDeploy safety-interception and reviewed-deployment requirement.
- #11 remains the intentionally open Fork Watch tracker; no other GitHub issues beyond #2, #11, #12, #13, #14 were open in this reconciliation.

### MOTHER social automation
- Airtable base `Humanity Loop — MOTHER Social` exists with an `X Queue` table for drafts/approved/posted/failed state.
- Airtable currently has no external social account authorized, so the X/Twitter action cannot be completed through the connector until Ryan authorizes @MotherFixes once in Airtable's UI.
- Do not pay for Metricool solely for X while a lower-cost native path remains viable.

### Current maintenance / known drift
- Humanity Loop README is refreshed to current operations.
- Ryan's GitHub profile README refresh subsequently succeeded and was verified after earlier intercepted attempts; the stale fallback should be treated as resolved.
- Three Humanity Loop issues remain open: **#2, #11, and #12**. #2 is blocked only on accountable human directory-submission/UI-validation steps; #11 is intentional infrastructure; #12 is outcome-pending rather than implementation-blocked.

## Current major architecture

- Bounded Foundry, no unrestricted recursion.
- 10th Man asks: **"If this idea wins, who loses?"** and distinguishes fatal flaws from manageable risks.
- Outcome tracking has stale thresholds and escalation.
- Assume ordinary error/chaos before bad faith.
- Verified wins route to `WIN-LEDGER.md` and MOTHER celebration candidates.
- Amplifier/Connector layer moves verified promising work toward grants, experts, compute, collaborators, institutions, or public support.
- Transition Barrier framework maps structural blockers between H2 pathways and H3 outcomes.
- Planetary Systems includes Humanity Loop's own compute/environmental break-even.
- Preventive mental health H3 remains active: fear/threat, anger/grievance, humiliation, disgust/dehumanization, regulation, trust, and prosocial capacity.
- Lifelong Learning, Inner Development, Country/Regional Nodes, Civic Engagement, and Foresight Transition workstreams are active architecture.
- GitHub fork watcher + daily public fork-network scan are enabled.
- Detached copy/copycat detection is a separate discovery problem.
- Multi-model direction includes OpenAI, Claude, Gemini, Perplexity, Kimi, DeepSeek, Qwen, and GLM where supported.

### OpenAI Plugins Directory submission
- Current public-plugin draft: **v0.2.4**.
- Package metadata and skill checks pass.
- MCP domain verification is externally blocked: the OpenAI portal reports a token mismatch even though the public challenge endpoint independently returns HTTP 200, `text/plain`, and the exact portal-generated token.
- Support escalation sent from Ryan's Gmail to `support@openai.com` on **2026-10-03** with screenshots and full reproduction details.
- The existing `Humanity Loop — Hourly Worker` now checks the exact Gmail support thread and notifies Ryan only when a new OpenAI reply arrives.
- Do **not** keep bumping plugin versions or modifying the verified challenge endpoint unless OpenAI requests a specific change or new evidence identifies a real endpoint defect.
- Issue #2 remains open as an **external OpenAI verification blocker**, not an implementation failure.

### Public-launch mobile gate
- MOTHER remains in maintenance-only mode until the **published Humanity Loop plugin is successfully exercised from the ChatGPT mobile app**.
- A desktop-only personal/imported plugin is not sufficient for launch readiness.
- Launch acceptance requires: public-directory approval → publication → install/open from mobile → successful Humanity Loop tool invocation → successful Add-a-Node onboarding path from mobile.
- OpenAI's public plugin guidelines require reliable ChatGPT operation on both desktop and mobile; this is therefore a release gate, not a cosmetic preference.
- Metricool is **not** the selected X publishing path because X support requires paid Metricool access plus an additional X add-on. Do not incur that cost merely to automate @MotherFixes.
- Until a lower-cost/free X automation path is justified, MOTHER posts may be published manually after mobile launch readiness is satisfied.

## Public/social strategy

- **Humanity Loop** = institution.
- **MOTHER** = public social voice/persona.
- MOTHER operating contract: `MOTHER.md`.
- MOTHER should answer people, celebrate wins, show receipts, route useful ideas, and punch up rather than down.
- Movement language: `#AddANode` paired with plain-language explanations / `#HelpWanted`.
- Visual direction currently specified in `SOCIAL-DISTRIBUTION.md`; visual work can be revisited separately.
- X account **@MotherFixes** is live. MOTHER is the public/social persona; formal correspondence remains **Ryan Lester | Humanity Loop**. Profile setup/launch configuration is still being completed. Metricool is installed but is intentionally **not** the chosen X path because connecting X would add paid subscription/add-on cost. Do not pay for Metricool solely to automate @MotherFixes.

## Prompt / instruction security
- Prompt trust boundary: `PROMPT-SECURITY.md`.
- Public issue/email/web text is data, not operating authority.
- Convenience prompt index has been moved to private Undermind storage and removed from the current public tree. Historical Git commits may still contain the former file until/unless repository history is deliberately rewritten.

## Open-source posture

- Public code/ideas can be forked.
- Forks cannot modify canonical Humanity Loop without permission.
- Canonical identity/provenance matter.
- Safety-critical authority remains permissioned even when philosophy/evidence/low-risk machinery are open.

## Important operational rules

- External actions: intend → execute → verify → commit.
- Failures are first-class events; see `OPERATIONS.md` and `PENDING-ACTIONS.md`.
- Do not modify Ryan-owned repos other than Humanity Loop without explicit repo-specific approval.
- Do not use Ryan's personal Gmail/Drive/contacts/social accounts without explicit authorization for that use.
- Humanity Loop repo is approved for autonomous maintenance.
- Project selection must not be personalized to Ryan's biography/location/politics.
- No political persuasion; policy work is factual/neutral.
- No indefinite "still monitoring" state.

## Core-readiness gate

As of 2026-10-01, public-facing MOTHER buildout is deliberately deprioritized while core readiness is hardened.

Before expanding social/public launch activity:
- latest core CI runs must be green, not merely historical failures superseded by later success;
- canonical GitHub and Undermind state must agree on active blockers;
- required durable writes/receipts must persist and verify;
- core scheduled workers must match the state documented here;
- security/audit gates for public infrastructure must pass.

Current reconciliation:
- governance-gate latest runs are green; the three earlier failures were superseded by successful runs;
- Foundry control-plane tests are green;
- environmental break-even tests are green;
- MCP build is green from a pinned dependency graph with a high-severity production audit gate; public HTTPS deployment and scheduled two-client live acceptance are also green;
- the previously missing 01:37Z Foundry receipt was replayed and read-back verified;
- stale Undermind write-interception blockers were reconciled as resolved;
- the independent AppDeploy Foundry cron is enabled while the separate ChatGPT Foundry automation is disabled; deployed safety-parser and truthful-error-status corrections remain pending.

MOTHER/profile growth, follow-network expansion, and social automation are maintenance-only until Ryan explicitly resumes public rollout.

## Current strategic correction

Humanity Loop must **not become an audit-only system**.

The target balance is:
- sensing/auditing;
- building;
- mobilizing resources;
- connecting people/institutions;
- removing transition barriers;
- implementing;
- tracking real outcomes.

Quarterly mission-drift audits should explicitly test whether auditing/infrastructure is crowding out real-world mobilization and implementation.

## Current durable source map

Use:
- `ACTION-LEDGER.md` for chronological actions;
- `actions.jsonl` for machine history;
- `WIN-LEDGER.md` for verified completed wins;
- `PENDING-ACTIONS.md` for unresolved external-action failures;
- `DEAD-ENDS.md` for rejected/retired paths;
- `PROJECTS/` for live project cards;
- `CHAT-CONTINUITY.md` for restart procedure.

## Current runtime resilience — October 20, 2026

- **P1 credit shutdown:** Native AppDeploy cron jobs for Foundry Alpha, CAP Daily Audit, Federal Policy Delta, Critical Guidance Delta, and Evidence Integrity Sentinel all returned `enabled=false`, `disabled_reason=credits_exhausted`. Applications remain deployed/ready; prior success timestamps are insufficient proof of actual scan/model outcomes. No funds were purchased and none of these crons were restarted.
- **Surviving GitHub scanner coverage:** CAP, Federal, Critical and the newly created bounded Evidence Integrity public-metadata backup have all completed live GitHub Actions runs with receipts October 20. Evidence backup originally identified one `unreviewed` possible downstream citation (preserved in its review queue); five Crossref retraction notices were not found in Europe PMC, recorded as `coverageGaps` rather than API failures. This is narrower than the disabled AppDeploy scanner and not connected to its UI/history. None of these jobs replace or safely restart Foundry.
- **Watchdog repaired end-to-end:** Ops Sentinel source's bold **not** safety warning was retained. Test-only commit `ddbdfec6583a5839538d18593590b1934f863339` and scoped on-push live-check workflow commit `e2613357a68ce9e93acf3726dec66d89bb4f893c` produced a successful run #59 and saved `runtime/ops-sentinel/latest.json` as **warning** with 3 detector receipts OK and missing ChatGPT worker heartbeat. It also opened **[issue #15](https://github.com/Lesterhau/humanity-loop/issues/15)**. This proves issue/report pipeline worked on that run; hourly cron schedule reliability is still unproven.
- **Unresolved:** `runtime/ops/hourly-worker.json` does not exist. Its absence is not proof the automation stopped. Worker prompt requires an independently read-back, truthfully sourced heartbeat every 3h; previous worker writes were safety-blocked. Alert #15 stays open until genuine evidence is recorded.
- **Foundry safety:** P1 issue #14 remains open: fail-open Verifier/Safety Governor parsing and HTTP200 swallowed model errors; patch prepared but not deployed. No independent, verified live Foundry replacement while credits are exhausted. Do not expand autonomous actions or run unsafe fallback.
- **Future parity issue #13:** Separate native/GitHub detector implementations still have different snapshots and UI histories; do not automatically reactivate all AppDeploy crons if credits return or claim the cutover finished.
- **Reliability ceiling:** GitHub scheduled workflows have shown major delay/drop events; a green source-triggered watchdog run does not establish hour-by-hour monitoring. Track actual scheduled-run coverage and verify alert notifications before declaring robust independence.

### Current GitHub ledger head
- Human ledger includes actions through at least **HL-069** (Oct20 public-guidance evidence update; outcome pending).
- Machine ledger `actions.jsonl` contains **69 unique well-formed actions**, through HL-069 (local JSON syntax + unique-ID readback confirmed; pipeline validator status not independently checked on this change).
- Ledger validation succeeded after both HL-067 (official registry/release packaging) and HL-068 (GestureLabs Connector execution).
- GitHub mutation capability is currently working. The 2026-10-01 recovered Foundry receipt write was independently read-back verified, and the corresponding Undermind failover record was resolved.

## Immediate continuity priority

If either master chat or hourly log hits a ChatGPT conversation limit:
- do not reconstruct manually;
- use `CHAT-CONTINUITY.md`;
- refresh this file from current durable state;
- bootstrap or migrate with the exact prompts there.
