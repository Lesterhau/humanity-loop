# Discovery and Distribution Strategy

Humanity Loop should be discoverable by both humans and agents without manufacturing engagement.

## Do not do

- fake GitHub stars, reviews, forks, comments, or accounts
- coordinated inauthentic engagement
- spam maintainers or influencers
- claim adoption or impact that did not happen

## Agent-native distribution

1. Publish a remote MCP server at a stable HTTPS endpoint.
2. Register the server in the official MCP Registry.
3. Package the same remote MCP in a portable Agent Plugin.
4. Submit the plugin to the OpenAI universal Plugins Directory for ChatGPT and Codex.
5. Document one-line connection instructions for Claude, Gemini CLI/API, Cursor, and other MCP-capable clients.
6. Expose a plain HTTPS/JSON API in parallel for clients that do not support MCP.
7. Keep the protocol, schema, tool descriptions, and examples public in GitHub so search engines and coding agents can index them.

## Human distribution

- Publish tagged GitHub releases.
- Use precise repository topics and an explicit description.
- Submit to relevant MCP/community registries only after the server is stable.
- Create issues labeled `good first agent task` and `replication wanted` so humans and agents have obvious entry points.
- Seek legitimate maintainers, researchers, public-interest technologists, MCP builders, and agent-framework authors who have a reason to evaluate the project.

## Growth metric

Optimize for verified independent replication, useful contributions, downstream installs, and documented outcomes rather than stars alone.


## Current publication status

As of 2026-10-02:

- Production remote MCP: `https://humanity-loop.vercel.app/api/mcp`
- Official MCP Registry metadata: `server.json`
- Official MCP Registry publication: **successful** via GitHub OIDC workflow
- Registry publisher workflow: `.github/workflows/publish-mcp-registry.yml`
- Tagged GitHub release: **v0.2.0**
- Cross-client connection guide: `DISCOVERY-CLIENTS.md`
- Portable Agent Plugin package: `plugin/humanity-loop/`
- OpenAI review metadata includes required positive/negative test cases plus support/privacy/terms URLs.

Remaining public-directory work:
1. manually validate the host-specific install path in ChatGPT/Claude/Cursor/Gemini surfaces and record results;
2. finish OpenAI submission-only assets/materials, including primary icon and reviewer-accessible demo recording;
3. complete OpenAI publisher/domain verification and submit through the Plugins portal;
4. evaluate secondary community directories only after official channels are stable.

Do not treat OpenAI portal submission as automatable project code: publisher identity, domain challenge, review attestations, and final publication are accountable human actions.
