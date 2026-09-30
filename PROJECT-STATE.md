# Humanity Loop Project State

**State timestamp:** 2026-09-30

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

## Current operating components

### Main hourly worker
- Title: **Humanity Loop — Hourly Worker**
- Cadence: hourly
- Canonical prompt: `AUTOMATION-PROMPT.md`
- Chat output is telemetry, not institutional memory.

### Foundry Alpha
- Live bounded multi-agent app surface:
  https://humanity-loop-foundry-alpha-0wls2s.v2.appdeploy.ai/
- AppDeploy hourly cron is currently disabled with `credits_exhausted`; the app itself remains deployed/ready.
- Core roles: Scout, Verifier, PM, Builder, 10th Man, Safety Governor, Outcome Tracker, Planetary Accountant.
- Specialist catalog: `ROLE-CATALOG.md`
- Do not claim unverified runtime enhancements are live.
- Do not wholesale-migrate the model-dependent Foundry to GitHub Actions; separate deterministic orchestration from provider-dependent execution first.

### Live independent apps
- Critical Guidance Delta UI/API:
  https://critical-guidance-delta-y7nzmd.v2.appdeploy.ai/
  - AppDeploy cron is disabled by `credits_exhausted`.
  - Credit-independent change detection now runs from `.github/workflows/critical-guidance-delta.yml`.
  - Canonical detector receipts: `runtime/critical-guidance-delta/`.
- Evidence Integrity Sentinel:
  https://evidence-integrity-sentinel-uip4nx.v2.appdeploy.ai/
  - AppDeploy cron remains enabled/healthy as of the latest reconciliation.
- CAP Clarity Check:
  https://cap-clarity-check-0jbjid.v2.appdeploy.ai/
  - Browser tool; no cron by design.
- CAP Daily Audit UI/API:
  https://cap-daily-audit-s0a2he.v2.appdeploy.ai/
  - AppDeploy cron is disabled by `credits_exhausted`.
  - Credit-independent daily audit now runs from `.github/workflows/cap-daily-audit.yml`.
  - Canonical audit receipts: `runtime/cap-daily-audit/`.
- Federal Policy Delta UI/API:
  https://federal-policy-delta-p49z0b.v2.appdeploy.ai/
  - AppDeploy cron is disabled by `credits_exhausted`.
  - Credit-independent official-source delta detection now runs from `.github/workflows/federal-policy-delta.yml`.
  - Canonical detector receipts: `runtime/federal-policy-delta/`.
  - Detection is intentionally separate from neutral legal-authority analysis.

### Durable research
- Undermind workspace configured.
- Humanity Loop folders include mental health, planetary systems, inner development, scientific integrity, and operations.
- Use `TOOLING.md` for research-stack routing.

### Project correspondence
- MOTHER project inbox: `mother.humanityloop@agentmail.to`
- Display identity: **MOTHER**
- Use for neutral project correspondence, contributor coordination, external responses, and failover alerts.
- Financial/legal commitments still require human handling.

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

## Public/social strategy

- **Humanity Loop** = institution.
- **MOTHER** = public social voice/persona.
- MOTHER should answer people, celebrate wins, show receipts, route useful ideas, and punch up rather than down.
- Movement language: `#AddANode` paired with plain-language explanations / `#HelpWanted`.
- Visual direction currently specified in `SOCIAL-DISTRIBUTION.md`; visual work can be revisited separately.
- X account not yet considered fully launched unless current external state proves otherwise.

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

## Current runtime resilience

- AppDeploy cron-credit exhaustion affected Foundry Alpha, CAP Daily Audit, Federal Policy Delta, and Critical Guidance Delta simultaneously.
- CAP Daily Audit has been migrated and live-validated on GitHub Actions.
- Critical Guidance Delta deterministic detection has been migrated and live-validated on GitHub Actions.
- Federal Policy Delta deterministic detection has been migrated and live-validated on GitHub Actions across all 17 configured official sources. The official GPO/LOC bill-status bulk-update feed replaces the Congress.gov homepage because the runner received HTTP 403 from Congress.gov.
- Evidence Integrity Sentinel remains healthy on AppDeploy.
- Foundry Alpha remains the unresolved runtime-credit dependency.

## Immediate continuity priority

If either master chat or hourly log hits a ChatGPT conversation limit:
- do not reconstruct manually;
- use `CHAT-CONTINUITY.md`;
- refresh this file from current durable state;
- bootstrap or migrate with the exact prompts there.
