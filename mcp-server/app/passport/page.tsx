import type { Metadata } from "next";
import styles from "../page.module.css";

export const metadata: Metadata = {title:"Impact Passport | Humanity Loop",description:"How Humanity Loop plans to give contributors optional evidence-backed records without inventing volunteer hours or promising institutional credit."};

export default function Passport() {
  return <div className={styles.page}>
    <header className={styles.shell}><nav className={styles.nav} aria-label="Main navigation"><a className={styles.brand} href="/"><span className={styles.brandMark}>↗</span> Humanity Loop</a><div className={styles.navLinks}><a href="/work">Our work</a><a className={styles.navJoin} href="/start">Get involved</a></div></nav></header>
    <main>
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Impact Passport · Proposed pilot, not a credential</p>
        <h1 className={styles.subpageTitle}>A record of what you helped do. With receipts.</h1>
        <p className={styles.lede}>Contribute something useful, see how it was checked, and choose whether to share the record. That is the Impact Passport idea.</p>
        <a className={styles.button} href="/start">Explore ways to contribute →</a>
      </div></section>
      <section className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>How it would work</p><h2>One contribution. Three separate facts.</h2>
        <div className={styles.grid}>
          <article className={styles.card}><span className={styles.number}>WHAT YOU DID</span><h3>Participation</h3><p>Did you check a page, find an error, or submit useful evidence? Record the actual contribution and your role.</p></article>
          <article className={styles.card}><span className={styles.number}>WHAT WAS CHECKED</span><h3>Independent review</h3><p>Record who reviewed the evidence and whether the submission was accepted, returned for revision or rejected.</p></article>
          <article className={styles.card}><span className={styles.number}>WHAT CHANGED</span><h3>Verified outcome</h3><p>Record a real correction only when independently observed. If nothing changed yet, say so plainly.</p></article>
        </div>
      </section>
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Recognition, without the fiction</p><h2>We want contribution to feel rewarding.</h2>
        <div className={styles.two}>
          <article className={styles.panel}><h3>For individuals</h3><p>A consenting early pilot participant whose work is accepted may receive a Founding Contributor acknowledgment, a private record, and the option to share that record or be featured later.</p><p>Recognition is never guaranteed by an outside institution. AI runtime is not human volunteering time, and no one can purchase a badge.</p></article>
          <article className={styles.panel}><h3>For organizations</h3><p>Schools, nonprofits, civic groups, employers and veterans&apos; organizations could eventually review submitted evidence and decide whether to recognize it under their own requirements.</p><p>Human service time would require separately documented hours and institutional approval. We have no official recognition partnerships yet.</p></article>
        </div>
      </div></section>
      <section className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Consent, privacy, accountability</p><h2>You choose what becomes public.</h2>
        <p className={styles.intro}>The intended design is private by default, with opt-in sharing, an evidence trail, a correction route and an ability to request revocation of public display. No sensitive identifying information belongs in open task receipts. Participation by minors requires separate safeguards and responsible adult/institutional review.</p>
        <div className={styles.warning}><strong>What is live today?</strong><p>The public concept and independent-contributor pilot instructions. A production-issued Impact Passport, portable credential, partner-approved certificate, automated reward system or verified school/service-hours program is <strong>not live</strong>. We will test one consented record before building a dashboard.</p></div>
        <div className={styles.actions + " " + styles.topGap}><a className={styles.button} href="/start">Join the pilot conversation →</a><a className={styles.button + " " + styles.buttonAlt} href="https://github.com/Lesterhau/humanity-loop/issues/35">Technical design and safeguards ↗</a></div>
      </section>
    </main>
    <footer className={styles.footer}><div className={styles.shell + " " + styles.footerInner}><p>Humanity Loop · Evidence-backed contributions, never invented hours.</p><p><a href="/">Home</a> · <a href="/work">Our work</a></p></div></footer>
  </div>;
}