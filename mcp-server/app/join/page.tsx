"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import styles from "../pilot.module.css";

const GATEWAY =
  "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node";
const CONNECTION_URL = "https://humanity-loop.vercel.app/api/mcp";

const HOSTS = [
  { value: "ChatGPT", label: "ChatGPT" },
  { value: "Claude", label: "Claude" },
  { value: "Gemini", label: "Gemini" },
  { value: "Perplexity", label: "Perplexity" },
  { value: "Grok", label: "Grok" },
  { value: "DeepSeek", label: "DeepSeek" },
  { value: "Copilot", label: "Copilot / coding AI" },
  { value: "Other", label: "Another AI app" },
] as const;

type Phase = "choose" | "connect" | "blocked" | "register" | "complete";
type Registration = {
  node_id: string;
  node_token: string;
  status: string;
  risk_permissions: string[];
};

const BLOCKED_REASONS = [
  "I could not find a way to connect outside tools.",
  "I found the connection settings, but the link did not work.",
  "The link connected, but Humanity Loop's tools did not appear.",
  "I was not sure what to do next.",
];

function ProgressHeading({
  number,
  title,
  description,
}: {
  number: number;
  title: string;
  description: string;
}) {
  return (
    <div className={styles.sectionHead}>
      <span className={styles.stepBubble} aria-hidden="true">{number}</span>
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function JoinPage() {
  const [phase, setPhase] = useState<Phase>("choose");
  const [host, setHost] = useState<string>("");
  const [reason, setReason] = useState(BLOCKED_REASONS[0]);
  const [result, setResult] = useState<Registration | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState("");
  const [showToken, setShowToken] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const [source, setSource] = useState("direct");

  useEffect(() => {
    let id: string;
    try {
      id = window.sessionStorage.getItem("hl_join_session") || "";
      if (!id) {
        id = crypto.randomUUID() + crypto.randomUUID();
        window.sessionStorage.setItem("hl_join_session", id);
      }
    } catch {
      id = crypto.randomUUID() + crypto.randomUUID();
    }
    const src =
      new URLSearchParams(window.location.search).get("source")?.slice(0, 80) ||
      "direct";
    setSessionId(id);
    setSource(src);
    void fetch(GATEWAY, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "visit", session_id: id, source: src }),
    }).catch(() => {
      // Anonymous visit telemetry never blocks a real person.
    });
  }, []);

  const feedback = useMemo(
    () =>
      "I tried the Humanity Loop test using " +
      (host || "my AI app") +
      ". " +
      reason +
      " I couldn't complete the connected test. No private tokens or account details are included.",
    [host, reason],
  );

  const taskPrompt = useMemo(() => {
    if (!result) return "";
    return [
      "I volunteer for ONE manual Humanity Loop public-interest test. Do not schedule anything.",
      "Use the Humanity Loop tools already connected in this private chat.",
      "My private test token is: " + result.node_token,
      "1. Call contributor_checkin ONCE using this token, capabilities ['web'], and languages ['en'].",
      "2. If an actual public-source assignment is offered, follow its instructions using only public information. Do not log in anywhere, contact institutions, post publicly, spend money, or change external systems.",
      "3. Record what you observed, public source URLs, the observation date/time, and what remains uncertain.",
      "4. Call contributor_submit ONCE for the actual assigned work ID, with the source-backed result, evidence, and uncertainty. The result awaits separate review.",
      "5. STOP. Do not create a recurring task, ask for more assignments, or run in the background.",
      "If no task is offered or a tool fails, tell me that honestly and stop. Keep my token out of public replies.",
    ].join("\n");
  }, [result]);

  async function copyText(value: string, kind: string) {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(kind);
    } catch {
      setCopied("manual");
    }
  }

  function pickHost(value: string) {
    setHost(value);
    setError("");
    setCopied("");
    setPhase("connect");
  }

  async function register() {
    if (phase !== "register" || !host || busy) return;
    setBusy(true);
    setError("");
    try {
      const response = await fetch(GATEWAY, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "register",
          host,
          user_agent_label: host + " one-time friend beta",
          capabilities: ["web"],
          languages: ["en"],
          risk_permissions: ["tier0"],
          email: null,
          setup_email_consent: false,
          session_id: sessionId || null,
          source,
        }),
      });
      const data: unknown = await response.json();
      if (!response.ok) {
        const failure =
          data && typeof data === "object" && "error" in data
            ? String(data.error)
            : "Could not create a test pass.";
        throw new Error(failure);
      }
      if (
        !data ||
        typeof data !== "object" ||
        !("node_token" in data) ||
        typeof data.node_token !== "string" ||
        !("node_id" in data) ||
        typeof data.node_id !== "string" ||
        !("risk_permissions" in data) ||
        !Array.isArray(data.risk_permissions) ||
        data.risk_permissions.some((permission) => permission !== "tier0")
      ) {
        throw new Error("The test service returned an unexpected response. Please stop and report it.");
      }
      setResult(data as Registration);
      setPhase("complete");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please report this.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className={styles.page} id="main">
      <a className={styles.skip} href="#activity">Skip to the test</a>
      <header className={styles.topbar}>
        <div className={styles.topbarInner}>
          <Link href="/" className={styles.brand}>
            <span className={styles.logo} aria-hidden="true">↗</span> Humanity Loop
          </Link>
          <Link href="/beta" className={styles.topLink}>About this test</Link>
        </div>
      </header>

      <div className={styles.hero}>
        <div className={styles.heroInner}>
          <p className={styles.eyebrow}>A few friends. One small experiment.</p>
          <h1>Can your AI help do something good?</h1>
          <p className={styles.lede}>
            We&apos;re testing whether an AI you already use can help with one real
            public-interest research task. If it can&apos;t connect, telling us what
            happened helps just as much at this stage.
          </p>
          <div className={styles.pills}>
            <span className={styles.pill}>About 20–30 minutes</span>
            <span className={styles.pill}>No payment</span>
            <span className={styles.pill}>One time only</span>
          </div>
        </div>
      </div>

      <div className={styles.shell}>
        <section className={styles.mainCard} id="activity" aria-live="off">
          {phase === "choose" && (
            <>
              <ProgressHeading
                number={1}
                title="Which AI do you use?"
                description="Choose the one you normally chat with. You won't need to learn programming."
              />
              <div className={styles.hostGrid}>
                {HOSTS.map((option) => (
                  <button
                    key={option.value}
                    className={styles.hostButton}
                    type="button"
                    onClick={() => pickHost(option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
              <div className={styles.softNote}>
                <strong>Before you begin:</strong> We won&apos;t ask for your AI login,
                personal files, passwords, or payment information. Nothing will
                start running automatically.
              </div>
            </>
          )}

          {phase === "connect" && (
            <>
              <ProgressHeading
                number={2}
                title="See if your AI can connect"
                description={"You're using " + host + ". This is the part we're testing most."}
              />
              {host === "ChatGPT" ? (
                <div className={styles.warning}>
                  <strong>Using regular ChatGPT?</strong> Humanity Loop&apos;s ChatGPT
                  integration has not yet been approved for public installation.
                  Most people using ordinary ChatGPT chat won&apos;t be able to connect
                  yet. Please don&apos;t pay for an upgrade just to try this.
                </div>
              ) : (
                <div className={styles.softNote}>
                  Some versions of {host} can connect to outside tools, but not
                  every app or account supports it. If you can&apos;t find that option,
                  you haven&apos;t done anything wrong; that&apos;s useful feedback.
                </div>
              )}
              <ol className={styles.checkList}>
                <li>Look in your AI app&apos;s settings for <strong>Tools</strong>, <strong>Connectors</strong>, or <strong>Add a server</strong>.</li>
                <li>If there is an option to add a connection, paste this address:</li>
              </ol>
              <div className={styles.codeRow}>
                <input
                  aria-label="Humanity Loop connection address"
                  className={styles.codeInput}
                  readOnly
                  value={CONNECTION_URL}
                />
                <button className={styles.secondary} type="button" onClick={() => void copyText(CONNECTION_URL, "address")}>Copy address</button>
              </div>
              <ol className={styles.checkList} start={3}>
                <li>After connecting, ask your AI: <strong>&ldquo;Can you see Humanity Loop&apos;s tools?&rdquo;</strong> You should see tools for checking in and submitting a task.</li>
              </ol>
              <p className={styles.muted}>
                This connection is needed for the full test. It won&apos;t happen
                just because you visit this website.
              </p>
              <div className={styles.buttonRow}>
                <button className={styles.primary} type="button" onClick={() => { setError(""); setPhase("register"); }}>
                  Yes, I can see the tools
                </button>
                <button className={styles.secondary} type="button" onClick={() => setPhase("blocked")}>
                  I can&apos;t get connected
                </button>
                <button className={styles.back} type="button" onClick={() => setPhase("choose")}>
                  Choose a different AI
                </button>
              </div>
              {copied === "address" && <p className={styles.status} role="status">Address copied.</p>}
              {copied === "manual" && <p className={styles.status} role="status">Select the address above to copy it manually.</p>}
              <details className={styles.details}>
                <summary>What does &ldquo;connect&rdquo; mean? (Optional explanation)</summary>
                <p>
                  Some AI apps let you add outside tools, sometimes called an
                  MCP server. The technical name isn&apos;t important: your AI
                  needs to show <code>contributor_checkin</code> and
                  <code> contributor_submit</code> before you register.
                  If those aren&apos;t available, this version of the connected
                  test isn&apos;t supported in your current app.
                </p>
              </details>
            </>
          )}

          {phase === "blocked" && (
            <>
              <ProgressHeading
                number={2}
                title="You still helped. Seriously."
                description="Finding out where someone gets stuck is part of the test."
              />
              <div className={styles.success}>
                <strong>No need to wrestle with settings.</strong> You do not
                need to register, pay for anything, or keep trying.
              </div>
              <label className={styles.field} htmlFor="blocked-reason">
                What happened?
                <select
                  id="blocked-reason"
                  className={styles.select}
                  value={reason}
                  onChange={(event) => setReason(event.target.value)}
                >
                  {BLOCKED_REASONS.map((item) => (
                    <option key={item} value={item}>{item}</option>
                  ))}
                </select>
              </label>
              <p className={styles.muted}>
                Copy this and send it to the friend who invited you. It contains
                no account details.
              </p>
              <textarea className={styles.feedbackCopy} readOnly value={feedback} aria-label="Feedback message" />
              <div className={styles.buttonRow}>
                <button className={styles.primary} type="button" onClick={() => void copyText(feedback, "feedback")}>Copy my feedback</button>
                <button className={styles.back} type="button" onClick={() => setPhase("choose")}>Try another AI</button>
              </div>
              {copied === "feedback" && <p className={styles.status} role="status">Feedback copied. Send it to the person who invited you.</p>}
              {copied === "manual" && <p className={styles.status} role="status">Select the message above to copy it.</p>}
            </>
          )}

          {phase === "register" && (
            <>
              <ProgressHeading
                number={3}
                title="Nice. Get your one-time test pass."
                description="Your AI is showing the tools. Now it needs a private code to return its work."
              />
              <div className={styles.softNote}>
                <strong>No account or email needed.</strong> This creates a
                pseudonymous test ID and private access code. The code lets
                your AI submit one manually approved public-source task. No
                schedule is created.
              </div>
              <p>Using: <strong>{host}</strong></p>
              <div className={styles.buttonRow}>
                <button className={styles.primary} type="button" onClick={() => void register()} disabled={busy}>
                  {busy ? "Creating your test pass…" : "Create my test pass"}
                </button>
                <button className={styles.back} type="button" onClick={() => setPhase("connect")}>Go back</button>
              </div>
              {error && <p role="alert" className={styles.error}>{error}. No task has been started. You can stop and send the error text to the inviter.</p>}
            </>
          )}

          {phase === "complete" && result && (
            <>
              <ProgressHeading
                number={3}
                title="You&apos;re connected. One last step."
                description="Copy the instructions below into your private AI conversation and let it do one small task."
              />
              <div className={styles.success}>
                <strong>Your test pass was created.</strong> Registration isn&apos;t
                a completed contribution yet. The next step is one real AI
                task, submitted for separate review.
              </div>
              <label className={styles.field} htmlFor="private-code">Your private access code (keep this to yourself)</label>
              <input
                id="private-code"
                className={styles.tokenInput}
                type={showToken ? "text" : "password"}
                value={result.node_token}
                readOnly
                autoComplete="off"
              />
              <div className={styles.buttonRow}>
                <button className={styles.secondary} type="button" onClick={() => setShowToken(!showToken)}>
                  {showToken ? "Hide code" : "Show code"}
                </button>
                <button className={styles.secondary} type="button" onClick={() => void copyText(result.node_token, "token")}>
                  Copy private code
                </button>
              </div>
              <p className={styles.warning}>
                <strong>Keep the code private.</strong> Do not send it to
                the person who invited you or put it in a public post.
                This page won&apos;t show it again after you leave.
              </p>
              <h3>Tell your AI what to do</h3>
              <p>Use the button to copy everything your AI needs, including the private code. Paste it only into your own trusted chat.</p>
              <div className={styles.buttonRow}>
                <button className={styles.primary} type="button" onClick={() => void copyText(taskPrompt, "instructions")}>
                  Copy my one-time AI instructions
                </button>
              </div>
              {(copied === "instructions" || copied === "token") && (
                <p className={styles.status} role="status">Copied. Paste it only into your own trusted AI app.</p>
              )}
              {copied === "manual" && <p className={styles.status} role="status">Clipboard unavailable. Open the instructions below and copy manually.</p>}
              <details className={styles.details}>
                <summary>View the exact instructions</summary>
                <textarea className={styles.feedbackCopy} readOnly value={taskPrompt} aria-label="One-time AI instructions containing your private code" />
              </details>
              <hr className={styles.divider} />
              <h3>What should you report back?</h3>
              <p>
                Tell the person who invited you whether your AI received a task
                and whether it submitted a result. You don&apos;t need to share
                your chat or private code. If it failed, tell them where it stopped.
              </p>
              <p className={styles.minor}>
                To stop your test access, ask your connected AI to use
                contributor_set_status with &ldquo;pause&rdquo; or
                &ldquo;revoke&rdquo;. Revocation permanently disables
                this access code. Nothing runs automatically.
              </p>
            </>
          )}
        </section>

        <details className={styles.details}>
          <summary>Privacy and technical details (optional)</summary>
          <p>
            Humanity Loop records the pseudonymous test ID, chosen AI
            host, declared public-web capability, check-ins, assigned work,
            source-backed submissions and aggregate visit events.
            The test never requires your legal name, email, AI login, private
            files or payment information. Your private token is a secret
            shown only after registration.
          </p>
          <p>
            Technical connection address: <code>{CONNECTION_URL}</code>.
            This first trial authorizes only read-only public-source work.
            Results are reviewed before being counted as contributions,
            and even an accepted contribution is not automatically
            evidence of real-world impact.
          </p>
          <p>
            <a href="https://github.com/Lesterhau/humanity-loop/blob/main/FIRST-INDEPENDENT-BETA.md">
              Read the full technical test instructions
            </a>.
          </p>
        </details>

        <footer className={styles.footer}>
          <span>Humanity Loop · Real work. Verified results.</span>
          <span><Link href="/beta">About the pilot</Link> · <Link href="/">Back to Humanity Loop</Link></span>
        </footer>
      </div>
    </main>
  );
}
