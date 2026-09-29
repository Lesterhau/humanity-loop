# Capability & Research Tooling Map

Humanity Loop should audit available tools before choosing a workflow. Do not default to generic web search when a specialized source is available.

## Current research stack

### Field shape / neglected-area discovery
- **Pendar** — exact corpus sizing, growth, institutions/countries, subfields, retraction counts.
- **SciSpace** — very broad semantic paper discovery.
- **Lune** — technical/research search, citation networks, full text, claim verification, evidence sufficiency.
- **Undermind** — Humanity Loop's persistent scholarly workspace: agentic deep literature reviews, iterative semantic/citation search, full-PDF reading via sub-agents, citation-linked notes, and preserved domain folders.

### Evidence synthesis
- **Consensus** — fast peer-reviewed synthesis and meta-analysis discovery.
- **Amass BioMedCore / TrialCore** — biomedical literature, trials, regulatory/drug/gene/patent cross-links.
- **Scite** — citation context, supporting/contrasting evidence, editorial notices, full-text excerpts.
- **Wiley Scholar Gateway** — Wiley peer-reviewed full-text evidence when service access succeeds.
- **Firecrawl Research** — cross-corpus scientific paper search, related-paper graph, passage retrieval.
- **PhysioKeys** — physiotherapy/rehabilitation specialty evidence.

### Evidence integrity
- **Scholar Sidekick** — citation existence/mismatch/retraction audits.
- **Scite** — corrections/retractions/expressions of concern and citation context.
- **Pendar** — paper verification/retraction and citation graph.
- **Lune** — claim verification.

### Public-sector / oversight research
- **GovQuery** — US government reports/oversight.
- **Firecrawl / Exa / Parallel Search** — current public web evidence and difficult site discovery.

### Data discovery
- **Dewey Data** — accessible academic/public datasets and schemas.
- domain-specific connectors when available.

### Code / implementation
- **GitHub** — code, issues, PRs, repository actions.
- **Firecrawl developer search** — public code/docs/issues/merged PR evidence.
- deployment tools such as AppDeploy/Vercel when appropriate.

## Tool-access status discovered 2026-09-28

- **Elicit:** installed, but the connected account currently does **not** have MCP/API access under its plan.
- **Undermind:** working. Workspace `Ryan's workspace` is configured (workspace_id `7792cb93-1c28-4847-9966-1b49eeef4f96`) with Humanity Loop folders for mental health, planetary systems, inner development, and scientific integrity.
- **Consensus:** working.
- **Scite:** working.
- **Amass:** working.
- **Pendar:** working.
- **Lune:** working.
- **SciSpace:** working.
- **Wiley Scholar Gateway:** available; individual queries may fail and should fall back gracefully.
- **Firecrawl:** working; call schemas must be respected.

## No credential bypass

Humanity Loop does not bypass subscription, API-key, institutional, or professional credential requirements.

When a preferred tool is gated:
1. document the missing capability;
2. use legal/open overlapping sources;
3. compare multiple substitutes for high-stakes research;
4. suggest legitimate connection/upgrade only when the marginal value justifies it.

## High-stakes research workflow

For consequential scientific/health conclusions, prefer:
1. map field with Pendar;
2. retrieve systematic reviews/meta-analyses with Consensus/Amass;
3. use **Undermind deep search** when the question is broad, contested, interdisciplinary, or important enough to merit citation-following and persistent workspace memory;
4. inspect citation support/contradiction and notices with Scite;
5. use full-text-capable tools (Undermind PDF readers, Amass, Scite OA/licensed, Lune, Wiley where available);
6. verify key citations/retractions with Scholar Sidekick/Pendar;
7. preserve important searches, papers, and synthesis notes in the relevant Undermind Humanity Loop folder;
8. use current web/government sources for implementation context;
9. explicitly record disagreements and evidence quality.

### When Undermind is the preferred tool
Use it when:
- a literature question needs comprehensive search rather than a few top papers;
- citation-network exploration may surface non-obvious evidence;
- important conclusions require reading full PDFs, tables, equations, or methods;
- a Humanity Loop research stream should accumulate knowledge across future tasks;
- we need to preserve a search and its ranked evidence for replication/audit.

Do not launch redundant deep searches if a recent workspace search already covers the question.

No single add-on is treated as ground truth.


## OSINT / weak-signal verification

Use `OSINT.md` for lawful open-source intelligence workflows: archives, media verification, geospatial/environmental evidence, corporate/government accountability, multilingual discovery, and provenance. The OSINT4ALL board is an index, not a whitelist; Humanity Loop explicitly excludes impersonation, credential abuse, doxxing, private-person surveillance, and unauthorized intrusion workflows.
