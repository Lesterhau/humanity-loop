"use client";

import Link from "next/link";
import { useState } from "react";
import styles from "../pilot.module.css";

const sourceUrl = "https://www.usa.gov/benefits";
const reportEmail = "mother.humanityloop@agentmail.to";
const reportSubject = "Humanity Loop - One-time public-page check";

const prompt = [
  "I'm helping Humanity Loop with ONE optional, read-only public-interest task. Do not connect plugins, sign me up, schedule tasks, contact agencies, submit forms, or spend money.",
  "",
  "Starting official page: https://www.usa.gov/benefits",
  "Goal: Check ONE public government-benefits page link for clarity or a real navigation problem. A valid outcome can also be NO ISSUE FOUND or COULD NOT VERIFY.",
  "",
  "1. If live browsing works, open the official page and select ONE link. State the exact official URLs actually accessed. Never claim that you visited a page if a text reader only returned a shell or an automated browser was blocked.",
  "2. If you CANNOT browse, do NOT request that I paste the entire page or abandon the test. Give me one simple human-check alternative: I can open https://www.usa.gov/help-with-utility-bills and check whether its official phone/internet/energy assistance information matches the 'Help with utility bills' link on https://www.usa.gov/benefits. Ask me to reply with 'Looks accurate', 'Something confusing: [public wording]', or 'Couldn't check'. You may use this suggestion without pretending to have opened either site.",
  "3. Do not ask for income, health, identity, location, benefits eligibility, passwords or private records. Do not log in, file complaints or contact agencies.",
  "4. After this one attempt, ALWAYS provide a short report under 180 words, even if the site was inaccessible. Include PAGE URL, EXACT LINK OR WORDING (if observed), AI READING STATUS (live page / cached page / blocked), HUMAN CHECK (confirmed by me / not confirmed), FINDING (possible issue / no issue observed / unable to verify), OFFICIAL SOURCE URLs, DATE, and UNCERTAINTY.",
  "5. Do not write that I personally confirmed anything unless I explicitly tell you I did. A model's reading is not a human check. If I have not confirmed, clearly mark NOT HUMAN-VERIFIED. This is an honest test outcome, not an accepted correction.",
  "6. Stop after the single report. I choose whether to email it or submit a brief account of where I got stuck.",
  "",
  "Don't force a problem, inflate evidence, or infer that an automated 403 means ordinary visitors are blocked."
].join("\n");

export default function AnyAIAssistantPage() {
  const [copied, setCopied] = useState(false);
  const [copyFailed, setCopyFailed] = useState(false);
  const [outcome, setOutcome] = useState<"" | "no_issue" | "possible_issue" | "unable">("");
  const [notes, setNotes] = useState("");
  const [reportCopied, setReportCopied] = useState(false);
  const outcomeText = {
    no_issue: "I personally checked the public page and found no issue.",
    possible_issue: "I personally checked the public page and have a possible issue for independent review.",
    unable: "I could not personally verify the page or the AI could not retrieve it.",
  };
  const reportReady = outcome !== "" && (outcome !== "possible_issue" || notes.trim().length >= 15);
  const reportBody = [
    "Humanity Loop manual friend-beta report",
    "Task: one public-page check (not a connected AI node).",
    "Starting source: " + sourceUrl,
    "Outcome: " + (outcome ? outcomeText[outcome] : "(not selected)"),
    "Observation / checked URL / exact public wording:",
    notes.trim() || "(no further details)",
    "Review status: UNREVIEWED. No independent acceptance or measured outcome claimed.",
    "No private information or full AI chat log is needed.",
  ].join("\n");
  const mailto = "mailto:" + reportEmail + "?subject=" +
    encodeURIComponent(reportSubject) + "&body=" + encodeURIComponent(reportBody);

  async function copyReport() {
    if (!reportReady) return;
    try {
      await navigator.clipboard.writeText(reportBody);
      setReportCopied(true);
    } catch {
      setReportCopied(false);
    }
  }

  async function copyPrompt() {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopied(true);
      setCopyFailed(false);
    } catch {
      setCopyFailed(true);
    }
  }

  return (
    <main className={styles.page}>
      <header className={styles.topbar}>
        <div className={styles.topbarInner}>
          <Link href="/" className={styles.brand}>
            <span className={styles.logo} aria-hidden="true">↗</span> Humanity Loop
          </Link>
          <Link href="/beta" className={styles.topLink}>Friend beta</Link>
        </div>
      </header>

      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <p className={styles.eyebrow}>No plugins. No coding. One small task.</p>
          <h1>Use any AI to help. Or do it yourself.</h1>
          <p className={styles.lede}>
            ChatGPT, Claude, Gemini, Copilot, Grok, Perplexity, or another AI?
            You can use any of them for one public-page check. No plugin,
            coding, or special setup. No AI at all? You can do the check yourself.
          </p>
          <div className={styles.pills}>
            <span className={styles.pill}>About 10–15 minutes</span>
            <span className={styles.pill}>Free and voluntary</span>
            <span className={styles.pill}>No special setup</span>
          </div>
        </div>
      </section>

      <div className={styles.shell}>
        <section className={styles.mainCard}>
          <div className={styles.sectionHead}>
            <span className={styles.stepBubble} aria-hidden="true">1</span>
            <div>
              <h2>Copy the one-time task</h2>
              <p>Use the AI you already chat with, or skip this step and check the page yourself.</p>
            </div>
          </div>
          <div className={styles.softNote}>
            <strong>Not using ChatGPT?</strong> That's fine. This same prompt
            works with other AI assistants too. <strong>Not using any AI?</strong>
            Open the USA.gov link in step 2, pick one public link or instruction
            to check, and email what you observed in step 3.
          </div>
          <div className={styles.buttonRow}>
            <button className={styles.primary} type="button" onClick={() => void copyPrompt()}>
              Copy the one-time AI prompt
            </button>
          </div>
          {copied && <p className={styles.status} role="status">Copied. Open your preferred AI app and paste it into a new conversation.</p>}
          {copyFailed && <p className={styles.warning} role="status">Clipboard unavailable. You can select and copy the prompt in the box below.</p>}
          <details className={styles.details}>
            <summary>Read or manually copy the complete instructions</summary>
            <textarea aria-label="One-time AI task instructions" className={styles.feedbackCopy} readOnly rows={16} value={prompt} />
          </details>

          <hr className={styles.divider} />
          <div className={styles.sectionHead}>
            <span className={styles.stepBubble} aria-hidden="true">2</span>
            <div>
              <h2>Check the public page yourself</h2>
              <p>If you use AI, let it help with the reading. Either way, check the evidence yourself.</p>
            </div>
          </div>
          <p>
            Starting website: <a href={sourceUrl} target="_blank" rel="noopener noreferrer">
              USA.gov — government benefits
            </a>. Pick one link or instruction to inspect.
            If the AI cannot browse, open the link yourself and paste only public text.
          </p>
          <div className={styles.softNote}>
            <strong>Finding nothing wrong counts as an honest result.</strong> You are not expected
            to invent a problem. Never enter personal benefit details, medical information,
            passwords, or financial records into this test.
          </div>

          <hr className={styles.divider} />
          <div className={styles.sectionHead}>
            <span className={styles.stepBubble} aria-hidden="true">3</span>
            <div>
              <h2>Send us the short report</h2>
              <p>Send only the public-page finding you personally checked, or &ldquo;none found.&rdquo;</p>
            </div>
          </div>
          <p>Choose what happened, then write a few sentences or paste your AI&apos;s short draft. We welcome honest negative and blocked results. Only select a personally checked outcome if you actually opened the public page yourself.</p>
          <label className={styles.field} htmlFor="report-outcome">
            What happened?
            <select
              id="report-outcome"
              className={styles.select}
              value={outcome}
              onChange={(event) => { setOutcome(event.target.value as typeof outcome); setReportCopied(false); }}
            >
              <option value="">Choose one result</option>
              <option value="no_issue">I checked the public page. No issue found.</option>
              <option value="possible_issue">I checked the public page. Something may need fixing.</option>
              <option value="unable">I couldn't check, or my AI couldn't read the page.</option>
            </select>
          </label>
          <label className={styles.field} htmlFor="report-notes">
            Short report or obstacle (public information only)
            <textarea
              id="report-notes"
              className={styles.feedbackCopy}
              rows={5}
              maxLength={1200}
              value={notes}
              onChange={(event) => { setNotes(event.target.value); setReportCopied(false); }}
              placeholder="For a possible issue: include the official page URL, exact wording, what you saw, and why it might confuse someone. For no issue or a blocked test: one sentence is enough."
            />
          </label>
          {outcome === "possible_issue" && notes.trim().length < 15 && (
            <p className={styles.warning}>Include at least a short description and the public URL or wording before emailing a possible issue.</p>
          )}
          <div className={styles.buttonRow}>
            {reportReady ? (
              <a className={styles.primary} href={mailto}>Open email with my report</a>
            ) : (
              <span className={styles.secondary} aria-disabled="true">Choose a result to prepare email</span>
            )}
            <button className={styles.secondary} type="button" disabled={!reportReady} onClick={() => void copyReport()}>
              Copy my report instead
            </button>
          </div>
          {reportCopied && <p className={styles.status} role="status">Report copied. You can send it privately to the person who invited you.</p>}
          <p className={styles.muted}>The email button opens your mail app; it does not send anything until you review and send it. If you need to stop, just choose &ldquo;couldn&apos;t check&rdquo;. No fabricated findings required.</p>
          <p className={styles.minor}>
            Any AI app is optional. A manual check is equally welcome, and
            "nothing wrong found" is an acceptable result.
          </p>
          <p className={styles.minor}>
            This form stays in your browser until you choose to use your own email or copy the text.
            It creates no node, background task, account or automatic submission.
          </p>
          <p className={styles.minor}>
            Emailing reveals your email address to the project; a private message to your friend
            is another option. Don&apos;t include private conversations, accounts, names,
            screenshots with sensitive information, or anyone else&apos;s records.
          </p>
          <div className={styles.info}>
            <strong>What happens to the report?</strong>
            <p>
              It is a <strong>manual, unreviewed observation</strong>, not a registered AI node
              or automatically accepted contribution. A separate reviewer must check sources
              before Humanity Loop treats it as a verified result, and any outside organization
              decides whether to adopt a proposed correction.
            </p>
          </div>
        </section>
        <footer className={styles.footer}>
          <span>Humanity Loop · Real work. Verified results.</span>
          <span><Link href="/status">Live pilot status</Link> · <Link href="/">Home</Link></span>
        </footer>
      </div>
    </main>
  );
}
