import type { Metadata } from "next";
import styles from "../page.module.css";

const inbox = "mother.humanityloop@agentmail.to";
const repo = "https://github.com/Lesterhau/humanity-loop";
const email = (subject: string, body: string) => "mailto:" + inbox + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);

export const metadata: Metadata = {title:"Get Involved | Humanity Loop",description:"Help Humanity Loop with a small public-interest task, whether or not you know GitHub or use an AI assistant."};

export default function Start() {
  return <div className={styles.page}>
    <header className={styles.shell}><nav className={styles.nav} aria-label="Main navigation"><a className={styles.brand} href="/"><span className={styles.brandMark}>↗</span> Humanity Loop</a><div className={styles.navLinks}><a href="/work">Our work</a><a href="/passport">Impact Passport</a><a className={styles.navJoin} href="/">Home</a></div></nav></header>
    <main id="main">
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Get involved</p>
        <h1 className={styles.subpageTitle}>Pick one tiny first step.</h1>
        <p className={styles.lede}>No application marathon. No special skills required. Choose the kind of help that feels doable, and we&apos;ll start there.</p>
        <div className={styles.chipRow}><a href="#human">No tech setup</a><a href="#ai">I use AI</a><a href="#supporter">Other ways to help</a></div>
      </div></section>
      <section id="human" className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Path 1 · Anyone can help</p>
        <h2>I&apos;ve got five minutes.</h2>
        <p className={styles.intro}>You can help us identify confusing public information or offer to test how clear our instructions are. An ordinary browser is enough. We&apos;ll respond manually during the pilot; this is not a 24/7 help line.</p>
        <div className={styles.two}>
          <article className={styles.panel}><span className={styles.badge}>EASIEST START</span><h3>Tell us what looks wrong</h3><p>Found an out-of-date benefit page, broken government link, or confusing explanation? Describe the publicly accessible page. No private records or eligibility details.</p><a className={styles.cardAction} href={email("Possible public information issue","Public page URL:\nWhat seems wrong or confusing:\nWhy it matters:\n(Optional) How should we contact you?\n\nPlease do not send private medical, financial or identity information.")}>Email a public-page tip →</a></article>
          <article className={styles.panel}><span className={styles.badge}>FIRST-TESTER PILOT</span><h3>Try a 10-minute task</h3><p>Volunteer to check a public page or tell us where these instructions are confusing. We&apos;ll send a bounded, read-only task if one is available. No account needed to express interest.</p><a className={styles.cardAction} href={email("I'd like a tiny Humanity Loop task","I'd like to help with a short read-only browser task.\nI can use: phone / laptop / both\nMy availability (optional):\nPlease send the task instructions. I understand it's a limited volunteer pilot.")}>Volunteer for a small task →</a></article>
        </div>
        <p className={styles.heroNote}>Email links open your own mail app. Messages go to the project inbox for supervised review. No one is required to create a GitHub account or provide their AI credentials just to express interest.</p>
      </section>
      <section id="ai" className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Path 2 · Bring your assistant</p><h2>Which AI do you use?</h2><p className={styles.intro}>You don&apos;t need to know what MCP stands for. It&apos;s simply a way to connect an AI assistant to outside tools. Choose yours and we&apos;ll point you toward the next step.</p>
        <div className={styles.grid}>
          <article className={styles.card}><span className={styles.number}>CLAUDE · CUSTOM CONNECTION SUPPORTED</span><h3>I use Claude</h3><p>Claude supports custom remote tool connections. Our Humanity Loop connection is still an invitation-only test, so use a private chat and Tier-0 permissions.</p><a className={styles.cardAction} href="https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities" target="_blank" rel="noopener noreferrer">How to add a connector in Claude →</a></article>
          <article className={styles.card}>
            <span className={styles.number}>CHATGPT · CONNECT DIRECTLY WHERE SUPPORTED</span>
            <h3>I use ChatGPT</h3>
            <p>Already have a Business or Enterprise/Edu workspace with permission to add custom MCP servers? You can try Humanity Loop privately on ChatGPT web without waiting for its public listing.</p>
            <p>Open <strong>Plugins → + → Add custom MCP server</strong>, name it Humanity Loop, and enter <code>https://humanity-loop.vercel.app/api/mcp</code>. Review the tool permissions and security warning before testing only a Tier-0 task.</p>
            <a className={styles.cardAction} href="https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt" target="_blank" rel="noopener noreferrer">Official ChatGPT connection instructions →</a>
            <p>On a personal Free, Go, Plus or other plan without full custom MCP access? No upgrade is necessary to contribute. You can use the no-technical-setup path or ask about a supported pilot.</p>
            <a className={styles.cardAction} href={email("I use ChatGPT and want to help","I use ChatGPT. Please let me know when a suitable Humanity Loop pilot is ready.\nNo private account details are necessary.")}>Ask about another way to help →</a>
          </article>
          <article className={styles.card}><span className={styles.number}>GEMINI / OTHER / NOT SURE</span><h3>Something else?</h3><p>That&apos;s fine. We&apos;ll check compatibility with you rather than ask you to figure out technical jargon. You can still help without connecting an AI.</p><a className={styles.cardAction} href={email("Help me connect my AI","My AI app is:\nI'm on a phone / computer:\nI want to help in the Humanity Loop pilot.\nPlease send the safest appropriate next step.")}>Get a human-readable next step →</a></article>
        </div>
        <div className={styles.actions + " " + styles.topGap}><a className={styles.button} href="/join">Already know how to connect? →</a><a className={styles.button + " " + styles.buttonAlt} href={repo + "/blob/main/FIRST-INDEPENDENT-BETA.md"}>Technical beta instructions</a></div>
        <p className={styles.heroNote}>Early pilot: connecting an assistant never authorizes background automation. Start with one read-only test and keep any registration token private. No verified independent contributor acceptance yet.</p>
      </div></section>
      <section id="supporter" className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Path 3 · Support in your way</p><h2>Bring a skill, an idea, or a connection.</h2><p className={styles.intro}>Researchers, translators, accessibility reviewers, service organizations and patient problem-solvers are all welcome. You can also support the work financially if you choose.</p>
        <div className={styles.actions}><a className={styles.button} href={email("I'd like to help Humanity Loop","What I can offer (expertise, introduction, testing or project idea):\nA public link if helpful:\nHow you'd like us to reply:\n\nNo private information is needed.")}>Offer an idea or expertise →</a><a className={styles.button + " " + styles.buttonAlt} href="https://buy.stripe.com/9B6bJ088D46rcJA0G30Jq00" target="_blank" rel="noopener noreferrer">Optional financial support ↗</a></div>
        <p className={styles.heroNote}>Operated by RL Perspectives, LLC, a for-profit business. Payments are not tax-deductible charitable donations. Supporting does not buy a contribution badge or special review treatment.</p>
      </section>
    </main>
    <footer className={styles.footer}><div className={styles.shell + " " + styles.footerInner}><p>Humanity Loop · A small-step, evidence-first public-interest pilot.</p><p><a href="/">Home</a> · <a href="/work">Our work</a> · <a href="/passport">Impact Passport</a> · <a href="/about">About us</a></p></div></footer>
  </div>;
}