import type { Metadata } from "next";
import styles from "../page.module.css";

export const dynamic = "force-static";
export const metadata: Metadata = {
  title: "Pilot capacity | Humanity Loop",
  description: "What to do when the Humanity Loop contributor pilot is at capacity.",
};

// Deliberately static. No forms, cookies set by this component, client script,
// analytics requests, registration, interest ticket, or live database call.
export default function CapacityPage() {
  return (
    <div className={styles.page}>
      <header className={styles.shell}>
        <nav className={styles.nav} aria-label="Main navigation">
          <a href="/" className={styles.brand}>Humanity Loop</a>
          <a href="/work">Verified work</a>
        </nav>
      </header>
      <main id="main">
        <section className={styles.soft}>
          <div className={styles.shell + " " + styles.section}>
            <p className={styles.eyebrow}>Early contributor pilot</p>
            <h1 className={styles.subpageTitle}>What if the pilot is full?</h1>
            <p className={styles.lede}>We admit contributors in small cohorts so that available assignments and independent review can keep pace.</p>
            <p className={styles.intro}>If registration has told you that the cohort is closed or full, please do not retry automatically or create another identity. If your registration outcome was uncertain, ask your existing inviter to reconcile it before any retry.</p>
            <article className={styles.panel}>
              <h2>Keep this page for later</h2>
              <p>Bookmark this page using your browser. No sign-up is needed to read it. An interest-ticket service is not live; there is no reserved place, queue position, admission date or promised notification.</p>
              <p>This page does not ask for your email, create a node or accept an interest ticket. Hosting providers may retain ordinary technical access logs under their own terms.</p>
              <p>When a new cohort is authorized, follow its published invitation instructions. This notice does not measure live capacity.</p>
              <div className={styles.actions}>
                <a href="/work" className={styles.button}>Explore documented work</a>
                <a href="/passport" className={styles.button + " " + styles.buttonAlt}>Learn about Impact Passport</a>
              </div>
            </article>
          </div>
        </section>
      </main>
      <footer className={styles.shell + " " + styles.footer}>
        <a href="/">Home</a> · <a href="https://github.com/Lesterhau/humanity-loop/blob/main/PRIVACY.md">Privacy notice</a>
      </footer>
    </div>
  );
}
