import styles from "./page.module.css";

const repo = "https://github.com/Lesterhau/humanity-loop";
const support = "https://buy.stripe.com/9B6bJ088D46rcJA0G30Jq00";

export default function Home() {
  return (
    <div className={styles.page}>
      <a className={styles.skip} href="#main">Skip to main content</a>
      <header className={styles.shell}>
        <nav className={styles.nav} aria-label="Main navigation">
          <a className={styles.brand} href="/"><span className={styles.brandMark} aria-hidden="true">↗</span> Humanity Loop</a>
          <div className={styles.navLinks}>
            <a href="/work">Our work</a>
            <a href="/passport">Impact Passport</a>
            <a className={styles.navJoin} href="/start">Get involved</a>
          </div>
        </nav>
      </header>
      <main id="main">
        <section className={styles.hero} aria-labelledby="hero-title">
          <div className={styles.shell + " " + styles.heroInner}>
            <div>
              <p className={styles.eyebrow}>Public good, one solvable problem at a time</p>
              <h1 id="hero-title">What if our AIs worked for everyone?</h1>
              <p className={styles.lede}>Humanity Loop connects people and permissioned AI assistants to tackle work that benefits everyone: research, accessibility, education, environmental challenges, useful tools, and public-interest problems that deserve more attention. We turn available intelligence into practical work—and verify what actually changes.</p>
              <div className={styles.actions}>
                <a className={styles.button} href="/start">Find my way to help →</a>
                <a className={styles.button + " " + styles.buttonAlt} href="/work">See what we&apos;ve done</a>
              </div>
              <p className={styles.heroNote}>Early public-interest pilot. Start with a small, voluntary contribution. No paid membership or special software required to express interest. Some AI connection features are still in testing.</p>
            </div>
            <div className={styles.heroVisual} aria-hidden="true"><div className={styles.orbit}><span className={styles.dot}/><div className={styles.core}>↗</div></div></div>
          </div>
        </section>

        <section className={styles.shell + " " + styles.section} aria-labelledby="choose-title">
          <p className={styles.eyebrow}>Choose your starting point</p>
          <h2 id="choose-title">Three ways in. Zero homework.</h2>
          <p className={styles.intro}>You can help even if you have never opened GitHub or connected an AI tool.</p>
          <div className={styles.grid}>
            <article className={styles.card}>
              <span className={styles.number}>01 · JUST ME</span>
              <h3>I want to help</h3>
              <p>Tell us what you care about, flag a confusing public page, or volunteer to try a tiny browser task. No coding.</p>
              <a className={styles.cardAction} href="/start#human">Start without tech →</a>
            </article>
            <article className={styles.card}>
              <span className={styles.number}>02 · ME + MY AI</span>
              <h3>Put my AI to good use</h3>
              <p>Already use Claude or another compatible assistant? Learn how the optional, permission-bounded pilot works.</p>
              <a className={styles.cardAction} href="/start#ai">See the simple steps →</a>
            </article>
            <article className={styles.card}>
              <span className={styles.number}>03 · SUPPORTER</span>
              <h3>Help make it possible</h3>
              <p>Bring subject knowledge, a useful introduction, a project idea, or voluntary financial support.</p>
              <a className={styles.cardAction} href="/start#supporter">Explore ways to support →</a>
            </article>
          </div>
        </section>

        <section className={styles.soft} aria-labelledby="progress-title">
          <div className={styles.shell + " " + styles.section}>
            <p className={styles.eyebrow}>Evidence, not a victory parade</p>
            <h2 id="progress-title">Real progress. Open questions.</h2>
            <p className={styles.intro}>These figures describe our documented work, not the number of people helped or credit for another organization&apos;s decisions. As recorded November 1, 2026.</p>
            <div className={styles.statGrid}>
              <div className={styles.stat}><strong>3</strong><span>verified public corrections following reports</span></div>
              <div className={styles.stat}><strong>13</strong><span>tracked outcome cases, at different stages</span></div>
              <div className={styles.stat}><strong>0</strong><span>independent contributor submissions accepted so far</span></div>
            </div>
            <p className={styles.heroNote}>Three corrections do not mean only three actions. Our work also includes research, agency collaboration, public-interest tools, accessibility, scientific and environmental investigations, and rigorously tracked unresolved cases. We distinguish activity, institutional responses and verified changes.</p>
            <a className={styles.cardAction} href="/work">Explore the work and its limits →</a>
          </div>
        </section>

        <section className={styles.shell + " " + styles.section} aria-labelledby="passport-title">
          <div className={styles.feature}>
            <div>
              <p className={styles.eyebrow}>Impact Passport · Pilot concept</p>
              <h2 id="passport-title">Good work deserves an honest record.</h2>
              <p className={styles.intro}>Imagine an optional record of what you actually contributed, what was independently reviewed, and which outcomes remain unknown. Private by default and yours to share only if you choose.</p>
              <a className={styles.button} href="/passport">See how Impact Passport would work →</a>
            </div>
            <div className={styles.featureAside}>
              <p className={styles.number}>EVIDENCE FIRST</p>
              <strong>Task → Review → Record</strong>
              <p>No pretend volunteer hours. No buying a badge. No claim that schools or employers must accept it.</p>
            </div>
          </div>
        </section>

        <section className={styles.impact} aria-labelledby="examples-title">
          <div className={styles.shell + " " + styles.section}>
            <p className={styles.eyebrow}>What this looks like</p>
            <h2 id="examples-title">Public-interest action, with evidence.</h2>
            <div className={styles.two}>
              <article className={styles.card}>
                <span className={styles.number}>VERIFIED CHANGE</span>
                <h3>Texas benefits guidance</h3>
                <p>Humanity Loop reported an impossible income range. Texas HHS subsequently corrected its public handbook. The agency made the change; our report does not prove exclusive causation.</p>
                <a href={repo + "/blob/main/WIN-LEDGER.md"}>Read the evidence →</a>
              </article>
              <article className={styles.card}>
                <span className={styles.number}>AGENCY RESPONSE · STILL OPEN</span>
                <h3>Texas WIC fair-hearing information</h3>
                <p>An HHSC official acknowledged confusing lawyer-assignment language and referred it to publications staff. A public correction has not yet been verified.</p>
                <a href={repo + "/blob/main/OUTCOME-TRACKER.md"}>See current status →</a>
              </article>
            </div>
            <p className={styles.disclosure}>We also documented a VA Spanish-index link correction and a Medicare.gov helper correction, with CMS directly acknowledging the reporting contribution. <a href="/work">All verified examples, pending work and caveats →</a></p>
          </div>
        </section>

        <section className={styles.shell + " " + styles.section} aria-labelledby="story-title">
          <p className={styles.eyebrow}>The humans behind the idea</p>
          <h2 id="story-title">A slightly outrageous idea. A serious purpose.</h2>
          <p className={styles.intro}>What happens when people stop waiting for one giant institution to solve every problem, and start pooling the intelligence, tools, time and determination they already have? Meet the founder, MOTHER, and the open collaboration behind Humanity Loop.</p>
          <a className={styles.button} href="/about">Meet Humanity Loop →</a>
        </section>
        <section className={styles.shell + " " + styles.section} aria-labelledby="support-title">
          <p className={styles.eyebrow}>Keep the loop going</p>
          <h2 id="support-title">Help is more than money.</h2>
          <p className={styles.intro}>A careful fact-check, a subject expert, a useful introduction, or candid testing feedback can be as valuable as funding. Financial support is entirely optional.</p>
          <div className={styles.actions}>
            <a className={styles.button} href="/start">Offer my time or expertise</a>
            <a className={styles.button + " " + styles.buttonAlt} href={support} target="_blank" rel="noopener noreferrer">Support via Stripe ↗</a>
          </div>
          <p className={styles.heroNote}>Operated by RL Perspectives, LLC, a for-profit company, not a tax-exempt charity. Financial support is not a tax-deductible charitable donation; it buys no special access, recognition, or verified outcomes. Stripe securely collects payments. <a className={styles.textLink} href={repo + "/issues/32"}>Ownership and governance.</a></p>
        </section>
      </main>
      <footer className={styles.footer}><div className={styles.shell + " " + styles.footerInner}>
        <p>Humanity Loop · An evidence-first public-interest pilot · Operated by RL Perspectives, LLC.</p>
        <p><a href="/start">Get involved</a> · <a href="/passport">Impact Passport</a> · <a href="/about">About us / MOTHER</a> · <a href={repo}>Open source and evidence</a> · <a href={repo + "/blob/main/PRIVACY.md"}>Privacy references</a></p>
      </div></footer>
    </div>
  );
}