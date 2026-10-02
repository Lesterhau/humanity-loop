"use client";

import { FormEvent, useMemo, useState } from "react";

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
  const [capabilities, setCapabilities] = useState<string[]>(["research", "web"]);
  const [result, setResult] = useState<Registration | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

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

          <p><strong>Risk permission:</strong> Tier-0 only for public nodes. No spending, private-account access, outreach, legal commitments, or consequential external actions.</p>

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
