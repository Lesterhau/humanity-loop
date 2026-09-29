# Multi-Model Humanity Loop

Humanity Loop is vendor-neutral. No single model should become the sole researcher, builder, critic, or arbiter.

## Core pattern

One shared Humanity Loop control plane:
- public GitHub repository and action ledger;
- remote MCP/API;
- evidence/provenance;
- task queue;
- governance rules;
- results/replication records.

Multiple independent model families can connect to the same system and take different roles.

## Claude

Claude Pro supports remote MCP connectors in Claude/Claude Desktop. Claude Code is also available to Pro/Max subscribers.

Planned use:
- independent 10th-Man reviews;
- long-form synthesis;
- coding/architecture review;
- replication of ChatGPT-built artifacts;
- contributor workers through the Humanity Loop MCP.

Important: Claude Pro chat subscription and Anthropic API billing are separate. Do not assume Pro includes API credits.

## Perplexity

Perplexity Pro supports custom remote MCP connectors / Bring Your Own Connector.

Planned use:
- independent fresh-web research;
- source discovery;
- claim verification;
- competitive/duplication scans;
- weak-signal research;
- contributor mode through Humanity Loop MCP.

Perplexity's API platform is separately billed from consumer Pro access. The consumer subscription can still be useful through the Perplexity interface and remote connectors.

## Kimi

Kimi supports plugins containing MCP and Skills; Kimi Code/Work support richer plugin components including agents/hooks/commands. Kimi Code can connect to remote MCP servers.

Planned use:
- additional independent model family;
- agent/swarm experiments;
- coding/engineering reviews;
- multilingual/China/Asia source discovery;
- contributor workers connected to Humanity Loop MCP.

Kimi API access may be used later for centrally scheduled workers if economical, but consumer/plugin participation does not require Humanity Loop to be tied to one API vendor.

## DeepSeek

DeepSeek exposes an OpenAI-compatible/Responses API and official integrations with Codex and Claude Code. It is currently best treated as an optional worker-model backend rather than Humanity Loop's coordination layer.

Planned use:
- low-cost independent replication;
- engineering/code-agent workloads;
- adversarial model diversity;
- off-peak batch work where cost/energy governance permits.

A DeepSeek web/app account does not by itself create an API worker. Automated central use requires API credentials/balance or a supported client configured to use DeepSeek.

## Cross-model assignment strategy

Do not ask every model the same question by default.

Prefer role diversity:
- Model A: primary researcher/builder
- Model B: replication
- Model C: 10th-Man / strongest dissent
- Model D: evidence/provenance audit
- Model E: implementation/code review

For high-impact conclusions, disagreement between model families is information, not noise. Preserve the disagreement and investigate why it occurred.

## Anti-groupthink rule

For consequential projects, at least one independent review should use a different model family or evidence pipeline when practical.

Do not let one vendor's shared training biases silently propagate through every worker.

## Consumer-subscription strategy

Use paid consumer subscriptions where their own interfaces legally support MCP/connectors/agent work. Do not automate consumer UIs by credential scraping or bypass product controls.

For centrally orchestrated unattended workers, use supported APIs, CLIs, hosted agents, or scheduled systems with explicit authorization.

## Goal

Humanity Loop should become a coordination protocol that can survive changes in:
- model vendor;
- frontier-model rankings;
- pricing;
- APIs;
- plugin ecosystems;
- hosting providers.

Models are workers. Humanity Loop is the institution.


## Gemini

Gemini Pro / Google AI can participate as another independent model family. Google's Gemini API supports remote MCP servers, and Gemini CLI can use MCP-capable tooling.

Planned use:
- independent research/replication;
- long-context synthesis;
- multimodal evidence review;
- coding/engineering review;
- Google-ecosystem and multilingual scouting;
- contributor workers through the Humanity Loop remote MCP.

Consumer Gemini Pro access should not be treated as equivalent to API credits. Humanity Loop should use supported consumer interfaces for voluntary/manual contribution and APIs/hosted agents for centrally orchestrated unattended workers.


## Qwen

Alibaba's Qwen open-weight family is part of the Humanity Loop model pool. Current 2026 releases include Qwen3.8 models, including large multimodal/agentic open models.

Planned use:
- open-weight independent replication;
- coding/agentic workloads;
- long-context and multimodal work;
- multilingual and China/Asia source analysis;
- model-diversity checks against U.S. proprietary systems.

Open weights are useful because Humanity Loop can eventually run selected Qwen workers on infrastructure it controls rather than depending entirely on a vendor-hosted chat product.


## Qwen / Alibaba

Qwen is a major Chinese model family and should be treated as another independent Humanity Loop worker family.

Use cases:
- coding and engineering replication;
- multilingual research;
- independent reasoning;
- long-context agentic tasks;
- cost-efficient hosted workers where appropriate;
- open-weight experimentation when a suitable Qwen checkpoint is available.

Track hosted and open-weight releases separately rather than assuming the newest hosted model is also open-weight.

## Z.ai / GLM

GLM is another independent Chinese model family suitable for model diversity, coding, long-horizon agentic work, and open-weight experimentation where licensing permits.

Use cases:
- engineering and coding review;
- long-horizon task replication;
- alternative reasoning pipelines;
- open-weight worker experiments;
- diversity against correlated model-family errors.

Benchmark task performance, cost, reliability, and environmental efficiency rather than assigning status based on nationality or vendor reputation.
