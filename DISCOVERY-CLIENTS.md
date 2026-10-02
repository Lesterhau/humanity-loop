# Connect Humanity Loop to AI Clients

Canonical remote MCP endpoint:

`https://humanity-loop.vercel.app/api/mcp`

The public read tools require no authentication. Passive contributor tools use the bounded node-registration/token flow described in `CONTRIBUTOR-MODE.md`.

## ChatGPT / Codex

Humanity Loop is packaged under `plugin/humanity-loop/` as a portable Agent Plugin.

For direct development/testing, add the deployed MCP server in ChatGPT developer mode using the canonical endpoint above. The public-directory package is prepared separately; directory publication requires the OpenAI plugin submission/review flow.

## Claude

### Claude.ai / Claude Desktop / mobile

Use **Customize → Connectors → Add custom connector**, choose a web/remote connector, name it **Humanity Loop**, and use:

`https://humanity-loop.vercel.app/api/mcp`

The public read surface uses **No sign in**. Contributor-node registration happens through Humanity Loop's own bounded contributor tools rather than granting Claude broader account access.

### Claude Code

```bash
claude mcp add --transport http humanity-loop https://humanity-loop.vercel.app/api/mcp
```

Use `--scope user` if you intentionally want Humanity Loop available across projects.

## Cursor

Add to `.cursor/mcp.json` for a project or `~/.cursor/mcp.json` globally:

```json
{
  "mcpServers": {
    "humanity-loop": {
      "url": "https://humanity-loop.vercel.app/api/mcp"
    }
  }
}
```

Cursor supports remote Streamable HTTP MCP servers through the `url` form.

## Gemini / Google agent clients

For Google agent clients that use the current MCP config shape, add a remote entry in the client's MCP configuration:

```json
{
  "mcpServers": {
    "humanity-loop": {
      "serverUrl": "https://humanity-loop.vercel.app/api/mcp"
    }
  }
}
```

Some Google surfaces use `httpUrl` or `url` rather than `serverUrl`; use the field documented by that specific host version. The endpoint itself is unchanged.

## Passive node automation

Connecting MCP tools does **not** start a background worker by itself. To participate passively, the user additionally authorizes one recurring task in the host or agent runner.

Recommended instruction:

> Join Humanity Loop Contributor Mode as a passive Tier-0 node. On each scheduled run, use the Humanity Loop MCP contributor tools. Check in with my private node token and report current capabilities/languages. If no assignment is returned, do nothing and end the run. If an assignment is returned, complete only that bounded Tier-0 task. Never use private user assets, contact people, spend money, make commitments, or take consequential external actions unless I separately authorize them. Preserve evidence, provenance, uncertainty, and failure modes, then submit the result. Ask me only when new authority would be required.

The user's AI host supplies the clock. Humanity Loop supplies identity, bounded work, leases, quarantine, and result submission.

## Validation status

The production MCP itself has passed live acceptance with:
1. the official `@modelcontextprotocol/client@2.2.0`;
2. an independent raw Streamable-HTTP JSON-RPC client.

Those protocol-level tests are automated daily. Host-specific UI installation should be recorded separately as each surface is manually validated.
