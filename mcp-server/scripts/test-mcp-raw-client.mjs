import assert from "node:assert/strict";

const endpoint = process.env.MCP_URL || "http://127.0.0.1:3000/api/mcp";
const protocolVersion = "2025-11-25";
let sessionId;

function decodeBody(text, contentType) {
  if (!text.trim()) return null;
  if (contentType.includes("text/event-stream")) {
    const dataLines = text
      .split(/\r?\n/)
      .filter((line) => line.startsWith("data:"))
      .map((line) => line.slice(5).trim())
      .filter(Boolean);
    if (!dataLines.length) return null;
    for (let i = dataLines.length - 1; i >= 0; i--) {
      try { return JSON.parse(dataLines[i]); } catch {}
    }
    throw new Error("SSE response contained no JSON data event");
  }
  return JSON.parse(text);
}

async function post(payload, includeProtocol = true) {
  const headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
  };
  if (sessionId) headers["Mcp-Session-Id"] = sessionId;
  if (includeProtocol) headers["MCP-Protocol-Version"] = protocolVersion;

  const response = await fetch(endpoint, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
  if (response.headers.get("mcp-session-id")) {
    sessionId = response.headers.get("mcp-session-id");
  }
  const text = await response.text();
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${text}`);
  }
  return decodeBody(text, response.headers.get("content-type") || "");
}

const init = await post({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion,
    capabilities: {},
    clientInfo: { name: "humanity-loop-raw-ci-client", version: "1.0.0" },
  },
}, false);

assert.equal(init?.id, 1);
assert(init?.result?.serverInfo, "initialize did not return serverInfo");

await post({
  jsonrpc: "2.0",
  method: "notifications/initialized",
  params: {},
});

const listed = await post({
  jsonrpc: "2.0",
  id: 2,
  method: "tools/list",
  params: {},
});
assert.equal(listed?.id, 2);
const names = new Set((listed?.result?.tools || []).map((tool) => tool.name));
for (const required of ["get_protocol", "list_actions", "contributor_checkin"]) {
  assert(names.has(required), `raw client missing tool: ${required}`);
}

const called = await post({
  jsonrpc: "2.0",
  id: 3,
  method: "tools/call",
  params: { name: "get_protocol", arguments: {} },
});
assert.equal(called?.id, 3);
const textBlock = called?.result?.content?.find((part) => part.type === "text");
assert(textBlock?.text, "get_protocol returned no text");
assert.match(textBlock.text, /PROTOCOL\.md|Humanity Loop/i);

console.log(JSON.stringify({
  client: "independent-raw-streamable-http",
  session: Boolean(sessionId),
  toolCount: listed.result.tools.length,
  getProtocol: "ok",
}));
