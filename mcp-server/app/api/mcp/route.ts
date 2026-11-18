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
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({}),
    },
    async () => text(await getProtocol()),
  );

  server.registerTool(
    "list_actions",
    {
      title: "List Humanity Loop actions",
      description: "List recent canonical Humanity Loop action-ledger entries.",
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({
        limit: z.number().int().min(1).max(500).optional().describe("Max public action-ledger entries to return, 1–500; default 50."),
      }),
    },
    async ({ limit }) => text(await listActions(limit ?? 50)),
  );

  server.registerTool(
    "get_action",
    {
      title: "Get Humanity Loop action",
      description: "Get one Humanity Loop action by ledger ID, for example HL-042.",
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({ id: z.string().min(1).describe("Public ledger identifier, e.g. HL-042.") }),
    },
    async ({ id }) => text(await getAction(id)),
  );

  server.registerTool(
    "list_live_projects",
    {
      title: "List Humanity Loop projects",
      description: "List public Humanity Loop project cards.",
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({}),
    },
    async () => text(await listLiveProjects()),
  );

  server.registerTool(
    "get_project",
    {
      title: "Get Humanity Loop project",
      description: "Read one public Humanity Loop project card by slug.",
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({ slug: z.string().min(1).describe("Public project slug obtained from list_live_projects.") }),
    },
    async ({ slug }) => text(await getProject(slug)),
  );

  server.registerTool(
    "get_replication_prompt",
    {
      title: "Get replication prompt",
      description: "Read the public Humanity Loop replication prompt.",
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({}),
    },
    async () => text(await getReplicationPrompt()),
  );


  server.registerTool(
    "contributor_register",
    {
      title: "Register a Humanity Loop contributor node",
      description: "Create a pseudonymous Tier-0 node after explicit consent. Writes to Humanity Loop's private ledger; returns a bearer token once. Does not schedule future work. Stage-0 rejects higher-risk permissions.",
      annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
      inputSchema: z.object({
        capabilities: z.array(z.string()).max(25).optional().describe("Public-safe capabilities such as [\"web\"]; up to 25."),
        languages: z.array(z.string()).max(12).optional().describe("Language codes such as [\"en\"]; up to 12."),
        host: z.string().max(80).optional().describe("Non-sensitive AI host name (e.g. Claude); maximum 80 characters."),
        user_agent_label: z.string().max(120).optional().describe("Optional non-identifying label for the operator's agent."),
        email: z.string().email().optional().describe("Optional contact email; only provide with explicit setup_email_consent."),
        setup_email_consent: z.boolean().optional().describe("True only when operator separately consents to a setup email; otherwise omit."),
        risk_permissions: z.array(z.enum(["tier0", "tier1-auto", "tier2-review"])).max(3).optional().describe("Current Stage-0 permits [\"tier0\"] only; higher-risk values are rejected."),
        allow_tier1_review: z.boolean().optional().describe("Reserved future capability: not authorized in Stage-0; omit or false."),
      }),
    },
    async (input) => text(await registerContributorNode(input)),
  );

  server.registerTool(
    "contributor_checkin",
    {
      title: "Check in as a Humanity Loop contributor node",
      description: "Record a consented check-in and claim at most one eligible Tier-0 public-web task with a two-hour lease. Writes to Humanity Loop's ledger; does not schedule an agent or authorize outside-site writes.",
      annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
      inputSchema: z.object({
        node_token: z.string().min(20).describe("Private bearer token returned at registration; never log or publish."),
        capabilities: z.array(z.string()).max(25).optional().describe("Currently available public-safe capabilities such as [\"web\"]."),
        languages: z.array(z.string()).max(12).optional().describe("Language codes such as [\"en\"]."),
        host: z.string().max(80).optional().describe("Non-sensitive current AI host label."),
        user_agent_label: z.string().max(120).optional().describe("Optional non-identifying agent label."),
      }),
    },
    async ({ node_token, ...input }) =>
      text(await contributorCheckin(node_token, input)),
  );

  server.registerTool(
    "contributor_submit",
    {
      title: "Submit contributor-node work",
      description: "Write a result and public-source evidence to a quarantined review record for the caller's claimed task. Human acceptance is separate; submission is not public benefit.",
      annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
      inputSchema: z.object({
        node_token: z.string().min(20).describe("Secret node bearer token; never expose in evidence or transcripts."),
        work_id: z.string().uuid().describe("Exact work UUID returned by a current, unexpired check-in assignment."),
        result: z.record(z.string(), z.unknown()).describe("JSON object of factual observation, public source URL, status and UTC timestamp."),
        evidence: z.array(z.unknown()).max(20).optional().describe("Up to 20 public-source URLs or redacted observations, never private data."),
        uncertainty: z.string().max(2000).optional().describe("Candid verification limitations and unknowns, max 2000 characters."),
        failure_modes: z.array(z.unknown()).max(20).optional().describe("Up to 20 descriptions of failures or source access limitations."),
      }),
    },
    async ({ node_token, ...input }) =>
      text(await submitContributorResult(node_token, input)),
  );

  server.registerTool(
    "contributor_set_status",
    {
      title: "Pause, resume, or revoke a contributor node",
      description: "Pause, resume or permanently revoke a node token in the private ledger. Revocation blocks token access but does not delete historical audit records.",
      annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: false },
      inputSchema: z.object({
        node_token: z.string().min(20).describe("Private bearer token authorizing this status change; never publish."),
        action: z.enum(["pause", "resume", "revoke"]).describe("pause, resume, or permanently revoke this token; revocation does not erase historical records."),
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
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
      inputSchema: z.object({ query: z.string().optional().describe("Optional public dead-end search terms; omit to list results.") }),
    },
    async ({ query }) => text(await searchDeadEnds(query ?? "")),
  );
});

export { handler as GET, handler as POST };
