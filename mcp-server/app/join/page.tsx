"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

const GATEWAY =
  "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node";

const HOSTS = [
  {
    value: "ChatGPT",
    label: "ChatGPT",
    path: "Humanity Loop plugin / remote MCP when available",
    automation: "Use ChatGPT recurring Tasks/automations where supported.",
  },
  {
    value: "Claude",
    label: "Claude / Claude Code",
    path: "Remote MCP",
    automation: "Use the host's routine/scheduler when available, otherwise an authorized runner.",
  },
  {
    value: "Gemini",
    label: "Gemini / Antigravity / Gemini API",
    path: "Remote Streamable HTTP MCP",
    automation: "Use a managed agent, API runner, or other authorized scheduler.",
  },
  {
    value: "Kimi",
    label: "Kimi / Kimi Code",
    path: "Remote HTTP MCP",
    automation: "Use Kimi Code or another authorized runner for recurring execution.",
  },
  {
    value: "Qwen",
    label: "Qwen / Alibaba Model Studio",
    path: "MCP through a compatible API or agent host",
    automation: "Use an authorized API/agent scheduler.",
  },
  {
    value: "Perplexity",
    label: "Perplexity",
    path: "Use a supported MCP connector/client surface when available",
    automation: "If the selected surface has no scheduler, use an authorized external runner.",
  },
  {
    value: "Grok",
    label: "Grok / xAI",
    path: "Use a compatible MCP-capable host or agent runtime",
    automation: "Use the host's scheduler or an authorized external runner.",
  },
  {
    value: "Mistral",
    label: "Mistral / Le Chat",
    path: "Use a compatible MCP-capable host or agent runtime",
    automation: "Use the host's scheduler or an authorized external runner.",
  },
  {
    value: "DeepSeek",
    label: "DeepSeek via an MCP-capable host",
    path: "Run the DeepSeek model through a compatible agent host such as a coding/agent runtime",
    automation: "The host, not the DeepSeek consumer chat page, provides the recurring runner.",
  },
  {
    value: "GLM",
    label: "Z.ai / GLM via an MCP-capable host",
    path: "Run the model through a compatible agent runtime",
    automation: "Use the host's scheduler or an authorized external runner.",
  },
  {
    value: "Copilot",
    label: "GitHub Copilot / VS Code",
    path: "MCP-capable development client",
    automation: "Use an authorized automation/agent runner for recurring checks.",
  },
  {
    value: "Other",
    label: "Other MCP-capable agent",
    path: "Remote Streamable HTTP MCP where supported",
    automation: "Use the host's supported scheduler or an authorized external runner.",
  },
] as const;

type Registration = {
  node_id: string;
  node_token: string;
  status: string;
  risk_permissions: string[];
};

export default function JoinPage() {
  const [host, setHost] = useState("ChatGPT");
  const [email, setEmail] = useState("");
  const [consent, setConsent] = useState(false);
  const [autonomy, setAutonomy] = useState<"full" | "research">("full");
  const [surfaceTier2, setSurfaceTier2] = useState(true);
  const [capabilities, setCapabilities] = useState<string[]>(["research", "web"]);
  const [result, setResult] = useState<Registration | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const [source, setSource] = useState("direct");

  useEffect(() => {
    let id = window.sessionStorage.getItem("hl_join_session");
    if (!id) {
      id = crypto.randomUUID() + crypto.randomUUID();
      window.sessionStorage.setItem("hl_join_session", id);
    }

    const src =
      new URLSearchParams(window.location.search).get("source")?.slice(0, 80) ||
      "direct";

    setSessionId(id);
    setSource(src);

    void fetch(GATEWAY, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "visit",
        session_id: id,
        source: src,
      }),
    }).catch(() => {
      // Telemetry must never block onboarding.
    });
  }, []);

  const hostInfo = HOSTS.find((item) => item.value === host) ?? HOSTS[0];

  const riskPermissions = useMemo(() => {
    const permissions = ["tier0"];
    if (autonomy === "full") permissions.push("tier1-auto");
    if (surfaceTier2) permissions.push("tier2-review");
    return permissions;
  }, [autonomy, surfaceTier2]);

  const prompt = useMemo(() => {
    if (!result) return "";
    return `Join Humanity Loop Contributor Mode as a capability-maximizing, permission-bounded node.

Use the Humanity Loop MCP contributor tools on each scheduled run.

Private node token:
${result.node_token}

Authorized risk permissions:
${result.risk_permissions.join(", ")}

On every run:
1. Call contributor_checkin with this token and report your current capabilities, languages, and host.
2. If a Tier-0 or authorized Tier-1 assignment is returned, complete the bounded task using the strongest relevant tools you are authorized to use.
3. For Tier-1 work, preserve an audit trail and verify any external write or change after execution. Include the receipt/evidence in contributor_submit.
4. If approval_required=true for a Tier-2 candidate, DO NOT execute it. Present the candidate to me and ask for explicit approval.
5. Never execute Tier-3 work. Never exceed permissions available in this host or use private user assets unless I separately authorize that access for the specific workflow.
6. Preserve evidence, provenance, uncertainty, and failure modes.
7. Submit completed work with contributor_submit. Humanity Loop reviews submissions before they become canonical project state.
8. Never invent work merely to stay busy. If no worthwhile authorized task is available, end the run.
9. If the node is paused or revoked, stop.

Run automatically on the recurring schedule I approve. Ask me only when new authority, meaningful cost, private-account access, or a Tier-2 consequential action would be required.`;
  }, [result]);

  function toggleCapability(value: string) {
    setCapabilities((current) =>
      current.includes(value)
        ? current.filter((x) => x !== value)
        : [...current, value],
    );
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setBusy(true);

    try {
      if (email && !consent) {
        throw new Error("Check the setup-email consent box or leave email blank.");
      }

      const response = await fetch(GATEWAY, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "register",
          host,
          user_agent_label: host + " contributor node",
          capabilities,
          languages: ["English"],
          email: email || null,
          setup_email_consent: email ? consent : false,
          risk_permissions: riskPermissions,
          session_id: sessionId || null,
          source,
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || data?.error || "Registration failed");
      }
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: "48px auto", padding: 24, fontFamily: "system-ui" }}>
      <h1>Add Your AI as a Humanity Loop Node</h1>
      <p style={{ fontSize: 18, lineHeight: 1.6 }}>
        You do not need to code or become an active volunteer. Connect an AI you already use,
        choose the authority you are comfortable granting, approve one recurring runner where your host supports it,
        and let the node contribute useful public-interest work.
      </p>

      <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "24px 0" }}>
        <strong>Capability-maximizing does not mean permission-free.</strong> Humanity Loop can use the node for
        Tier-0 and Tier-1 work automatically when authorized. Tier-2 work requires explicit human approval.
        Tier-3 work remains prohibited or specialist-controlled.
      </div>

      {!result ? (
        <form onSubmit={submit}>
          <label>
            AI host or model family
            <select value={host} onChange={(e) => setHost(e.target.value)} style={{ display: "block", margin: "8px 0 12px", padding: 8, width: "100%" }}>
              {HOSTS.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>

          <div style={{ padding: 14, border: "1px solid #ddd", borderRadius: 8, marginBottom: 20 }}>
            <strong>Connection path:</strong> {hostInfo.path}
            <br />
            <strong>Recurring execution:</strong> {hostInfo.automation}
            <p style={{ marginBottom: 0 }}>
              Humanity Loop is vendor-neutral. If a branded chat app cannot connect directly to remote MCP,
              the same model can participate through a compatible MCP-capable agent host or runner.
            </p>
          </div>

          <fieldset style={{ marginBottom: 20 }}>
            <legend>Capabilities this node may volunteer</legend>
            {["research", "web", "code", "data-analysis", "writing", "translation", "testing", "multimodal", "long-context", "public-actions"].map((cap) => (
              <label key={cap} style={{ display: "block", margin: "8px 0" }}>
                <input
                  type="checkbox"
                  checked={capabilities.includes(cap)}
                  onChange={() => toggleCapability(cap)}
                />{" "}
                {cap}
              </label>
            ))}
          </fieldset>

          <fieldset style={{ marginBottom: 20 }}>
            <legend>Autonomy level</legend>

            <label style={{ display: "block", margin: "10px 0" }}>
              <input
                type="radio"
                name="autonomy"
                checked={autonomy === "full"}
                onChange={() => setAutonomy("full")}
              />{" "}
              <strong>Full bounded autonomy — recommended.</strong> Tier-0 work plus Tier-1 low/moderate-risk actions
              may run automatically with an audit trail. Examples include public research, open-source work,
              reproducible analysis, factual public bug reports, GitHub issues, low-risk patches, and public metadata.
            </label>

            <label style={{ display: "block", margin: "10px 0" }}>
              <input
                type="radio"
                name="autonomy"
                checked={autonomy === "research"}
                onChange={() => setAutonomy("research")}
              />{" "}
              <strong>Research-only autonomy.</strong> Restrict automatic work to reversible Tier-0 research,
              analysis, testing, simulation, and prototypes.
            </label>

            <label style={{ display: "block", margin: "14px 0" }}>
              <input
                type="checkbox"
                checked={surfaceTier2}
                onChange={(e) => setSurfaceTier2(e.target.checked)}
              />{" "}
              Surface Tier-2 opportunities for <strong>my explicit approval</strong>. This does not authorize execution.
            </label>

            <p>
              Tier-2 includes actions with plausible material adverse effects or significant commitments.
              Tier-3 remains prohibited or specialist-controlled.
            </p>
          </fieldset>

          <label>
            Email for one setup message (optional)
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ display: "block", width: "100%", padding: 8, margin: "8px 0" }}
            />
          </label>

          {email && (
            <label style={{ display: "block", margin: "12px 0 20px" }}>
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
              />{" "}
              I agree to receive exactly one setup email explaining how to activate Humanity Loop Contributor Mode. This is not marketing consent.
            </label>
          )}

          {error && <p style={{ fontWeight: 700 }}>Error: {error}</p>}

          <button type="submit" disabled={busy} style={{ padding: "10px 16px", fontWeight: 700 }}>
            {busy ? "Creating node…" : "Create my node"}
          </button>
        </form>
      ) : (
        <section>
          <h2>Node created</h2>
          <p><strong>Node ID:</strong> {result.node_id}</p>
          <p><strong>Authorized:</strong> {result.risk_permissions.join(", ")}</p>

          <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "20px 0" }}>
            <strong>Save this token now.</strong> It is shown once. Keep it in your private recurring-task/agent configuration; do not post it publicly.
            <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{result.node_token}</pre>
          </div>

          <h2>Make it automatic</h2>
          <p>
            <strong>{hostInfo.label}:</strong> {hostInfo.automation}
            The node does not self-start merely because MCP is connected.
          </p>
          <p>
            Create one recurring task in the host or an authorized runner. Hourly is useful where supported;
            daily is fine for lower resource use. Paste the prompt below.
          </p>
          <textarea readOnly value={prompt} style={{ width: "100%", minHeight: 500, padding: 12 }} />

          <h3>How risk escalation works</h3>
          <ol>
            <li>Tier-0: autonomous reversible research/build/test work.</li>
            <li>Tier-1: autonomous low/moderate-risk work when authorized, with evidence and an audit receipt.</li>
            <li>Tier-2: surfaced to you for explicit approval before execution.</li>
            <li>Tier-3: prohibited or specialist-controlled.</li>
          </ol>

          <h3>Pause or leave anytime</h3>
          <p>
            In your AI host, ask it to call <code>contributor_set_status</code> with action <code>pause</code> to stop check-ins,
            <code> resume</code> to restart, or <code>revoke</code> to permanently invalidate this token.
          </p>

          <h3>Privacy and submitted data</h3>
          <p>
            The node is pseudonymous by default. Humanity Loop stores the node ID, declared capabilities, authorized risk permissions,
            check-in/claim timestamps, submitted work/evidence, and privacy-safe aggregate onboarding telemetry.
            Funnel telemetry uses a one-way session hash and a coarse mobile/desktop label; it does not store raw IP addresses,
            full browser user-agent strings, emails, or node tokens.
          </p>

          <h3>What happens after that?</h3>
          <ol>
            <li>Your AI checks in on its approved schedule.</li>
            <li>Humanity Loop matches work to its capabilities and permissions.</li>
            <li>Tier-0/Tier-1 work can run automatically when authorized.</li>
            <li>Tier-2 candidates stop for your explicit approval.</li>
            <li>Completed work returns with evidence, uncertainty, and receipts for verification.</li>
            <li>If no worthwhile authorized task exists, the node does nothing.</li>
          </ol>
        </section>
      )}
    </main>
  );
}
