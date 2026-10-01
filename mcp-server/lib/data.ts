const RAW_BASE = "https://raw.githubusercontent.com/Lesterhau/humanity-loop/main";
const CONTENTS_BASE = "https://api.github.com/repos/Lesterhau/humanity-loop/contents";

async function fetchText(path: string): Promise<string> {
  const response = await fetch(`${RAW_BASE}/${path}`, {
    cache: "no-store",
    headers: { "User-Agent": "HumanityLoop-MCP/0.1" },
  });
  if (!response.ok) throw new Error(`Failed to fetch ${path}: ${response.status}`);
  return response.text();
}

export async function getProtocol() {
  return { source: "PROTOCOL.md", content: await fetchText("PROTOCOL.md") };
}

export async function listActions(limit = 50) {
  const raw = await fetchText("actions.jsonl");
  const actions = raw
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
  const safeLimit = Math.max(1, Math.min(Number(limit) || 50, 500));
  return { count: actions.length, actions: actions.slice(-safeLimit) };
}

export async function getAction(id: string) {
  const { actions } = await listActions(500);
  const action = actions.find((item: any) => item.id === id);
  if (!action) throw new Error(`Action not found: ${id}`);
  return action;
}

export async function listLiveProjects() {
  const response = await fetch(`${CONTENTS_BASE}/PROJECTS`, {
    cache: "no-store",
    headers: {
      "Accept": "application/vnd.github+json",
      "User-Agent": "HumanityLoop-MCP/0.1",
    },
  });
  if (!response.ok) throw new Error(`Failed to list projects: ${response.status}`);
  const entries = await response.json();
  return (entries as any[])
    .filter((item) => item.type === "file" && item.name.endsWith(".md"))
    .map((item) => ({
      slug: item.name.replace(/\.md$/, ""),
      name: item.name,
      url: item.html_url,
    }));
}

function assertSlug(slug: string) {
  if (!/^[a-zA-Z0-9._-]+$/.test(slug)) throw new Error("Invalid project slug");
}

export async function getProject(slug: string) {
  assertSlug(slug);
  return {
    slug,
    source: `PROJECTS/${slug}.md`,
    content: await fetchText(`PROJECTS/${slug}.md`),
  };
}

export async function getReplicationPrompt() {
  return {
    source: "REPLICATION-PROMPT.md",
    content: await fetchText("REPLICATION-PROMPT.md"),
  };
}

export async function searchDeadEnds(query: string) {
  const content = await fetchText("DEAD-ENDS.md");
  const q = (query || "").trim().toLowerCase();
  if (!q) return { source: "DEAD-ENDS.md", matches: [content] };
  const lines = content.split(/\r?\n/);
  const matches: string[] = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].toLowerCase().includes(q)) {
      matches.push(lines.slice(Math.max(0, i - 2), Math.min(lines.length, i + 3)).join("\n"));
    }
  }
  return { source: "DEAD-ENDS.md", query, matches };
}
