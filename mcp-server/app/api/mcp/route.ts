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
  return {
    content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }],
  };
}

const handler = createMcpHandler((server) => {
  server.registerTool(
    "get_protocol",
    {
      title: "Get Humanity Loop protocol",
      description: "Read the canonical Humanity Loop public protocol.",
      inputSchema: z.object({}),
    },
    async () => text(await getProtocol()),
  );

  server.registerTool(
    "list_actions",
    {
      title: "List Humanity Loop actions",
      description: "List recent canonical Humanity Loop action-ledger entries.",
      inputSchema: z.object({
        limit: z.number().int().min(1).max(500).optional(),
      }),
    },
    async ({ limit }) => text(await listActions(limit ?? 50)),
  );

  server.registerTool(
    "get_action",
    {
      title: "Get Humanity Loop action",
      description: "Get one Humanity Loop action by ledger ID, for example HL-042.",
      inputSchema: z.object({ id: z.string().min(1) }),
    },
    async ({ id }) => text(await getAction(id)),
  );

  server.registerTool(
    "list_live_projects",
    {
      title: "List Humanity Loop projects",
      description: "List public Humanity Loop project cards.",
      inputSchema: z.object({}),
    },
    async () => text(await listLiveProjects()),
  );

  server.registerTool(
    "get_project",
    {
      title: "Get Humanity Loop project",
      description: "Read one public Humanity Loop project card by slug.",
      inputSchema: z.object({ slug: z.string().min(1) }),
    },
    async ({ slug }) => text(await getProject(slug)),
  );

  server.registerTool(
    "get_replication_prompt",
    {
      title: "Get replication prompt",
      description: "Read the public Humanity Loop replication prompt.",
      inputSchema: z.object({}),
    },
    async () => text(await getReplicationPrompt()),
  );

  server.registerTool(
    "search_dead_ends",
    {
      title: "Search Humanity Loop dead ends",
      description: "Search Humanity Loop's public dead-end and rejected-path ledger.",
      inputSchema: z.object({ query: z.string().optional() }),
    },
    async ({ query }) => text(await searchDeadEnds(query ?? "")),
  );
});

export { handler as GET, handler as POST };
