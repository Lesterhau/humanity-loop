"use client";

import Link from "next/link";
import { useState } from "react";
import styles from "../pilot.module.css";

const sourceUrl = "https://www.usa.gov/benefits";
const reportEmail = "mother.humanityloop@agentmail.to";
const reportSubject = "Humanity Loop - One-time public-page check";

const prompt = [
  "I'm helping Humanity Loop with ONE optional, read-only public-interest task. Do not connect plugins, sign me up for anything, schedule tasks, contact agencies, submit forms, or spend money.",
  "",
  "Task: Help me check how understandable one public government-benefits page is for someone seeking information.",
  "Official starting page: https://www.usa.gov/benefits",
  "",
  "1. Open the official page if browsing is available. If you cannot open it, ask me to open it in my browser and paste just the public text or link details you need. Never pretend you read it.",
  "2. Help me select ONE link or instruction on that page. Do not ask for my income, health, identity, location, account access, or benefit eligibility.",
  "3. Flag only something you can support with direct evidence: a broken link, unclear instruction, missing next step, contradiction with another cited official source, or a confirmed 'none found'. Do not claim policy is wrong on the basis of wording alone.",
  "4. Ask me to personally open and confirm the link or wording in my own browser. If I cannot verify it, label the observation UNVERIFIED.",
  "5. Write a report under 180 words with: PAGE URL, EXACT LINK OR WORDING, WHAT I PERSONALLY CONFIRMED, WHY IT MAY CONFUSE PEOPLE (or NONE FOUND), DATE CHECKED, SECOND OFFICIAL SOURCE (if relevant), and UNCERTAINTY.",
  "6. Stop after the one report. Do not send it anywhere yourself. I decide whether to email Humanity Loop.",
  "",
  "Be skeptical of your own suggestions. A plausible-sounding answer without a working public link and a human observation is not a verified issue."
].join("\n");

export default function AnyAIAssistantPage() {
  const [copied, setCopied] = useState(false);
  const [copyFailed, setCopyFailed] = useState(false);

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
          <p>Copy your checked report from your AI, or write a few sentences yourself. Email it to the project, or send it privately to the friend who invited you.</p>
          <div className={styles.buttonRow}>
            <a className={styles.primary} href={"mailto:" + reportEmail + "?subject=" + encodeURIComponent(reportSubject)}>
              Email my report
            </a>
            <Link className={styles.secondary} href="/beta">Back to friend beta</Link>
          </div>
          <p className={styles.minor}>
            Any AI app is optional. A manual check is equally welcome, and
            "nothing wrong found" is an acceptable result.
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
