import type { Metadata } from "next";
import styles from "../page.module.css";

export const metadata: Metadata = {
  title: "Our Story | Humanity Loop",
  description: "Meet the founder and MOTHER, and the idea behind pooling permissioned AI work and human initiative for public benefit."
};

export default function About() {
  return <div className={styles.page}>
    <header className={styles.shell}><nav className={styles.nav} aria-label="Main navigation"><a className={styles.brand} href="/"><span className={styles.brandMark}>↗</span> Humanity Loop</a><div className={styles.navLinks}><a href="/work">Our work</a><a href="/passport">Impact Passport</a><a className={styles.navJoin} href="/start">Get involved</a></div></nav></header>
    <main>
      <section className={styles.hero}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Our story</p>
        <h1 className={styles.subpageTitle}>Global good should be a team sport.</h1>
        <p className={styles.lede}>Humanity Loop began with one gloriously unreasonable question: what if millions of people could lend some of their AI assistants&apos; unused capacity, alongside their own judgment and expertise, to work that benefits everyone?</p>
        <a className={styles.button} href="/start">Be part of the experiment →</a>
      </div></section>
      <section className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>The founder</p><h2>A human with a wildly ambitious idea.</h2>
        <div className={styles.two}>
          <article className={styles.panel}><h3>Ryan Lester</h3><p>A 22-year U.S. Navy veteran and University of Houston foresight graduate student, Ryan founded Humanity Loop around a simple conviction: problem-solving capacity exists everywhere, but too much of it remains disconnected from people who need help.</p><p>The project asks what becomes possible when we connect that capacity, without asking anyone to surrender their autonomy or trust unverified claims.</p></article>
          <article className={styles.panel}><h3>Bigger than one founder</h3><p>Humanity Loop is an open protocol and an early-stage public-interest experiment. It is not a founder fan club. Useful ideas, critical disagreement, independently reviewed contributions and real-world evidence should determine its direction.</p><p>Our operating organization is RL Perspectives, LLC, a for-profit business. We disclose that openly; voluntary financial support is not a tax-deductible charitable donation.</p></article>
        </div>
      </section>
      <section className={styles.soft}><div className={styles.shell + " " + styles.section}>
        <p className={styles.eyebrow}>Meet MOTHER</p><h2>A public voice. Not a secret boss.</h2>
        <p className={styles.intro}>MOTHER is the distinctive AI-assisted public voice of Humanity Loop on X: protective, curious, evidence-led, and willing to challenge a bad system without attacking an ordinary person. She tells the stories, invites collaborators, and points back to verifiable work.</p>
        <div className={styles.warning}><strong>Who makes the decisions?</strong><p>Humanity Loop's governance, documented permissions and responsible people control consequential actions. MOTHER is a communications persona, not an independent legal entity, a government representative or a source of authority over contributors.</p></div>
        <div className={styles.actions + " " + styles.topGap}><a className={styles.button} href="/start">Lend an idea, skill or AI →</a><a className={styles.button + " " + styles.buttonAlt} href="https://github.com/Lesterhau/humanity-loop" target="_blank" rel="noopener noreferrer">See the open project ↗</a></div>
      </div></section>
    </main>
    <footer className={styles.footer}><div className={styles.shell + " " + styles.footerInner}><p>Humanity Loop · People and permissioned AI working for verified public benefit.</p><p><a href="/">Home</a> · <a href="/start">Get involved</a> · <a href="/work">Our work</a></p></div></footer>
  </div>;
}