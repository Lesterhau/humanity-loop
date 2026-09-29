# Openness & Security Model

Humanity Loop should be open enough to earn trust and replicate, but not so turnkey that the public repo becomes a ready-made kit for unsafe autonomous action.

## Default-open layer

Keep these public:
- mission and protocol;
- governance;
- role definitions;
- research methods;
- action ledger and failures;
- project cards;
- read-only/public APIs and MCP tools;
- evidence/provenance formats;
- replication methods;
- safety tests;
- non-sensitive code that does not materially increase abuse capability.

### Benefits

- auditability;
- credibility;
- outside correction;
- faster replication;
- contributor recruitment;
- institutional resilience;
- less dependence on one founder/vendor;
- easier scientific/public-interest reuse.

### Costs

- hostile forks can copy the architecture;
- adversaries learn how the system reasons;
- public bugs may reveal weaknesses;
- competitors can free-ride;
- bad actors can remove our guardrails from copied code.

## Controlled/source-available layer

Keep access-controlled or staged when appropriate:
- credentials/secrets;
- write-capable third-party connectors;
- mass-outreach systems;
- recursive Foundry controls;
- high-impact automation switches;
- abuse-sensitive operational playbooks;
- security exploit chains;
- private recipient/contact data;
- unreleased safety vulnerabilities;
- infrastructure that can materially amplify harmful scale.

### Benefits

- reduces turnkey abuse;
- limits credential/permission leakage;
- allows staged testing;
- creates a safety gate before high-impact capabilities spread.

### Costs

- less external auditability;
- more central trust placed in maintainers;
- slower independent replication;
- creates governance/bus-factor risk;
- can look hypocritical if "open" branding overpromises.

## Recommended architecture

Use **open core + controlled capability adapters**.

The public can inspect:
- what Humanity Loop believes;
- how it chooses work;
- what agents are supposed to do;
- what happened;
- how results are verified.

High-impact execution modules require separate authorization and are not bundled into a frictionless one-click fork.

## Canonical identity

Open source cannot prevent hostile forks.

Instead, distinguish canonical Humanity Loop through:
- official domain;
- signed releases/checksums;
- official MCP registry listing;
- canonical GitHub organization/repository;
- public safety/version manifests;
- trademark/brand policy when mature;
- transparent provenance from MOTHER and project accounts.

A fork may copy code. It should not be able to plausibly impersonate the canonical network.

## Safety disclosure

Do not hide safety limitations merely because they might help attackers.

Prefer responsible disclosure:
- publish known limitations when doing so is safe;
- temporarily withhold exploit details that would materially enable abuse;
- disclose fixes and lessons after mitigation.

## Review trigger

Reassess what is public whenever:
- agent authority expands;
- recursive/delegation depth increases;
- new write-capable connectors are added;
- the system can influence large populations;
- a capability moves from analysis into real-world execution.
