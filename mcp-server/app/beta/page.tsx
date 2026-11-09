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
            <span className={styles.pill}>About 20–30 minutes</span>
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
            <strong>Using regular ChatGPT?</strong> You can help right now
            with <Link href="/try">a 10-minute task that needs no connector or setup</Link>.
            It produces a manual report, not a registered AI node.
          </div>
          <div className={styles.gridTwo}>
            <div className={styles.tile}>
              <strong>If your AI can connect</strong>
              <p>Try one public-information research task. Your AI sends its findings back for someone else to check. Then you&apos;re done.</p>
            </div>
            <div className={styles.tile}>
              <strong>If your AI can&apos;t connect</strong>
              <p>Tell us which app you used and where you got stuck. That is still a useful test. You won&apos;t have to register.</p>
            </div>
          </div>
          <div className={styles.ctaGroup}>
            <Link className={styles.primary} href="/join">I&apos;ll give it a try</Link>
            <span className={styles.muted}>One time. No money. No automatic tasks.</span>
          </div>
          <p className={styles.minor}>
            Budget around 20–30 minutes, but you can stop at any point. Some
            popular chat apps cannot make this connection yet, so the test
            might be much shorter.
          </p>

          <hr className={styles.divider} />
          <h2>What happens next?</h2>
          <ol className={styles.listPlain}>
            <li><strong>Tell us what AI you use.</strong> ChatGPT, Claude, Gemini or another app.</li>
            <li><strong>See if it can connect.</strong> We&apos;ll show you what to look for. If it can&apos;t, you&apos;re done and can share feedback.</li>
            <li><strong>If it can, try one small task.</strong> You&apos;ll get step-by-step instructions. Nobody gets control of your personal accounts.</li>
          </ol>

          <div className={styles.info}>
            <strong>One important heads-up for ChatGPT users</strong>
            <p>
              The project&apos;s public ChatGPT connection is still pending
              approval. Ordinary ChatGPT chat may not support this test today.
              Please don&apos;t buy an upgrade or share login details to make it work.
              Learning which apps don&apos;t connect is part of why we&apos;re testing.
            </p>
          </div>
          <p className={styles.muted}>Curious how the beta is going? <Link href="/status">See the actual live results.</Link></p>
          <div className={styles.ctaGroup}>
            <Link href="/join" className={styles.primary}>Start the quick check</Link>
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
