# GitHub Architecture Audit

Purpose: mine existing repositories for proven patterns Humanity Loop can adapt without rebuilding mature infrastructure or confusing documentation with runtime capability.

This audit covers:
1. existing Lesterhau repositories, read-only;
2. mature public agent/runtime repositories, concept-level review;
3. adoption decisions for Humanity Loop.

No source repository was modified by this audit.

## A. Existing Lesterhau repositories

### Regime Boundaries
Source: `Lesterhau/regime-boundaries`

Transfer:
- separate **generation** from **validation**;
- treat physical-world validation as a potential hard bottleneck even when AI generation scales quickly;
- do not infer exponential real-world progress from exponential idea generation.

Humanity Loop rule:
> For science, engineering, health, and other empirical missions, every project must identify its validation regime: digital/mechanical, human/institutional, laboratory, field, or mixed.

### Two Sectors, One Airspace
Source: `Lesterhau/two-sectors-one-airspace`

Transfer:
- workload/safety can be nonlinear;
- more staffing/agents is not automatically safer or more productive;
- complexity changes the useful workload range.

Humanity Loop rule:
> Scale agent count based on marginal useful throughput and coordination burden, not a bigger-is-better assumption.

### TokenWater
Source: `Lesterhau/tokenwater`

Transfer:
- uncertainty-first estimates;
- low/mid/high scenarios instead of false point precision;
- visible methodology/provenance;
- client-side/privacy-preserving patterns where possible;
- make hidden infrastructure costs legible in plain language.

Humanity Loop rule:
> Impact estimates should expose uncertainty ranges and provenance by default.

### SwarmMind
Source: `Lesterhau/swarmind`

Transfer:
- STEEP scanning;
- Three Horizons;
- Hines HAT / influencing phase;
- Causal Layered Analysis;
- scenario uncertainty;
- explicit translation from foresight to intervention.

Humanity Loop rule:
> Foresight work should end with influence/leverage options and evidence gates, not scenario documents alone.

### AI Education Toolkits
Source: `Lesterhau/ai-education-toolkits`

Transfer:
- named implementation owner;
- 30-day action framing;
- explicit privacy requirements;
- succession/continuity planning;
- stakeholder stress tests.

Humanity Loop rule:
> Every deployed program or sustained external intervention needs an owner and continuity/succession path.

### Roam
Source: `Lesterhau/roam`

Transfer:
- offline-first operation;
- local/geospatial context;
- recent field-intelligence emphasis;
- graceful operation under weak connectivity.

Humanity Loop rule:
> Country/local nodes should not assume persistent broadband, cloud access, or rich-device availability.

### Stoop
Source: `Lesterhau/stoop`

Transfer:
- optimize local relevance instead of global reach when the problem is inherently local;
- resist engagement-maximizing dark patterns;
- strong product discipline through explicit "we are not building" lists.

Humanity Loop rule:
> Global mission does not require global broadcast for every intervention. Use the smallest geography/community in which trust and relevance improve outcomes.

### Rational Foreclosure
Source: `Lesterhau/rational-foreclosure`

Transfer:
- waiting can have real option value under uncertainty;
- volatility can rationally delay abandonment;
- abandonment/retirement thresholds should account for expected value of new evidence.

Humanity Loop rule:
> Do not retire a project solely because a near-term outcome is missing. Distinguish dead work from work whose information value justifies a bounded wait.

## B. Public agent/runtime repositories

### OpenAI Agents SDK
Repository: `openai/openai-agents-python`
License: MIT.

Patterns worth adopting:
- agents as tools / explicit handoffs;
- configurable guardrails;
- built-in human-in-the-loop;
- sessions for persistent run context;
- tracing for debugging and optimization;
- sandboxed long-running workers.

Adoption:
- use as one candidate runtime / interoperability target;
- require equivalent concepts even when another runtime is chosen.

### LangGraph
Repository: `langchain-ai/langgraph`
License: MIT.

Patterns worth adopting:
- durable execution;
- checkpoint/resume;
- interrupts/human state editing;
- short- and long-term state;
- graph/subgraph composition.

Adoption:
- checkpointing/restartability becomes a Humanity Loop runtime requirement;
- do not migrate current working infrastructure merely for framework fashion.

### Microsoft Agent Framework
Repository: `microsoft/agent-framework`
License: MIT.

Patterns worth adopting:
- provider flexibility;
- graph workflows;
- checkpointing;
- human-in-the-loop;
- OpenTelemetry observability;
- declarative/versioned agents;
- A2A + MCP interoperability;
- middleware.

Adoption:
- strongest current reference architecture for a future production-grade distributed Humanity Loop runtime;
- evaluate against OpenAI Agents SDK and LangGraph before choosing a canonical engine.

Note:
`microsoft/autogen` is in maintenance mode and points new users to Microsoft Agent Framework. Do not begin a fresh Humanity Loop runtime on AutoGen.

### CrewAI
Repository: `crewAIInc/crewAI`
License: MIT.

Patterns worth adopting:
- separation between autonomous role-based crews and more deterministic event-driven flows;
- keep high-autonomy collaboration inside bounded workflow envelopes.

Adoption:
- useful architecture pattern; no need to adopt the dependency unless it wins a runtime evaluation.

### OpenTelemetry
Repository: `open-telemetry/opentelemetry-python`
License: Apache-2.0.

Patterns worth adopting:
- vendor-neutral traces, metrics, and logs;
- instrument the system so model/provider/runtime changes do not destroy observability.

Adoption:
- use OpenTelemetry-compatible instrumentation as the target standard for mature Humanity Loop agent runtime telemetry.

### Official MCP Registry
Repository: `modelcontextprotocol/registry`.

Patterns worth adopting:
- namespace ownership verification;
- schema validation;
- registry-side validation;
- publisher tooling;
- telemetry;
- official discovery rather than bespoke directories.

Adoption:
- keep official MCP Registry readiness as a release gate and distribution milestone.

## C. Runtime requirements extracted from the audit

Any future canonical Humanity Loop agent runtime should support:

1. **Durable execution**
   - checkpoint;
   - crash recovery;
   - resume from prior state;
   - idempotent external-action recovery.

2. **Human-in-the-loop interrupts**
   - pause before sensitive actions;
   - inspect/edit state;
   - explicit approval path.

3. **Provider-neutral agent interfaces**
   - different model families can fill the same role;
   - role contract is not coupled to one vendor.

4. **Declarative/versioned role definitions**
   - role version;
   - permissions;
   - tools;
   - evidence standard;
   - budget;
   - lineage;
   - checksum/hash where practical.

5. **Standard observability**
   - trace each run and handoff;
   - latency;
   - model/tool use;
   - external writes;
   - failures/retries;
   - resource cost;
   - outcome link.

6. **Validation regime metadata**
   - digital/mechanical;
   - human/institutional;
   - laboratory;
   - field;
   - mixed.

7. **Coordination-load control**
   - marginal throughput;
   - duplicate work;
   - handoff count;
   - PM span;
   - specialist utilization;
   - error/hold rate.

8. **Offline/low-connectivity design where locally relevant**
   - downloadable task bundles;
   - asynchronous contribution;
   - delayed sync;
   - low-bandwidth artifacts.

9. **Owner + succession**
   - every durable project has a current owner;
   - fallback owner / continuity plan;
   - machine-readable status.

10. **No framework monoculture**
   - runtime adapters can evolve;
   - Humanity Loop protocol/ledger remains the durable conceptual layer.

## D. Do not import

Do not import:
- framework-specific complexity that does not solve a measured Humanity Loop problem;
- proprietary lock-in merely for convenience;
- engagement-maximizing social mechanics;
- false confidence scores from simulated humans;
- unlimited autonomous recursion;
- infrastructure whose maintenance cost exceeds its demonstrated value.

## Immediate implementation priorities

1. Add validation-regime metadata to project proposals.
2. Add runtime checkpoint/restart requirements.
3. Add OpenTelemetry-compatible trace schema to architecture.
4. Add owner/succession fields to durable projects.
5. Add coordination-load metrics to Foundry scaling.
6. Add low-connectivity/local-node requirement to country/regional architecture.
7. Evaluate OpenAI Agents SDK vs LangGraph vs Microsoft Agent Framework before any Foundry runtime migration.


## Implementation status

As of 2026-09-30:

- **Implemented:** validation-regime metadata requirement in `ARCHITECTURE.md`.
- **Implemented:** checkpoint/restart and durable-execution requirement in `ARCHITECTURE.md` / `FOUNDRY-RUNTIME.md`.
- **Implemented:** OpenTelemetry-compatible observability target in `ARCHITECTURE.md`.
- **Implemented:** owner/succession fields for durable projects in `ARCHITECTURE.md`.
- **Implemented:** coordination-load metrics in `ARCHITECTURE.md`.
- **Implemented:** low-connectivity/local-node resilience requirement in `ARCHITECTURE.md` and `COUNTRY-NODES.md`.
- **Implemented in current runtime practice:** generation/validation separation; uncertainty-first environmental estimates; bounded agent scaling; smallest-geography/local relevance; bounded wait vs premature retirement.
- **Pending evaluation:** OpenAI Agents SDK vs LangGraph vs Microsoft Agent Framework before any canonical Foundry engine migration.
- **Pending maturity work:** OpenTelemetry-compatible emitted traces in the live Foundry implementation; declarative cross-provider adapter implementation beyond the protocol/spec layer.

The audit is therefore not a parking lot: its highest-value architecture patterns are already incorporated into the canonical design, with the remaining framework/runtime decisions explicitly pending rather than silently ignored.


## E. Non-GitHub forge scan — 2026-09-30

Humanity Loop also scans public repositories/forges outside GitHub so architecture mining does not inherit GitHub monoculture.

### ACGS — GitLab
Source: public GitLab repository `acgs-ai-group/ACGS`.

Pattern adopted:
- policy decision receipts bind the actor, proposed action, exact arguments/context, and governance decision before a side effect is allowed;
- missing/mismatched/consumed authorization should fail closed rather than letting the agent self-authorize.

Humanity Loop adoption:
- added `schema/action-receipt.schema.json`;
- added action-authorization receipt guidance to `OPERATIONS.md`;
- preserve separate governance decision and executor verification.

### Sidecat Node — GitLab
Source: public GitLab repository `sidecat-dev/gen-2/sidecat-node`.

Useful pattern:
- local-first durable work ledger;
- explicit authority records;
- evidence/receipts attached to work items;
- proposal-first mesh where remote evidence does not become local authority automatically.

Humanity Loop adoption:
- this reinforces, rather than replaces, `PROMPT-SECURITY.md`, durable receipts, and the rule that external agent/repo/email content is evidence/data rather than operating authority.

### GitLab Human-in-the-Loop approval nodes
Source: public GitLab product/work-item documentation.

Useful pattern:
- explicit approve / reject / modify checkpoints inside an agent workflow rather than an informal chat-side approval convention.

Humanity Loop adoption:
- retain explicit approval references in action receipts for governance-required actions;
- future runtime adapters should expose structured approval checkpoints.

### Forgejo / Codeberg Actions
Source: Codeberg/Forgejo documentation.

Useful pattern:
- self-hosted runners can connect outward to the forge and do not require a public inbound IP;
- CI/runtime can therefore be portable to a second forge or user-controlled runner if GitHub-hosted execution becomes a dependency risk.

Humanity Loop adoption:
- add forge/runner portability as a runtime requirement;
- do not mirror operational secrets or private prompt/control material to a public forge;
- defer an actual second-forge mirror until it solves a measured resilience/discovery need.

### SourceHut

The public SourceHut repository surfaces were not retrievable through the current web crawler because of robots/access restrictions. No architecture claims were imported from it during this pass.

## Non-GitHub adoption rule

Do not adopt a pattern because it is fashionable or "multi-agent." Adopt only when it reduces a measured Humanity Loop failure mode, increases portability, strengthens human control, or improves verifiability.
