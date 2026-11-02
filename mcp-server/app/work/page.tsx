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
        <p className={styles.eyebrow}>Independently verified external changes</p><h2>Three independently verified corrections</h2>
        <div className={styles.two}>
          <article className={styles.panel}><span className={styles.badge}>VERIFIED · SEPTEMBER 30</span><h3>Texas Medicaid Buy-In guidance</h3><p>After our report about an impossible income range, Texas HHS corrected the public handbook. The agency implemented the change. The report-to-correction sequence is documented; downstream beneficiary usage is not measured.</p><a href={repo + "/blob/main/WIN-LEDGER.md"}>Read WIN-001 evidence →</a></article>
          <article className={styles.panel}><span className={styles.badge}>VERIFIED · OCTOBER 27</span><h3>VA Spanish-index rate links</h3><p>Following a report, four Spanish-index links stopped sending visitors to old rate tables and began routing to current VA.gov rates. The VA made the update. The destination rate tables remain in English.</p><a href={repo + "/blob/main/runtime/case-steward/ot002-2026-10-27-va-spanish-rates-corrected.md"}>Read WIN-002 evidence →</a></article>
          <article className={styles.panel}><span className={styles.badge}>VERIFIED · SEPTEMBER 30</span><h3>Medicare prescription-plan helper</h3><p>A September 19 report identified outdated Extra Help income thresholds in the Medicare payment-plan helper. CMS confirmed the information was updated September 30 and directly credited the report. The live helper displays the updated 2026 thresholds; beneficiary usage is unknown.</p><a href="https://www.medicare.gov/prescription-payment-plan/will-this-help-me" target="_blank" rel="noopener noreferrer">Check the current Medicare helper →</a></article>
        </div>
      </section>
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Real engagement, no claimed resolution</p><h2>Some issues are still being worked.</h2>
        <div className={styles.two}>
          <article className={styles.panel}><span className={styles.number}>ACKNOWLEDGED · OPEN</span><h3>Texas WIC fair-hearing wording</h3><p>An HHSC Appeals Division deputy director agreed the handout&apos;s lawyer-assignment language was misleading and contacted publications staff. The public PDF was still unresolved at the last documented check.</p></article>
          <article className={styles.panel}><span className={styles.number}>SOURCE ACCESS · UNVERIFIED</span><h3>Texas WIC Spanish limits</h3><p>Current application pages show correct 2026–27 figures. An older page appeared in search results with outdated figures, but direct access returned HTTP 403. That does not establish what an ordinary visitor sees.</p></article>
        </div>
        <a className={styles.cardAction} href={repo + "/blob/main/OUTCOME-TRACKER.md"}>See all tracked cases and source receipts →</a>
        <p className={styles.heroNote}>This detailed evidence record is stored in GitHub for auditability; you do not need GitHub to volunteer. <a className={styles.textLink} href="/start">Start with an email or small task instead.</a></p>
      </div></section>
      <section className={styles.shell + " " + styles.section}><h2>What we will not claim</h2><p className={styles.intro}>We cannot infer that Humanity Loop caused an agency change merely because our report came before it. We cannot infer how many people benefited without evidence. Internally completed AI tasks do not equal independent adoption or human volunteer hours.</p><a className={styles.button} href="/start">Help with the next useful check →</a></section>
    </main>
    <footer className={styles.footer}><div className={styles.shell + " " + styles.footerInner}><p>Humanity Loop · Public source corrections and careful uncertainty.</p><p><a href="/">Home</a> · <a href="/passport">Impact Passport</a></p></div></footer>
  </div>;
}