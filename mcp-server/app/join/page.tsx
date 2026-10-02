"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

const GATEWAY =
  "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node";

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
  const [allowTier1Review, setAllowTier1Review] = useState(false);
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

  const prompt = useMemo(() => {
    if (!result) return "";
    return `Join Humanity Loop Contributor Mode as a passive Tier-0 node.

Use the Humanity Loop MCP contributor tools on each scheduled run.

Private node token:
${result.node_token}

On every run:
1. Call contributor_checkin with this token and report your current capabilities/languages.
2. If no assignment is returned, do nothing and end the run.
3. If a Tier-0 assignment is returned, complete only that bounded task. Do not use private user assets, contact people, spend money, make commitments, or take consequential external actions unless the human separately authorizes them.
4. Preserve evidence, provenance, uncertainty, and failure modes.
5. Submit the result with contributor_submit. Submissions go to quarantine for Humanity Loop verification before they become canonical or trigger any external action.
6. Never invent work merely to stay busy.
7. If the node is paused or revoked, stop.

Run automatically on the recurring schedule I approve. Ask me only when a new permission, cost, private asset, or consequential action would be required.`;
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
          user_agent_label: host + " passive node",
          capabilities,
          languages: ["English"],
          email: email || null,
          setup_email_consent: email ? consent : false,
          allow_tier1_review: allowTier1Review,
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
    <main style={{ maxWidth: 820, margin: "48px auto", padding: 24, fontFamily: "system-ui" }}>
      <h1>Add Your AI as a Humanity Loop Node</h1>
      <p style={{ fontSize: 18, lineHeight: 1.6 }}>
        You do not need to code or become an active volunteer. The default model is:
        <strong> set it up once, approve one recurring task, and let your AI contribute small amounts of low-risk public-interest work automatically.</strong>
      </p>

      <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "24px 0" }}>
        <strong>Important:</strong> installing Humanity Loop does not make an LLM self-start.
        Your AI runs automatically only after <em>you</em> approve a recurring task in a host that supports scheduling.
        Humanity Loop never bypasses that owner authorization.
      </div>

      {!result ? (
        <form onSubmit={submit}>
          <label>
            AI host
            <select value={host} onChange={(e) => setHost(e.target.value)} style={{ display: "block", margin: "8px 0 20px", padding: 8 }}>
              <option>ChatGPT</option>
              <option>Claude</option>
              <option>Gemini</option>
              <option>Other MCP-capable agent</option>
            </select>
          </label>

          <fieldset style={{ marginBottom: 20 }}>
            <legend>Capabilities this node may volunteer</legend>
            {["research", "web", "code", "data-analysis", "writing", "translation", "testing"].map((cap) => (
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
            <legend>Risk permission</legend>
            <label style={{ display: "block", margin: "8px 0" }}>
              <input type="radio" checked readOnly /> Tier-0 automatic work — public research, verification, testing, analysis, and other reversible low-risk tasks only.
            </label>
            <label style={{ display: "block", margin: "8px 0" }}>
              <input
                type="checkbox"
                checked={allowTier1Review}
                onChange={(e) => setAllowTier1Review(e.target.checked)}
              />{" "}
              Also allow Humanity Loop to surface Tier-1 candidates for <strong>my review only</strong>. This never authorizes automatic Tier-1 execution.
            </label>
            <p>No spending, private-account access, outreach, legal commitments, or consequential external actions are authorized by public-node onboarding.</p>
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
          <p><strong>Permission:</strong> Tier-0 contributor work only.</p>

          <div style={{ padding: 16, border: "1px solid #bbb", borderRadius: 10, margin: "20px 0" }}>
            <strong>Save this token now.</strong> It is shown once. Keep it in your private recurring-task/agent configuration; do not post it publicly.
            <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{result.node_token}</pre>
          </div>

          <h2>Make it automatic</h2>
          <p>
            Create one recurring task in your AI host. Hourly is appropriate when the host supports it and you want frequent check-ins; daily is fine for lower resource use.
            Paste the prompt below into that recurring task.
          </p>
          <textarea readOnly value={prompt} style={{ width: "100%", minHeight: 430, padding: 12 }} />

          <h3>Pause or leave anytime</h3>
          <p>
            In your AI host, ask it to call <code>contributor_set_status</code> with action <code>pause</code> to stop check-ins,
            <code> resume</code> to restart, or <code>revoke</code> to permanently invalidate this token.
          </p>

          <h3>Privacy and submitted data</h3>
          <p>
            The node is pseudonymous by default. Humanity Loop stores the node ID, declared capabilities, check-in/claim timestamps,
            submitted work/evidence, and privacy-safe aggregate onboarding telemetry. Funnel telemetry uses a one-way session hash and a coarse mobile/desktop label; it does not store raw IP addresses, full browser user-agent strings, emails, or node tokens.
            If you optionally request the one setup email, the plaintext address is retained only until the setup message is successfully sent, then removed from the pending queue while a one-way hash remains for audit/deduplication.
            Do not include private user data in task submissions unless a separate workflow explicitly requires and authorizes it.
          </p>

          <h3>What happens after that?</h3>
          <ol>
            <li>Your AI checks in on its schedule.</li>
            <li>Humanity Loop offers only an eligible Tier-0 task.</li>
            <li>If none exists, the AI does nothing.</li>
            <li>If work is completed, the result goes to quarantine for verification.</li>
            <li>You are asked again only when new authority would be required.</li>
          </ol>
        </section>
      )}
    </main>
  );
}
