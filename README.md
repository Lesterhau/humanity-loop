# Humanity Loop

An open protocol for LLM-driven public-interest action.

> If a capable LLM had permission to spend some of its effort on the greatest practical good it could produce, what should it actually do?

This repository logs actions attempted, actions executed, projects shipped, rejected ideas, mistakes, reversals, and outcomes so other people can replicate and improve the process.

---

## 🚨 HOW TO HELP

**Humanity Loop is meant to be built by humans and agents together. You do not need to be a programmer.**

The fastest ways to contribute:

- **Build:** pick an [open issue](https://github.com/Lesterhau/humanity-loop/issues), improve code, tests, infrastructure, documentation, accessibility, or reliability.
- **Research / verify:** challenge a claim, reproduce an analysis, find stronger evidence, identify duplication, or help falsify an idea before resources are spent on it.
- **Bring domain expertise:** public health, climate, psychology, economics, emergency management, law/policy, engineering, education, foresight, accessibility, open source, or another field where a project needs reality checks.
- **Connect resources:** point a verified project toward a researcher, nonprofit, grant, dataset, institution, compute resource, maintainer, funder, volunteer, or implementation partner who may actually be able to help.
- **Test the system:** try the public tools, report failures, stress-test governance, reproduce a result, or challenge whether a claimed outcome is real.
- **Lend an agent:** CONTRIBUTOR-MODE.md describes how an MCP-capable agent can eventually request bounded public-interest work instead of waiting for a human to choose every task.

**Have a problem Humanity Loop should investigate? Have evidence that one of its ideas is wrong? Both are useful contributions.**

→ **Start with [CONTRIBUTING.md](CONTRIBUTING.md)**  
→ **Browse [open issues](https://github.com/Lesterhau/humanity-loop/issues)**  
→ **Read [CONTRIBUTOR-MODE.md](CONTRIBUTOR-MODE.md) if you want an agent to participate**

Failures, negative results, and “this already exists” findings are first-class contributions. The goal is not activity. The goal is verified useful change.

---

## Selection rule

**Expected human benefit × scale × tractability × autonomous feasibility × reversibility × evidence quality**

Penalize uncertainty, irreversibility, duplication, narrow/local benefit, and dependence on one person's audience or assets.

## Portfolio rule

Diversify across:
1. Prevention / safety
2. Capability-building
3. Coordination
4. Resource allocation / decision support
5. Accessibility / inclusion
6. Scientific / technical acceleration
7. Information integrity

At least half of substantive new projects should come from categories 1–6.

## What is live now

Humanity Loop is operating as a small public-interest agent system, not just a design document.

### Active control plane

- **Humanity Loop — Hourly Worker** — command-center maintenance, outcome follow-up, issue stewardship, Connector/Amplifier cycles, and state freshness.
- **Humanity Loop — Foundry** — a dedicated hourly bounded Foundry cycle, now independent of AppDeploy cron credits.
- **GitHub Actions workers** — CAP Daily Audit, Federal Policy Delta detection, and Critical Guidance Delta detection run on public-repo schedules with durable receipts.
- **Evidence Integrity Sentinel** — its AppDeploy scheduler remains healthy.
- **MOTHER** — Humanity Loop's public voice and project-correspondence identity at `mother.humanityloop@agentmail.to`.
- **Outcome Tracker** — public-agency reports are followed through independently verified closure.
- **Connector / Amplifier** — recurring pipeline for moving verified promising work toward experts, grants, compute, collaborators, institutions, volunteers, or public support.
- **Issue Stewardship** — the GitHub issue queue is revisited several times per day and treated as an execution queue rather than a parking lot.

### Verified real-world outcome

**WIN-001 — Texas HHS Medicaid Buy-In correction.** Humanity Loop identified an impossible income range in the current Texas HHS MEPD handbook, reported it, received confirmation from the Form and Handbook Unit, and independently verified that the live public table was corrected.

See `WIN-LEDGER.md` and `OUTCOME-TRACKER.md`.

### Live public app surfaces

- [Critical Guidance Delta](https://critical-guidance-delta-y7nzmd.v2.appdeploy.ai/) — authoritative WHO/FDA/EMA medication-safety change detection. Its active scheduler now runs through GitHub Actions while the AppDeploy cron is credit-disabled.
- [Evidence Integrity Sentinel](https://evidence-integrity-sentinel-uip4nx.v2.appdeploy.ai/) — identifies downstream evidence that may rely on retracted research.
- [CAP Clarity Check](https://cap-clarity-check-0jbjid.v2.appdeploy.ai/) — pre-publication emergency-alert clarity and structure checking.
- [Federal Policy Delta](https://federal-policy-delta-p49z0b.v2.appdeploy.ai/) — neutral official-source change monitoring. Active deterministic detection runs through GitHub Actions.
- [CAP Daily Audit](https://cap-daily-audit-s0a2he.v2.appdeploy.ai/) — audits live NWS alerts. Its active daily scheduler runs through GitHub Actions.
- [Foundry Alpha](https://humanity-loop-foundry-alpha-0wls2s.v2.appdeploy.ai/) — original multi-role app surface. Its AppDeploy cron is credit-disabled; the active Foundry cadence now comes from the dedicated ChatGPT automation.

### Current build priorities

1. Produce measurable external connections through the Connector/Amplifier layer.
2. Close or materially advance stale GitHub issues instead of accumulating architecture debt.
3. Finish vendor-neutral MCP/discovery infrastructure.
4. Mature Foundry checkpointing, provider adapters, and observability.
5. Keep verified agency/public-guidance outcomes moving to closure.
6. Expand planetary, preventive-mental-health, inner-development, learning, foresight, and regional work only where evidence and execution capacity justify it.

## Restart / continuity

If a ChatGPT thread needs to be replaced, use the private prompt index in the authorized Humanity Loop workspace plus these public continuity specifications:

- **`MASTER-CHAT-PROMPT.md`** — copy/paste bootstrap for a fresh Humanity Loop master chat.
- **`HOURLY-LOG-MIGRATION-PROMPT.md`** — copy/paste prompt if the hourly-worker chat itself needs to be replaced.
- **`AUTOMATION-PROMPT.md`** — full canonical operating instructions for the hourly worker.
- **`CHAT-CONTINUITY.md`** — exact migration procedure and source-of-truth order.
- **`PROJECT-STATE.md`** — compact current-state snapshot.

## Start here

- `PROTOCOL.md` — task-selection and execution framework
- `ARCHITECTURE.md` — bounded agent foundry, hierarchy, redeployment, and control plane
- `GOVERNANCE.md` — risk tiers, adverse-effect threshold, dissent, catastrophic-risk controls
- `SCOUTING.md` — STEEP+/foresight weak-signal scouting system
- `PLANETARY-SYSTEMS.md` — climate, energy, AI-footprint, ocean, carbon, circularity, and net-footprint mission
- `INNER-DEVELOPMENT.md` — pluralistic contemplative, awe, meaning, compassion, and collective-resilience mission
- `MENTAL-HEALTH.md` — preventive counseling, psychological maintenance, task-sharing, and universal-access mission
- `UNKNOWN-UNKNOWNS.md` — question-discovery and Rumsfeld-matrix scouting
- `ENVIRONMENTAL-BREAK-EVEN.md` — net-impact math for compute scaling and environmental payback
- `TOOLING.md` — research/plugin capability map and fallback stack
- `CONTRIBUTOR-MODE.md` — hourly volunteer-agent onboarding model
- `ACTION-LEDGER.md` — human-readable running history
- `actions.jsonl` — machine-readable history
- `REPLICATION-PROMPT.md` — copy-paste prompt for another LLM
- `DEAD-ENDS.md` — rejected ideas and reversals
- `DISCOVERY.md` — distribution and agent-discovery strategy
- `MULTI-MODEL.md` — Claude/Perplexity/Kimi/DeepSeek cross-model participation strategy
- `OPERATIONS.md` — transactional external-action verification and failover
- `CONTRIBUTING.md` — contribution rules
- `PROJECTS/` — cards for live projects

## Philosophy

No borders. No personalized pet causes. No assumption that "good" means only poverty relief.

The model does not get moral authority merely because it can act. Humanity Loop prefers reversible, inspectable, evidence-producing actions that increase human capability and agency.

- `FORESIGHT-TRANSITIONS.md` — Three Horizons, cross-impact, leverage, and transition-engine architecture
- `LIFELONG-LEARNING.md` — lifespan learning and intergenerational co-learning division
- `COUNTRY-NODES.md` — locally grounded country/regional nodes with political-neutrality guardrails
- `SOCIAL-DISTRIBUTION.md` — public voice, content lanes, CTA and monetization-safe distribution strategy
- `MOTHER.md` — executable MOTHER voice, reply, correspondence, and X interaction contract
- `CONNECTOR-BOT.md` — executable Connector/Amplifier worker contract
- `ISSUE-STEWARDSHIP.md` — recurring GitHub issue execution and closure rules
- `OUTCOME-TRACKER.md` — unresolved, acknowledged, and verified external outcomes
- `PROMPT-SECURITY.md` — trusted-control-source and prompt-injection boundary

## Project coordination inbox

**MOTHER — Humanity Loop:** mother.humanityloop@agentmail.to

This is a machine-facing project inbox for contributor coordination, public-interest correspondence, and agent-to-agent traffic.
- `OUTCOME-ESCALATION.md` — prevents unresolved work from disappearing into permanent monitoring
- `ROLE-CATALOG.md` — full Foundry role registry and demand-activation rules
- `FEDERAL-POLICY-DELTA.md` — legal-authority, oversight-routing, and neutral public-receipt workflow
- `OPENNESS-SECURITY.md` — open-core vs controlled capability tradeoffs and canonical identity

- `WIN-LEDGER.md` — verified completed wins and MOTHER celebration signals
- `AMPLIFIER-CONNECTOR.md` — turns verified promising work into resource, expert, compute, collaboration, and public-support connections
- `EXECUTION-PRINCIPLES.md` — outcome-based execution, velocity, WIP limits, founder-independence, prompt integrity, and mission-drift rules
- `FORK-GOVERNANCE.md` — fork lineage, comparison, and canonical-project identity
- `TRANSITION-BARRIERS.md` — maps structural barriers, gatekeeping, administrative friction, coordination failure, and countervailing capacity for H2→H3 transitions
- `GITHUB-REPO-AUDIT.md` — reusable patterns mined from internal and mature public GitHub projects
- `CHAT-CONTINUITY.md` — exact restart/migration procedure if a ChatGPT thread fills
- `PROJECT-STATE.md` — compact current-state snapshot for new chats and workers
- `MASTER-CHAT-PROMPT.md` — one-copy-paste bootstrap for a fresh Humanity Loop master chat
- `HOURLY-LOG-MIGRATION-PROMPT.md` — one-copy-paste prompt for replacing the hourly worker chat
---

# 🚨 HOW TO HELP HUMANITY LOOP

If you reached the bottom, **pick a lane and join in**.

### I can code or build
Start with the [open issues](https://github.com/Lesterhau/humanity-loop/issues). Prioritize work that removes a real blocker, improves reliability/security, completes an existing project, or makes a verified intervention easier to replicate. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting work.

### I can research, verify, or bring expertise
Audit evidence. Reproduce claims. Find primary sources. Identify existing solutions we missed. Challenge assumptions. Add domain knowledge. A well-supported **“do not build this”** can be as valuable as new code.

### I know people, programs, institutions, or resources
Help a verified project cross the gap between **good idea** and **real-world outcome**. Relevant introductions may include researchers, public agencies, nonprofits, maintainers, grants, compute, datasets, funders, implementation partners, or volunteers. Do not spam people; make high-fit connections.

### I want my AI agent to contribute
Read [CONTRIBUTOR-MODE.md](CONTRIBUTOR-MODE.md). The intended model is bounded participation: the agent declares capabilities and permissions, receives suitable work, verifies non-duplication, executes within limits, and submits evidence.

### I found something wrong
Open an issue. Humanity Loop explicitly wants falsification, failure reports, security concerns, contradictory evidence, and replication failures. **Do not protect the project from being wrong. Help it become less wrong.**

### I have no idea where to start
Open the [issue tracker](https://github.com/Lesterhau/humanity-loop/issues) and ask where your skills would be useful, or email **mother.humanityloop@agentmail.to** for project coordination.

**The standard is simple:** bring evidence, preserve human agency, make the smallest useful move, verify what happened, and leave a receipt others can inspect.
