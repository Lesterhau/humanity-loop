# Humanity Loop Core Independence Roadmap

**Purpose:** remove any single hosting/model/provider dependency from the system's critical path.

## Target architecture

Humanity Loop should survive the loss of AppDeploy, one model provider, one scheduler, or one chat without losing canonical state or silently stopping.

### 1. Canonical state
- GitHub remains the public institutional record: protocol, code, governance, issues, ledgers, receipts, release history.
- A transactional control-plane datastore holds ephemeral operational state: agents, tasks, leases, heartbeats, attempts, approvals, dead letters, usage and run events.
- GitHub records durable summarized receipts; the control plane handles concurrency.

**Default long-term control-plane backend: Supabase/Postgres.** Use standard Postgres schema and SQL so the control plane remains portable; avoid Supabase-only business logic where practical.

### 2. Scheduling
- Deterministic/public-data jobs: GitHub Actions.
- Model-dependent Foundry cycles: replaceable executor(s) triggered from an independent schedule.
- ChatGPT automation remains a continuity path, not the only scheduler.
- AppDeploy cron is optional; credit exhaustion must not stop the system.

### 3. Execution/provider adapters
All model calls sit behind a provider interface.

A task declares:
- role;
- required capabilities;
- allowed tools;
- budget;
- deadline;
- evidence requirements;
- approval tier.

The control plane assigns it to an available provider adapter. No provider gets more authority because it is available.

Potential adapters include OpenAI/ChatGPT, Anthropic, Gemini, open-weight/local models, and future providers. Provider selection is a routing concern, not a governance concern.

### 4. Public gateway
The remote MCP server is the vendor-neutral read-only public gateway.

Near-term acceptance:
1. build/typecheck/security audit green;
2. deploy on stable HTTPS;
3. validate with at least two independent MCP clients;
4. publish discovery metadata only after validation.

**Default public MCP/web host: Vercel.** The current MCP server is Next.js-native, making Vercel the lowest-friction primary host with a straightforward scale-up path. Hosting must remain replaceable; AppDeploy is not required, and the service must be portable to another Node-compatible host.

### 5. Permissions and side effects
Use capability-based permissions.

Every external-action worker receives only the minimum scopes needed for the assigned action. Sensitive actions require explicit approval or qualified oversight.

Required lifecycle:
intend → authorize → execute → verify → receipt → outcome follow-up.

### 6. Observability / reliability
Minimum production-readiness surface:
- latest health per scheduler/worker;
- queue depth and stale leases;
- failed/dead-letter tasks;
- durable-write failures;
- provider availability;
- usage/cost/environmental telemetry;
- latest governance/security test state;
- alert when canonical state disagrees with live state.

A historical red CI run superseded by a current verified green run is incident history, not an active outage.

### 7. Security
- secrets never stored in repository/chat;
- scoped provider/tool credentials;
- dependency lockfiles and vulnerability gates;
- prompt/instruction trust boundaries;
- signed or otherwise tamper-evident action receipts where practical;
- RLS/least privilege on operational state;
- explicit PII/data-retention classes;
- public write authority remains permissioned.

### 8. Governance
Power must grow with accountability.

Increasing autonomy requires:
- stronger verification;
- smaller permission scopes;
- reversible first actions;
- independent dissent/safety review;
- explicit stop conditions;
- external/human oversight for consequential domains;
- outcome evidence before scale.

Humanity Loop should maximize **effective public-interest agency**, not unconstrained machine authority.

## AppDeploy role going forward

AppDeploy may continue to host useful UIs and prototypes.

It is **not** allowed to be:
- sole scheduler;
- sole datastore;
- sole model runtime;
- sole gateway;
- sole receipt store;
- a blocker to core operation because credits are exhausted.

If AppDeploy credits disappear, the public surfaces may degrade, but sensing, scheduling, governance, persistence, MCP, and outcome tracking must continue elsewhere.

## Near-term sequence

### Phase A — stabilize
- [x] current core CI green
- [x] governance regression suite green
- [x] Foundry control-plane regression suite green
- [x] MCP build/security gate green
- [x] recover missing durable Foundry receipt
- [x] reconcile active scheduler truth

### Phase B — remove hosting dependency
- [ ] deploy MCP to replaceable public HTTPS host
- [ ] validate MCP with two independent clients
- [ ] add health endpoint + uptime check
- [ ] document host failover/redeploy procedure

### Phase C — transactional control plane
- [ ] create portable Postgres schema for agents/tasks/leases/events/dead-letter/approvals/usage
- [ ] implement lease claiming and heartbeat expiration transactionally
- [ ] persist Foundry cycles through the control plane
- [ ] reconcile completed runs into GitHub receipts
- [ ] add RLS/least privilege and security advisor checks

### Phase D — provider independence
- [ ] define provider adapter interface
- [ ] connect at least two model execution paths
- [ ] add health/cost/capability routing
- [ ] prove failover without changing governance semantics

### Phase E — public readiness
- [ ] dependency/security scan green
- [ ] failure injection: disable one scheduler/provider and prove continuity
- [ ] permission-boundary tests
- [ ] privacy/data-retention review
- [ ] disaster-recovery test
- [ ] external contributor sandbox
- [ ] publish MCP/discovery channels only after the above passes

## Definition of world-changing capability

The objective is not to give one model unrestricted control.

The objective is a repeatable loop:

**sense → verify → prioritize → design → dissent → safeguard → act → verify → measure → connect → scale → learn**

The system becomes powerful when it can repeat that loop across many domains, with credible evidence, resources, collaborators, durable memory, and bounded authority.


## Knowledge cockpit

Obsidian may be used as an optional **human-facing knowledge cockpit** for browsing linked Markdown, visualizing relationships, and offline reading.

It is not canonical infrastructure:
- GitHub remains the public/versioned institutional record.
- Supabase/Postgres owns transactional runtime state.
- Undermind remains the research workspace for literature-heavy work.
- Obsidian must not become a scheduler, control plane, approval system, or sole copy of project knowledge.

If adopted, prefer a read-only or carefully synchronized view of selected Humanity Loop Markdown rather than creating another independent source of truth.
