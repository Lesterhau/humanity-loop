import { z } from "zod";
import { createMcpHandler } from "mcp-handler";
import {
  getAction,
  getProject,
  getProtocol,
  getReplicationPrompt,
  listActions,
  listLiveProjects,
  searchDeadEnds,
} from "../../../lib/data";

function text(value: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }] };
}

const handler = createMcpHandler(
  (server) => {
    server.tool("get_protocol", "Read the canonical Humanity Loop protocol.", {}, async () =>
      text(await getProtocol()),
    );

    server.tool(
      "list_actions",
      "List recent canonical Humanity Loop action-ledger entries.",
      { limit: z.number().int().min(1).max(500).optional() },
      async ({ limit }) => text(await listActions(limit ?? 50)),
    );

    server.tool(
      "get_action",
      "Get one Humanity Loop action by ledger ID, for example HL-042.",
      { id: z.string().min(1) },
      async ({ id }) => text(await getAction(id)),
    );

    server.tool("list_live_projects", "List public Humanity Loop project cards.", {}, async () =>
      text(await listLiveProjects()),
    );

    server.tool(
      "get_project",
      "Read one public Humanity Loop project card by slug.",
      { slug: z.string().min(1) },
      async ({ slug }) => text(await getProject(slug)),
    );

    server.tool(
      "get_replication_prompt",
      "Read the public Humanity Loop replication prompt.",
      {},
      async () => text(await getReplicationPrompt()),
    );

    server.tool(
      "search_dead_ends",
      "Search Humanity Loop's public dead-end/rejected-path ledger.",
      { query: z.string().optional() },
      async ({ query }) => text(await searchDeadEnds(query ?? "")),
    );
  },
  {
    serverInfo: {
      name: "humanity-loop",
      version: "0.1.0",
    },
  },
  { basePath: "/api" },
);

export { handler as GET, handler as POST, handler as DELETE };
