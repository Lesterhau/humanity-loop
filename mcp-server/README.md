# Humanity Loop Remote MCP

Read-only vendor-neutral gateway for the public Humanity Loop repository.

## Endpoints

- Streamable HTTP MCP: `/api/mcp`
- Plain JSON fallback: `/api/v1?tool=<tool>`

## MCP tools

- `get_protocol`
- `list_actions`
- `get_action`
- `list_live_projects`
- `get_project`
- `get_replication_prompt`
- `search_dead_ends`

The server reads only public canonical files from `Lesterhau/humanity-loop`. No public write tools are exposed in v1.

## Local validation

```bash
npm install
npm run typecheck
npm run build
npm run dev
```

Then connect an MCP client to `http://localhost:3000/api/mcp`.

Before official registry publication, test the deployed endpoint with at least two independent MCP clients and record the results in the parent repository.
