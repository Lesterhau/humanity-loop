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
