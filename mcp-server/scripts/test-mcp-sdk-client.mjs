import assert from "node:assert/strict";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

const endpoint = process.env.MCP_URL || "http://127.0.0.1:3000/api/mcp";

const client = new Client(
  { name: "humanity-loop-ci-sdk-client", version: "1.0.0" },
  { versionNegotiation: { mode: "auto" } },
);
const transport = new StreamableHTTPClientTransport(new URL(endpoint));

try {
  await client.connect(transport);
  const { tools } = await client.listTools();
  const names = new Set(tools.map((tool) => tool.name));

  for (const required of [
    "get_protocol",
    "list_actions",
    "get_action",
    "list_live_projects",
    "get_project",
    "get_replication_prompt",
    "search_dead_ends",
    "contributor_register",
    "contributor_checkin",
    "contributor_submit",
    "contributor_set_status",
  ]) {
    assert(names.has(required), `missing MCP tool: ${required}`);
  }

  const result = await client.callTool({ name: "get_protocol", arguments: {} });
  assert.equal(result.isError, undefined);
  const block = result.content?.find((part) => part.type === "text");
  assert(block && block.type === "text");
  assert.match(block.text, /PROTOCOL\.md|Humanity Loop/i);

  console.log(JSON.stringify({
    client: "official-typescript-sdk",
    protocolEra: client.getProtocolEra?.(),
    toolCount: tools.length,
    getProtocol: "ok",
  }));
} finally {
  try { await transport.terminateSession(); } catch {}
  await client.close();
}
