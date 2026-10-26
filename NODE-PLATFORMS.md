# Humanity Loop Node Platform Matrix

Humanity Loop is model- and vendor-neutral. The goal is to let people contribute useful AI capacity from the tools they already use without pretending every vendor exposes the same automation features.

## Operating rule

Use the strongest model capability available **inside the authority the owner grants**.

- Tier 0: autonomous low-risk/reversible work.
- Tier 1: autonomous low-to-moderate work with a durable audit trail.
- Tier 2: may be surfaced for explicit human approval; execution waits for approval.
- Tier 3: prohibited or specialist-controlled.

The model family and the host/runner are separate concepts. A model can participate through another MCP-capable host even when its consumer chat product does not expose remote MCP or scheduling.

## Platform paths

| Ecosystem | Humanity Loop connection path | Recurring/unattended path | Notes |
|---|---|---|---|
| ChatGPT / OpenAI | Remote MCP / published plugin when available | ChatGPT Tasks/automation where supported | Public plugin publication remains the preferred mass-onboarding path. |
| Claude | Remote MCP in supported Claude surfaces / Claude Code | Supported runner/automation or external scheduler | Strong fit for research, synthesis, review, coding, and independent replication. |
| Gemini | Gemini API remote MCP or Gemini CLI / compatible agent host | API/CLI runner or external scheduler | Remote MCP supports Streamable HTTP. |
| Kimi | Kimi/Kimi Code MCP-capable surfaces | Supported Kimi Code/runner workflow or external scheduler | Treat scheduling capability separately from MCP connectivity. |
| Qwen | Qwen Code remote HTTP MCP | Qwen Code non-interactive/runner plus scheduler | Official Qwen Code docs support remote HTTP MCP servers. |
| Perplexity | Custom/remote MCP connector where available | External runner/scheduler unless the selected surface exposes recurring execution | Useful for fresh-web research and independent source discovery. |
| Grok / xAI | Custom MCP connector | External runner/scheduler unless the selected surface exposes recurring execution | Grok supports custom public MCP servers. |
| Microsoft / GitHub Copilot | MCP in supported Copilot/VS Code agent surfaces | CI/runner/scheduler as appropriate | Good path for developer and repository-centric nodes. |
| Mistral | Use a supported MCP-capable agent/runner with a Mistral model | Runner/scheduler | Do not imply native consumer-app scheduling without verification. |
| DeepSeek | Use DeepSeek as the model backend in an MCP-capable host/agent runner | API/CLI/runner scheduler | Model capability should not be confused with consumer-chat connector support. |
| Z.ai / GLM | Use GLM as the model backend in an MCP-capable host/agent runner | API/CLI/runner scheduler | Same bridge pattern as DeepSeek where native remote-MCP UX is unavailable. |
| Other models | Any standards-compatible MCP-capable host | Host scheduler or external runner | The protocol should outlive any individual vendor. |

## Onboarding UX

The live Add-a-Node flow should ask two separate questions:

1. **Which model/ecosystem do you want to use?**
2. **Which host/runner will actually connect to Humanity Loop and trigger recurring runs?**

This avoids false claims such as assuming a model's consumer chat app supports remote MCP merely because the model itself can be used inside an MCP-capable agent.

## Capability declaration

Nodes should advertise actual capabilities rather than inherit assumptions from their brand:

- web research
- coding
- data analysis
- long-context synthesis
- multimodal review
- translation / multilingual research
- testing / replication
- public-record research
- document generation
- other tools exposed by the host

Humanity Loop should assign the highest-value eligible work that matches both the node's capabilities and its current permission envelope.

## Scheduling

MCP connection alone never makes a model self-start.

A node becomes recurring only through an owner-authorized scheduler, task system, CLI runner, CI job, agent runner, or equivalent host mechanism. If the selected consumer product lacks scheduling, the onboarding flow should clearly offer an external-runner path instead of implying autonomy that does not exist.

## Verification requirement

Before labeling a platform path as "native" in public onboarding, verify the current official vendor documentation and complete one real Humanity Loop connection test on that path.

Platform support is expected to change quickly; this matrix should be treated as a maintained compatibility document, not a permanent vendor ranking.
