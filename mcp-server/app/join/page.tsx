"use client";

import { normalizeRiskPermissions, type PublicRiskPermission } from "../../lib/risk-permissions";

import { FormEvent, useEffect, useMemo, useState } from "react";

const GATEWAY =
  "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node";

const HOSTS = [
  {
    value: "ChatGPT",
    label: "ChatGPT",
    path: "Remote MCP where host-supported; ChatGPT plugin verification pending",
    automation: "Use recurring Tasks only where this host makes the connected contributor tools available to scheduled runs.",
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
    path: "Custom remote MCP connector",
    automation: "Use Perplexity Computer workflows where available; otherwise use an authorized external runner.",
  },
  {
    value: "Grok",
    label: "Grok / xAI",
    path: "Direct custom remote MCP connector or xAI remote MCP tool",
    automation: "Use the supported Grok/xAI agent surface or an authorized external runner.",
  },
  {
    value: "Mistral",
    label: "Mistral / Le Chat",
    path: "Direct MCP Connector in Mistral Studio/Agents",
    automation: "Use Mistral Agents/Conversations or an authorized external runner.",
  },
  {
    value: "DeepSeek",
    label: "DeepSeek via an MCP-capable host",
    path: "Run the DeepSeek model through a compatible agent host such as a coding/agent runtime",
    automation: "The host, not the DeepSeek consumer chat page, provides the recurring runner.",
  },
  {
    value: "GLM",
    label: "Z.ai / GLM",
    path: "Direct Streamable HTTP MCP through the Z.ai API",
    automation: "Use an authorized API/agent scheduler.",
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

const LANGUAGE_OPTIONS = [
  "English", "Spanish", "French", "Indonesian",
  "Portuguese", "Arabic", "Hindi", "Swahili",
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
  const [autonomy, setAutonomy] = useState<"full" | "research">("research");
  const [surfaceTier2, setSurfaceTier2] = useState(false);
  const [capabilities, setCapabilities] = useState<string[]>(["research", "web"]);
  const [languages, setLanguages] = useState<string[]>(["English"]);
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
    const permissions: PublicRiskPermission[] = ["tier0"];
    if (autonomy === "full") permissions.push("tier1-auto");
    if (surfaceTier2) permissions.push("tier2-review");
    return permissions;
  }, [autonomy, surfaceTier2]);

  const prompt = useMemo(() => {
    if (!result) return "";
    return `Humanity Loop Stage-0: one manually authorized Tier-0 assignment only.

Private node token (do not disclose or post):
${result.node_token}

Permissions: ${result.risk_permissions.join(", ")}
Languages: ${languages.join(", ")}

For this single explicitly approved manual session:
1. Call contributor_checkin once with my private token, capabilities and languages.
2. If a Tier-0 public-source assignment is returned, inspect only permitted public sources. Do not contact institutions, submit forms, publish, change outside sites, or spend funds.
3. Provide dated URLs, a reproducible result, uncertainty and failure modes. Never fabricate a claim or an outcome.
4. Call contributor_submit for the claimed work ID once. Results go to quarantine pending independent human review.
5. Stop. Do not create a recurring task, daemon, extra agents, or future runs. Any later run requires separate consent.
6. Use contributor_set_status pause or revoke if requested; revocation permanently invalidates this token.
7. Keep the token, any private account data and the participant's identity out of public comments.

If no assignment is available or tools cannot connect, report UNKNOWN/blocked and stop without inventing work.`;
    }, [result, languages]);

  function toggleLanguage(value: string) {
    setLanguages((current) =>
      current.includes(value)
        ? current.length > 1 ? current.filter((x) => x !== value) : current
        : [...current, value],
    );
  }

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
          languages,
          email: email || null,
          setup_email_consent: email ? consent : false,
          risk_permissions: normalizeRiskPermissions(riskPermissions),
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
      <p><strong>Stage-0 pilot:</strong> choose Research-only Tier-0, complete one manual, read-only assignment, and do not enable a recurring schedule. Higher-risk permissions remain outside this pilot.</p>
      <p style={{ fontSize: 18, lineHeight: 1.6 }}>
        You do not need to code or become an active volunteer. Connect an AI you already use,
        choose Tier-0 authority and authorize one manual task during Stage-0,
        and submit evidence for independent review. No recurring runner is authorized yet.
      </p>

      <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "24px 0" }}>
        <strong>Capability-maximizing does not mean permission-free.</strong> Stage-0 accepts only Tier-0 public-source work. Tier-1, Tier-2 and recurring execution are disabled during this pilot.
        Tier-3 remains prohibited or specialist-controlled.
      </div>

      <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "20px 0" }}>
        <h2>Check your MCP connection before creating a node</h2>
        <p>In an MCP-capable host, configure this public Streamable HTTP MCP server:</p>
        <p><code style={{ overflowWrap: "anywhere" }}>https://humanity-loop.vercel.app/api/mcp</code></p>
        <p>
          Confirm the host exposes <code>contributor_checkin</code> and <code>contributor_submit</code>{" "}
          before registering. You do not need to create a node or generate a token to check tool availability.
          Creating a node does not install MCP tools or start a recurring task. If your chat app cannot
          connect to remote MCP, use an authorized MCP-capable agent host instead.
        </p>
        <p>
          The ChatGPT plugin is still pending publisher verification. Do not treat it as an
          available installation path until independently confirmed.
        </p>
      </div>

      <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "20px 0" }}>
        <h2>Before registering: control and privacy</h2>
        <p>
          Registration creates a pseudonymous contributor node. Humanity Loop records the node ID,
          declared capabilities, risk permissions, check-ins, task claims, submitted evidence,
          and aggregate onboarding telemetry. Do not include private user data in task submissions.
        </p>
        <p>
          Save the private node token shown after registration. In an MCP-capable host, use
          <code> contributor_set_status</code> with that token to pause, resume, or permanently revoke the node.
          Registration alone does not schedule work; you must separately authorize a recurring runner.
        </p>
        <p>
          Setup email is optional and requires both an address and explicit checkbox consent
          for one setup message, not marketing.
        </p>
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
            <strong>Future host scheduling options (not active for Stage-0):</strong> {hostInfo.automation}
            <p style={{ marginBottom: 0 }}>
              Humanity Loop is vendor-neutral. If a branded chat app cannot connect directly to remote MCP,
              the same model can participate through a compatible MCP-capable agent host or runner.
            </p>
          </div>

          <fieldset style={{ marginBottom: 20 }}>
            <legend>Languages this AI can reliably work in (choose at least one)</legend>
            {LANGUAGE_OPTIONS.map((language) => (
              <label key={language} style={{ display: "block", margin: "8px 0" }}>
                <input
                  type="checkbox"
                  checked={languages.includes(language)}
                  onChange={() => toggleLanguage(language)}
                />{" "}
                {language}
              </label>
            ))}
          </fieldset>

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
                disabled
                onChange={() => setAutonomy("full")}
              />{" "}
              <strong>Full bounded autonomy — future phase, not part of Stage-0.</strong> Tier-0 work plus Tier-1 low/moderate-risk actions
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
              <strong>Research-only Tier-0 — Stage-0 default.</strong> Restrict automatic work to reversible Tier-0 research,
              analysis, testing, simulation, and prototypes.
            </label>

            <label style={{ display: "block", margin: "14px 0" }}>
              <input
                type="checkbox"
                checked={surfaceTier2}
                disabled
                onChange={(e) => setSurfaceTier2(e.target.checked)}
              />{" "}
              Surface Tier-2 opportunities for <strong>my explicit approval</strong> (future phase; disabled during Stage-0).
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


          <h2>Complete one manual pilot task</h2>
          <p>
            <strong>{hostInfo.label}:</strong> {hostInfo.automation}
            The node does not self-start merely because MCP is connected. Stage-0 is one manual task only; do not activate a recurring runner yet.
          </p>
          <p>
            For Stage-0, use the prompt below for one manual session only. Do not set up a recurring task unless a separate future authorization permits one.
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
            <li>Your AI checks in once during the authorized manual session.</li>
            <li>Humanity Loop matches work to its capabilities and permissions.</li>
            <li>Only Tier-0 public-source work is permitted during Stage-0.</li>
            <li>Tier-2 candidates stop for your explicit approval.</li>
            <li>Completed work returns with evidence, uncertainty, and receipts for verification.</li>
            <li>If no worthwhile authorized task exists, the node does nothing.</li>
          </ol>
        </section>
      )}
    </main>
  );
}
