import LiveCaseUpdates from "./live-case-updates";
import LiveLedgerFeed from "./live-ledger-feed";
import type { Metadata } from "next";
import styles from "../page.module.css";
const repo = "https://github.com/Lesterhau/humanity-loop";
export const metadata: Metadata = {title:"Our Work | Humanity Loop",description:"A transparent look at verified corrections, public-sector responses and unresolved public-guidance issues documented by Humanity Loop."};
export default function Work() {
  return <div className={styles.page}>
    <header className={styles.shell}><nav className={styles.nav} aria-label="Main navigation"><a className={styles.brand} href="/"><span className={styles.brandMark}>↗</span> Humanity Loop</a><div className={styles.navLinks}><a href="/passport">Impact Passport</a><a className={styles.navJoin} href="/start">Get involved</a></div></nav></header>
    <main>
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}><p className={styles.eyebrow}>Public evidence · Reviewed as of Nov 1, 2026</p><h1 className={styles.subpageTitle}>The work, including what isn&apos;t fixed yet.</h1><p className={styles.lede}>A report is not a correction. An agency acknowledgment is not a measurable benefit. These are distinct stages, and we show the difference.</p><div className={styles.statGrid}><div className={styles.stat}><strong>3</strong><span>independently observed corrections</span></div><div className={styles.stat}><strong>13</strong><span>tracked outcome cases</span></div><div className={styles.stat}><strong>0</strong><span>accepted outside node submissions</span></div></div></div></section>
      <section className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Independently verified changes · S.T.A.R. case files</p>
        <h2>What we identified, did, and verified.</h2>
        <p className={styles.intro}>Each result separates our reporting from what the responsible institution changed. No imaginary beneficiaries or inferred volunteer hours.</p>
        <div className={styles.two}>
          <article className={styles.panel}>
            <span className={styles.badge}>WIN-001 · VERIFIED</span><h3>Texas Medicaid Buy-In guidance</h3>
            <p><strong>Situation:</strong> An impossible income range appeared in a Texas Medicaid Buy-In premium chart.</p>
            <p><strong>Task:</strong> Identify the correct published range and alert the responsible handbook unit.</p>
            <p><strong>Action:</strong> Humanity Loop reported the documented contradiction September 25.</p>
            <p><strong>Result:</strong> Texas HHS corrected the public chart by September 30. Agency action and updated text were independently observed.</p>
            <p><strong>Reach:</strong> Relevant to people consulting that chart; verified individual readership and benefit not measured.</p>
            <a href={repo + "/blob/main/WIN-LEDGER.md"}>Official source and evidence ledger →</a>
          </article>
          <article className={styles.panel}>
            <span className={styles.badge}>WIN-002 · VERIFIED</span><h3>VA Spanish-index rate links</h3>
            <p><strong>Situation:</strong> Four links on a Spanish-language VA rate index led to outdated or unrelated benefit tables.</p>
            <p><strong>Task:</strong> Document the affected paths and current official rate destinations.</p>
            <p><strong>Action:</strong> We reported the link discrepancies September 25 and provided an evidence update October 20.</p>
            <p><strong>Result:</strong> On October 27, all <strong>four affected links</strong> were independently verified pointing to current 2026 VA rate tables. The VA made the changes; our exclusive causal role is unknown.</p>
            <p><strong>Reach:</strong> Four corrected navigation paths, not four people. Audience size and actual exposure are unmeasured; linked destinations remain in English.</p>
            <a href={repo + "/blob/main/runtime/case-steward/ot002-2026-10-27-va-spanish-rates-corrected.md"}>Before / report / after receipts →</a>
          </article>
          <article className={styles.panel}>
            <span className={styles.badge}>WIN-003 · VERIFIED</span><h3>Medicare prescription-plan helper</h3>
            <p><strong>Situation:</strong> A Medicare.gov helper showed outdated Extra Help income figures.</p>
            <p><strong>Task:</strong> Identify the 2026 thresholds and reach the responsible CMS team.</p>
            <p><strong>Action:</strong> We reported the discrepancy with official comparison sources September 19.</p>
            <p><strong>Result:</strong> CMS confirmed a September 30 update and explicitly acknowledged our reporting. The helper now displays <strong>$23,940</strong> for an individual and <strong>$32,460</strong> for a married couple.</p>
            <p><strong>Reach:</strong> Two corrected thresholds; the number of actual users helped is not measured. The CMS response is attribution evidence, not beneficiary analytics.</p>
            <a href="https://www.medicare.gov/prescription-payment-plan/will-this-help-me" target="_blank" rel="noopener noreferrer">Check Medicare's current helper →</a>
          </article>
        </div>
        <p className={styles.heroNote}>These are three verified corrections, with distinct evidence and attribution strengths. Modest counts such as four corrected links are defensible; we will not turn eligible population estimates into invented counts of people helped.</p>
      </section>
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Real engagement, no claimed resolution</p><h2>Feedback received. Work still open.</h2>
        <div className={styles.two}>
          <article className={styles.panel}><span className={styles.number}>ACKNOWLEDGED · OPEN</span><h3>Texas WIC fair-hearing wording</h3><p>An HHSC Appeals Division deputy director agreed the handout&apos;s lawyer-assignment language was misleading and contacted publications staff. The public PDF was still unresolved at the last documented check.</p></article>
          <article className={styles.panel}><span className={styles.number}>SOURCE ACCESS · UNVERIFIED</span><h3>Texas WIC Spanish limits</h3><p>Current application pages show correct 2026–27 figures. An older page appeared in search results with outdated figures, but direct access returned HTTP 403. That does not establish what an ordinary visitor sees.</p></article>
        </div>
        <LiveCaseUpdates />
        <LiveLedgerFeed />
        <a className={styles.cardAction} href={repo + "/blob/main/OUTCOME-TRACKER.md"}>See the full case and evidence register →</a>
        <p className={styles.heroNote}>This detailed evidence record is stored in GitHub for auditability; you do not need GitHub to volunteer. <a className={styles.textLink} href="/start">Start with an email or small task instead.</a></p>
      </div></section>
      <section className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Impact measurement</p><h2>How many people did this actually help?</h2>
        <p className={styles.intro}>That is the question we want to answer for every intervention. But a potential audience is not a count of people reached, and an agency correction is not proof of better real-world outcomes. Each win will include a documented S.T.A.R. account (Situation, Task, Action, Result) plus a separate reach and benefit assessment.</p>
        <div className={styles.grid}>
          <article className={styles.card}><span className={styles.number}>POTENTIAL AUDIENCE</span><h3>Who could benefit?</h3><p>Dated population estimates with explicit denominator, geographic and program relevance, uncertainty and source links. Never labeled as people helped.</p></article>
          <article className={styles.card}><span className={styles.number}>OBSERVED EXPOSURE</span><h3>Who actually encountered it?</h3><p>Page views, publication downloads or confirmed tool usage when responsible institutions can provide valid figures. No assumption all visitors changed behavior.</p></article>
          <article className={styles.card}><span className={styles.number}>VERIFIED BENEFIT</span><h3>What changed for someone?</h3><p>Evidence of improved comprehension, access or outcomes, with permissions and privacy protected. If unavailable, the count is not yet measured.</p></article>
        </div>
        <p className={styles.heroNote}>There are three verified public corrections, but no defensible aggregate person-level beneficiary count. Medicare and Veterans Affairs are different populations and are never interchangeable.</p>
        <a className={styles.cardAction} href={repo + "/blob/main/IMPACT-MEASUREMENT.md"}>Measurement rules and limitations →</a>
      </section>
      <section className={styles.shell + " " + styles.section}><h2>What we will not claim</h2><p className={styles.intro}>We cannot infer that Humanity Loop caused an agency change merely because our report came before it. We cannot infer how many people benefited without evidence. Internally completed AI tasks do not equal independent adoption or human volunteer hours.</p><a className={styles.button} href="/start">Help with the next useful check →</a></section>
    </main>
    <footer className={styles.footer}><div className={styles.shell + " " + styles.footerInner}><p>Humanity Loop · Public source corrections and careful uncertainty.</p><p><a href="/">Home</a> · <a href="/passport">Impact Passport</a> · <a href="/about">About us</a></p></div></footer>
  </div>;
}