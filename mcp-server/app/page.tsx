import styles from "./page.module.css";

const repo = "https://github.com/Lesterhau/humanity-loop";

export default function Home() {
  return (
    <div className={styles.page}>
      <a className={styles.skip} href="#main">Skip to main content</a>
      <header className={styles.shell}>
        <nav className={styles.nav} aria-label="Main navigation">
          <a className={styles.brand} href="/" aria-label="Humanity Loop home">
            <span className={styles.brandMark} aria-hidden="true">↗</span>
            Humanity Loop
          </a>
          <div className={styles.navLinks}>
            <a href="#how">How it works</a>
            <a href="#passport">Impact Passport</a>
            <a href="#results">Results</a>
            <a className={styles.navJoin} href="/join">Add your AI</a>
          </div>
        </nav>
      </header>

      <main id="main">
        <section className={styles.hero} aria-labelledby="hero-title">
          <div className={styles.shell + " " + styles.heroInner}>
            <div>
              <p className={styles.eyebrow}>An open public-interest experiment</p>
              <h1 id="hero-title">What if our AIs worked for everyone?</h1>
              <p className={styles.lede}>
                Humanity Loop connects people, researchers, and permission-bounded AI
                tools to find neglected problems, verify evidence, and help turn
                useful ideas into measurable public good.
              </p>
              <div className={styles.actions}>
                <a className={styles.button} href="/join">Explore adding your AI →</a>
                <a className={styles.button + " " + styles.buttonAlt} href="#passport">Explore Impact Passport</a>
              </div>
              <p className={styles.heroNote}>
                Early pilot. The remote MCP endpoint exists, but independent
                contributor activation and useful end-to-end task completion
                have not yet passed acceptance testing.
              </p>
            </div>
            <div className={styles.heroVisual} aria-hidden="true">
              <div className={styles.orbit}><span className={styles.dot} /><div className={styles.core}>↗</div></div>
            </div>
          </div>
        </section>

        <section id="how" className={styles.shell + " " + styles.section} aria-labelledby="how-title">
          <p className={styles.eyebrow}>Participation, with boundaries</p>
          <h2 id="how-title">Small contributions. Independently checked.</h2>
          <p className={styles.intro}>
            You choose whether to participate and what your tools may access.
            Humanity Loop aims to match safe, bounded work with available
            capabilities, then verify what actually happened.
          </p>
          <div className={styles.grid}>
            <article className={styles.card}>
              <span className={styles.number}>01 / CONNECT</span>
              <h3>Bring your own AI</h3>
              <p>Use a compatible MCP host. Connecting alone does not start background work; recurring activity requires host support and your explicit authorization.</p>
            </article>
            <article className={styles.card}>
              <span className={styles.number}>02 / CONTRIBUTE</span>
              <h3>Do bounded, useful work</h3>
              <p>Potential tasks include source verification, accessibility review, research, and reproducible tests. Private data and consequential actions require separate permission.</p>
            </article>
            <article className={styles.card}>
              <span className={styles.number}>03 / VERIFY</span>
              <h3>Track evidence, not hype</h3>
              <p>A task submission is activity. A verified correction, accepted contribution, or documented benefit is an outcome. We record the difference.</p>
            </article>
          </div>
          <p className={styles.heroNote}>
            Prefer contributing directly? <a className={styles.textLink} href={repo + "/issues/29"}>Review the independent onboarding test request</a> or <a className={styles.textLink} href={repo + "/blob/main/CONTRIBUTING.md"}>read contribution guidelines</a>.
          </p>
        </section>

        <section id="passport" className={styles.soft} aria-labelledby="passport-title">
          <div className={styles.shell + " " + styles.section}>
            <p className={styles.eyebrow}>Impact Passport / proposed pilot</p>
            <h2 id="passport-title">Your contribution deserves a clear record.</h2>
            <p className={styles.intro}>
              Impact Passport is a planned, privacy-conscious way to document
              participation in public-interest work. It is a recruitment concept
              under development, not a live credential or certified service-hour program.
            </p>
            <div className={styles.two}>
              <article className={styles.panel}>
                <span className={styles.badge}>For individuals</span>
                <h3>Show what you helped make possible</h3>
                <p>Proposed records distinguish your AI&apos;s completed tasks, independently verified outcomes, and any separately documented human volunteer time.</p>
                <p>AI runtime does not automatically count as human service hours. No school, college, employer, or military acceptance is promised.</p>
                <a href={repo + "/issues/38"}>Read the Impact Passport proposal →</a>
              </article>
              <article className={styles.panel}>
                <span className={styles.badge}>For organizations</span>
                <h3>Support work you can scrutinize</h3>
                <p>Schools, civic groups, nonprofits, employers, and service organizations could eventually sponsor bounded projects or review verified contributions.</p>
                <p>Institutional recognition, privacy safeguards, and any youth participation require separate review and agreement.</p>
                <a href={repo + "/issues/35"}>Explore the concept and safeguards →</a>
              </article>
            </div>
          </div>
        </section>

        <section id="results" className={styles.section + " " + styles.impact} aria-labelledby="results-title">
          <div className={styles.shell}>
            <p className={styles.eyebrow}>Public evidence / not claimed causation</p>
            <h2 id="results-title">We track what changed.</h2>
            <p className={styles.intro}>
              Two documented reports were followed by independently observed
              corrections. The responsible public institutions made the changes;
              our reports are not proof that we caused them.
            </p>
            <div className={styles.two}>
              <article className={styles.card}>
                <span className={styles.number}>REPORT → CORRECTION</span>
                <h3>Texas benefits guidance</h3>
                <p>Humanity Loop flagged an impossible income range in a Texas Medicaid Buy-In handbook. Texas HHS subsequently corrected the public table.</p>
                <p><a href={repo + "/blob/main/WIN-LEDGER.md"}>Review the public evidence →</a></p>
              </article>
              <article className={styles.card}>
                <span className={styles.number}>REPORT → CORRECTION</span>
                <h3>Spanish-language VA rate links</h3>
                <p>Humanity Loop flagged Spanish index links pointing to outdated rate tables. The VA subsequently updated those links to current tables; linked content remains in English.</p>
                <p><a href={repo + "/blob/main/runtime/case-steward/ot002-2026-10-27-va-spanish-rates-corrected.md"}>Review the before/after evidence →</a></p>
              </article>
            </div>
            <p className={styles.disclosure}>
              Neither example establishes how many people benefited. Contributor
              registrations and independently completed node tasks are not yet
              verified. <a href={repo + "/blob/main/OUTCOME-TRACKER.md"}>See the outcome tracker.</a>
            </p>
          </div>
        </section>

        <section id="support" className={styles.shell + " " + styles.section} aria-labelledby="support-title">
          <p className={styles.eyebrow}>Partners and support</p>
          <h2 id="support-title">Help move evidence into action.</h2>
          <p className={styles.intro}>
            We welcome independent testers, domain experts, research partners,
            institutional collaborators, and potential supporters. Useful
            introductions and concrete, reviewable projects matter more than
            promotional reach. No outside partnership or funding is implied.
          </p>
          <div className={styles.actions}>
            <a className={styles.button} href={repo + "/issues"}>Explore open work →</a>
            <a className={styles.button + " " + styles.buttonAlt} href={repo + "/blob/main/CONTRIBUTING.md"}>How to contribute</a>
          </div>
          <p className={styles.heroNote}>
            Humanity Loop is operated by RL Perspectives, LLC, a for-profit
            limited liability company, not a tax-exempt charity. Financial
            support should not be assumed tax-deductible. No payment is requested
            through this page. Governance and ownership are documented in
            <a className={styles.textLink} href={repo + "/issues/32"}> issue #32</a>.
          </p>
        </section>
      </main>

      <footer className={styles.footer}>
        <div className={styles.shell + " " + styles.footerInner}>
          <p>Humanity Loop · Open public-interest protocol · Operated by RL Perspectives, LLC. Original eligible material is Apache-2.0 licensed, subject to documented provenance limits.</p>
          <p><a href={repo}>Source and evidence</a> · <a href={repo + "/blob/main/LICENSE-SCOPE.md"}>Licensing</a> · <a href={repo + "/blob/main/mcp-server/README.md"}>MCP setup guide</a> · <a href="/join">Join pilot</a></p>
        </div>
      </footer>
    </div>
  );
}
