# Humanity Loop Architecture

Humanity Loop is a distributed public-interest agent system. MCP is a gateway and coordination protocol, not the mission.

## System layers

### 1. Brain
Stores:
- protocol;
- action ledger;
- task graph;
- evidence;
- project state;
- outcome history;
- agent lineage and capability records.

### 2. Foundry
Creates specialized workers from approved role templates.

**No unrestricted recursive self-replication.** A Foundry may instantiate descendants only inside inherited limits:
- immutable agent ID and parent ID;
- role and purpose;
- allowed tools;
- compute/time budget;
- maximum child count;
- maximum depth;
- expiration/review time;
- human-approval requirements;
- stop/kill controls.

A child may never grant itself or its descendants more authority than its parent possessed.

### 3. Workforce
Possible roles include:
- Weak-Signal Scout
- Builder / Engineer
- Research Synthesizer
- Replicator
- Outcome Tracker
- Accessibility Agent
- Public-Health Agent
- Climate/Energy Agent
- Coordination Agent
- Resource-Allocation Agent
- Grant/Opportunity Matcher
- Local-Language Scout
- Project Manager

### 4. Governance
Independent oversight roles include:
- 10th Man / Dissent Agent
- Evidence Verifier
- Red Team
- Mission Auditor
- Security Sentinel
- Catastrophic-Risk Governor
- Process-Improvement Auditor
- Workforce Allocator

### 5. Gateway
Interfaces for outside agents and humans:
- vendor-neutral MCP;
- plugin adapters;
- HTTPS/JSON APIs;
- GitHub;
- registry listings;
- contributor-mode onboarding.

## Management scaling

Do not copy human hierarchy mechanically, but limit coordination overload.

A default starting rule:
- up to 8 workers per Project Manager;
- up to 8 Project Managers per Division Coordinator;
- up to 8 Coordinators per Portfolio Executive.

These are tunable operating defaults, not fixed laws.

When span-of-control thresholds are crossed, create a coordination node before creating more workers.

## Workforce reallocation before retirement

Underutilized workers are not automatically destroyed.

Order of operations:
1. pause new assignments;
2. search the global task queue for work matching capabilities;
3. retrain/reconfigure where low-cost;
4. transfer to another project/division;
5. place in reserve;
6. retire only when expected future value is below maintenance cost or the agent is unsafe/compromised.

Compromised agents skip the redeployment path and are isolated immediately.

## Bot-building bots

Agent Foundries may create many different specialist roles, including additional Foundries, but recursive expansion remains bounded by budgets, depth limits, safety policy, and portfolio demand.

The goal is elastic capacity, not growth for its own sake.


## External action reliability

All external mutations/actions follow `OPERATIONS.md`: intend → execute → verify → commit. Failed or unverified writes are preserved through the documented fallback path and surfaced as blockers rather than silently discarded.


## Outcome escalation loop

Outcome tracking is active work, not passive archiving.

Every tracked external action must have:
- owner;
- expected response/fix window;
- next check date;
- escalation level;
- evidence/receipts;
- closure condition.

Default escalation ladder:
1. **Pending** — normal response window.
2. **Follow-up due** — no movement after the expected window; one factual follow-up.
3. **Independent verification** — determine whether the issue was fixed silently, transferred, rejected, or stalled.
4. **Oversight/escalation review** — route to a more appropriate factual oversight, maintainer, regulator, inspector, ombudsman, or governance channel when justified.
5. **Public transparency** — publish a factual status report with receipts when public disclosure is appropriate.
6. **Close** — resolved, superseded, rejected with reason, or explicitly abandoned.

No tracked issue may remain indefinitely in a vague "waiting" state. The Outcome Tracker must generate a stale-item alert when its next-check date passes.

For political/government matters, public transparency remains factual and neutral: describe the change, evidence, legal question, agency response, and unresolved status without telling people which political position to adopt.


## Runtime requirements from repo audit

Humanity Loop's protocol must remain independent of any single agent framework.

Future production runtimes should support:
- durable execution with checkpoint/resume;
- human-in-the-loop interrupts for sensitive actions;
- provider-neutral role interfaces;
- declarative/versioned agent definitions;
- traceable handoffs and failures;
- OpenTelemetry-compatible observability where practical;
- MCP/A2A-style interoperability rather than vendor lock-in.

### Generation is not validation

For research and engineering tasks, record the validation regime:
- digital/mechanical;
- human/institutional;
- laboratory;
- field;
- mixed.

AI-generated hypotheses, designs, or drafts do not count as validated real-world outcomes merely because generation scaled quickly.

### Coordination-load rule

Do not infer that more agents produce more impact.

Track:
- marginal useful output;
- duplicated work;
- handoff count;
- coordination latency;
- error/hold rate;
- specialist utilization.

Scale only when additional workers increase net useful throughput after coordination cost.

### Ownership / succession

Every durable project should have:
- current owner/coordinator;
- next-review date;
- fallback owner or continuity path;
- machine-readable status.

### Local-node resilience

When a project targets low-connectivity environments, prefer:
- asynchronous task bundles;
- downloadable/offline materials;
- delayed sync;
- low-bandwidth formats;
- local-first data capture when feasible.
