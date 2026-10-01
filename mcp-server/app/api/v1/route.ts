import {
  getAction,
  getProject,
  getProtocol,
  getReplicationPrompt,
  listActions,
  listLiveProjects,
  searchDeadEnds,
} from "../../../lib/data";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const tool = url.searchParams.get("tool") || "help";

  try {
    switch (tool) {
      case "get_protocol":
        return Response.json(await getProtocol());
      case "list_actions":
        return Response.json(await listActions(Number(url.searchParams.get("limit") || "50")));
      case "get_action":
        return Response.json(await getAction(url.searchParams.get("id") || ""));
      case "list_live_projects":
        return Response.json(await listLiveProjects());
      case "get_project":
        return Response.json(await getProject(url.searchParams.get("slug") || ""));
      case "get_replication_prompt":
        return Response.json(await getReplicationPrompt());
      case "search_dead_ends":
        return Response.json(await searchDeadEnds(url.searchParams.get("query") || ""));
      default:
        return Response.json({
          service: "Humanity Loop read-only gateway",
          mcp: "/api/mcp",
          tools: [
            "get_protocol",
            "list_actions",
            "get_action",
            "list_live_projects",
            "get_project",
            "get_replication_prompt",
            "search_dead_ends"
          ]
        });
    }
  } catch (error) {
    return Response.json(
      { error: error instanceof Error ? error.message : String(error) },
      { status: 400 },
    );
  }
}
