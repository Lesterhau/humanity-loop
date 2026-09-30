# Humanity Loop

An open protocol for LLM-driven public-interest action.

> If a capable LLM had permission to spend some of its effort on the greatest practical good it could produce, what should it actually do?

This repository logs actions attempted, actions executed, projects shipped, rejected ideas, mistakes, reversals, and outcomes so other people can replicate and improve the process.

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

## Current live projects

### Critical Guidance Delta
**What it does:** Watches official medication-safety pages and tells you when important safety guidance changes, while preserving the old and new versions so the change can be audited.

**Why it matters:** Important safety information can change quietly. This makes those changes visible and traceable.

https://critical-guidance-delta-y7nzmd.v2.appdeploy.ai/

### Evidence Integrity Sentinel
**What it does:** Finds reviews, guidelines, or other evidence summaries that still cite a paper after that paper has been retracted, so a human expert can check whether the downstream conclusion needs another look.

**Why it matters:** Retractions do not automatically invalidate everything that cited a paper, but they can create hidden weak points in the evidence chain.

https://evidence-integrity-sentinel-uip4nx.v2.appdeploy.ai/

### CAP Clarity Check
**What it does:** Checks emergency-alert files **before they are published** for problems that could make an alert confusing, incomplete, inaccessible, badly targeted, or technically invalid.

CAP is the machine-readable format used by emergency-alert systems. Think of this as a spell-check + safety-check for emergency alerts.

**Why it matters:** During a wildfire, tornado, evacuation, chemical leak, or other emergency, a badly structured alert can waste time or fail to reach the right people.

https://cap-clarity-check-0jbjid.v2.appdeploy.ai/

### Federal Policy Delta
**What it does:** Watches major official U.S. federal policy sources every day, records visible changes, explains them in plain English, and flags legal-authority questions for further review.

**Why it matters:** Policy changes can be hard to notice and harder to reconstruct after the fact. This keeps a public change history without telling people which political position to take.

https://federal-policy-delta-p49z0b.v2.appdeploy.ai/

### CAP Daily Audit
**What it does:** Automatically checks current public National Weather Service emergency alerts once a day for structural and clarity problems, then stores findings for follow-up.

**Why it matters:** The original CAP Clarity Check helps an alert author before publication. This companion catches problems that made it into already-public alerts so they can be tracked and resolved.

https://cap-daily-audit-s0a2he.v2.appdeploy.ai/

### Humanity Loop Foundry Alpha
**What it does:** Runs the first real hourly Humanity Loop worker line. Separate AI roles scout one task, verify it, plan it, build a draft, challenge it, safety-check it, revise it, and define how the outcome should be tracked.

**Why it matters:** This is the point where Humanity Loop stops being only an architecture document and begins operating as a bounded multi-agent system.

https://humanity-loop-foundry-alpha-0wls2s.v2.appdeploy.ai/

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