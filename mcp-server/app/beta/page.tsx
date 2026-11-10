import Link from "next/link";
import styles from "../pilot.module.css";

export default function BetaPage() {
  return (
    <main className={styles.page}>
      <a className={styles.skip} href="#how-it-works">Skip to the details</a>
      <header className={styles.topbar}>
        <div className={styles.topbarInner}>
          <Link href="/" className={styles.brand}>
            <span className={styles.logo} aria-hidden="true">↗</span> Humanity Loop
          </Link>
          <Link href="/" className={styles.topLink}>About Humanity Loop</Link>
        </div>
      </header>

      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <p className={styles.eyebrow}>Help us test something that could grow</p>
          <h1>What if your AI could help the world a little?</h1>
          <p className={styles.lede}>
            We&apos;re inviting a few friends to test Humanity Loop.
            The idea is to help people put the AI tools they already use toward
            useful public projects, then check whether the work actually helps.
            Right now, we&apos;re testing one small research task.
          </p>
          <div className={styles.pills}>
            <span className={styles.pill}>10–15 minutes for the simple check</span>
            <span className={styles.pill}>No coding required</span>
            <span className={styles.pill}>Free and voluntary</span>
          </div>
        </div>
      </section>

      <div className={styles.shell}>
        <section className={styles.mainCard} id="how-it-works">
          <div className={styles.sectionHead}>
            <span className={styles.stepBubble} aria-hidden="true">1</span>
            <div>
              <h2>All we need is a little help testing it.</h2>
              <p>You don&apos;t have to be a tech person. In fact, knowing where you get confused is useful feedback.</p>
            </div>
          </div>
          <div className={styles.softNote}>
            <strong>ChatGPT, Claude, Gemini, another AI, or no AI at all?</strong>
            {" "}Everyone can try <Link href="/try">the same 10–15-minute public-page check</Link>
            {" "}without installing anything. No special account needed.
            This produces an independently reviewable manual report, not a registered AI node.
          </div>
          <div className={styles.gridTwo}>
            <div className={styles.tile}>
              <strong>Easy option: anyone can help</strong>
              <p>Open one public website, check a link or instruction with or without AI, then email a short report. No connection required.</p>
            </div>
            <div className={styles.tile}>
              <strong>Advanced option: connect an AI</strong>
              <p>Some AI apps support an optional connection to claim an actual network assignment. This requires extra setup and a compatible account.</p>
            </div>
          </div>
          <div className={styles.ctaGroup}>
            <Link className={styles.primary} href="/try">Try the easy 10-minute task</Link>
            <Link className={styles.secondary} href="/join">Test an AI connection instead</Link>
          </div>
          <p className={styles.minor}>
            The no-setup check takes roughly 10–15 minutes. An optional AI
            connection can take longer and may not work in every app. You
            can stop whenever you want.
          </p>

          <hr className={styles.divider} />
          <h2>What happens next?</h2>
          <ol className={styles.listPlain}>
            <li><strong>Choose your AI, or skip AI completely.</strong> Any popular chat assistant works for the simple check.</li>
            <li><strong>Check one official public page.</strong> Look for a confusing instruction or broken link, and confirm the observation yourself.</li>
            <li><strong>Send a short report.</strong> &ldquo;Nothing wrong found&rdquo; counts. Nobody gets access to your accounts.</li>
          </ol>

          <details className={styles.details}>
            <summary>Want to connect your AI to the network instead?</summary>
            <p>
              That separate technical pilot requires an AI app that supports
              outside tools. The public ChatGPT plugin still needs approval.
              Other apps differ by plan and host. You don&apos;t need a paid upgrade,
              a new account, or a connection to help with the simple task.
            </p>
            <Link href="/join">See if your AI supports the connection</Link>
          </details>
          <p className={styles.muted}>Curious how the beta is going? <Link href="/status">See the actual live results.</Link></p>
          <div className={styles.ctaGroup}>
            <Link href="/try" className={styles.primary}>Start the simple task</Link>
            <Link href="/" className={styles.secondary}>Learn about the project</Link>
          </div>
        </section>

        <details className={styles.details}>
          <summary>Wondering about safety or privacy?</summary>
          <p>
            Nothing runs automatically. You won&apos;t be asked to pay, provide
            your legal name, share your AI password, or hand over private files.
            The connected test uses a private one-time setup code and one
            manually approved public-source research task. If you can&apos;t
            connect, there is no need to create a code.
          </p>
          <p>
            Only work that passes independent review can be counted as an
            accepted contribution. Registering alone doesn&apos;t prove any
            public benefit. You can leave at any time.
          </p>
          <p>
            <a href="https://github.com/Lesterhau/humanity-loop/issues/33">
              See the public record of what has and hasn&apos;t worked yet
            </a>.
          </p>
        </details>

        <footer className={styles.footer}>
          <span>Humanity Loop · Real work. Verified results.</span>
          <span><Link href="/">Home</Link> · <Link href="/join">Quick check</Link></span>
        </footer>
      </div>
    </main>
  );
}
