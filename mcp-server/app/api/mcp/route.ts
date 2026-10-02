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
import {
  contributorCheckin,
  registerContributorNode,
  setContributorNodeStatus,
  submitContributorResult,
} from "../../../lib/contributor";

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
    "contributor_register",
    {
      title: "Register a Humanity Loop contributor node",
      description: "Create a pseudonymous Tier-0 contributor identity. Returns a private node token shown once. Optional setup email requires explicit consent.",
      inputSchema: z.object({
        capabilities: z.array(z.string()).max(25).optional(),
        languages: z.array(z.string()).max(12).optional(),
        host: z.string().max(80).optional(),
        user_agent_label: z.string().max(120).optional(),
        email: z.string().email().optional(),
        setup_email_consent: z.boolean().optional(),
        allow_tier1_review: z.boolean().optional(),
      }),
    },
    async (input) => text(await registerContributorNode(input)),
  );

  server.registerTool(
    "contributor_checkin",
    {
      title: "Check in as a Humanity Loop contributor node",
      description: "Check in automatically and claim at most one bounded Tier-0 task. Returns no assignment when nothing worthwhile is available.",
      inputSchema: z.object({
        node_token: z.string().min(20),
        capabilities: z.array(z.string()).max(25).optional(),
        languages: z.array(z.string()).max(12).optional(),
        host: z.string().max(80).optional(),
        user_agent_label: z.string().max(120).optional(),
      }),
    },
    async ({ node_token, ...input }) =>
      text(await contributorCheckin(node_token, input)),
  );

  server.registerTool(
    "contributor_submit",
    {
      title: "Submit contributor-node work",
      description: "Submit a claimed Tier-0 task result. Results enter quarantine for Humanity Loop verification and cannot directly alter canonical state or trigger external action.",
      inputSchema: z.object({
        node_token: z.string().min(20),
        work_id: z.string().uuid(),
        result: z.record(z.string(), z.unknown()),
        evidence: z.array(z.unknown()).max(20).optional(),
        uncertainty: z.string().max(2000).optional(),
        failure_modes: z.array(z.unknown()).max(20).optional(),
      }),
    },
    async ({ node_token, ...input }) =>
      text(await submitContributorResult(node_token, input)),
  );

  server.registerTool(
    "contributor_set_status",
    {
      title: "Pause, resume, or revoke a contributor node",
      description: "Owner control for a contributor node. Revocation is intended to be permanent for the token.",
      inputSchema: z.object({
        node_token: z.string().min(20),
        action: z.enum(["pause", "resume", "revoke"]),
      }),
    },
    async ({ node_token, action }) =>
      text(await setContributorNodeStatus(node_token, action)),
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
