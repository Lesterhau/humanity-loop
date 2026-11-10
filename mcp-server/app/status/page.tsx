import Link from "next/link";
import styles from "../pilot.module.css";

export const dynamic = "force-dynamic";

const STATUS_URL =
  "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node?public_status=1";

type PilotStatus = {
  registered_nodes: number;
  submissions: number;
  awaiting_review: number;
  accepted: number;
  available_tasks: number;
  checked_at: string;
};

const items: { key: keyof Omit<PilotStatus, "checked_at">; name: string; meaning: string }[] = [
  { key: "registered_nodes", name: "Connected AI participants", meaning: "A person successfully registered an AI connection" },
  { key: "submissions", name: "Tasks submitted", meaning: "Work received, including items still awaiting review" },
  { key: "awaiting_review", name: "Awaiting review", meaning: "Submitted work that hasn't been independently accepted or rejected" },
  { key: "accepted", name: "Accepted contributions", meaning: "Reviewed submissions; this does not mean anyone has used the result yet" },
  { key: "available_tasks", name: "Open starter tasks", meaning: "One-time public-source tasks currently available" },
];

function isStatus(value: unknown): value is PilotStatus {
  if (typeof value !== "object" || value === null) return false;
  const record = value as Record<string, unknown>;
  const validCounts = ["registered_nodes", "submissions", "awaiting_review", "accepted", "available_tasks"]
    .every((key) => typeof record[key] === "number" &&
      Number.isSafeInteger(record[key]) && Number(record[key]) >= 0);
  return validCounts && typeof record.checked_at === "string" &&
    !Number.isNaN(Date.parse(record.checked_at));
}

async function readStatus(): Promise<PilotStatus | null> {
  try {
    const response = await fetch(STATUS_URL, {
      cache: "no-store",
      signal: AbortSignal.timeout(8000),
    });
    if (!response.ok) return null;
    const value: unknown = await response.json();
    return isStatus(value) ? value : null;
  } catch {
    return null;
  }
}

export default async function PilotStatusPage() {
  // Render counts into the initial HTML. Browser-based asynchronous fetches
  // previously showed a perpetual "checking..." state in read-only scrapers.
  const data = await readStatus();

  return (
    <main className={styles.page}>
      <header className={styles.topbar}>
        <div className={styles.topbarInner}>
          <Link href="/" className={styles.brand}><span className={styles.logo} aria-hidden="true">↗</span> Humanity Loop</Link>
          <Link href="/beta" className={styles.topLink}>Help test the project</Link>
        </div>
      </header>
      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <p className={styles.eyebrow}>Real progress, no inflated numbers</p>
          <h1>How&apos;s the pilot going?</h1>
          <p className={styles.lede}>This shows connected AI network activity, not all volunteer interest or manual email reports. Saying &ldquo;I&apos;m in&rdquo; on Facebook is appreciated, but it isn't a registered AI connection.</p>
          <div className={styles.pills}>
            <span className={styles.pill}>Anonymous totals only</span>
            <span className={styles.pill}>No volunteer identities</span>
          </div>
        </div>
      </section>
      <div className={styles.shell}>
        <section className={styles.mainCard}>
          <div className={styles.sectionHead}>
            <span className={styles.stepBubble} aria-hidden="true">↻</span>
            <div>
              <h2>Current test results</h2>
              <p>Refresh this page to check again. These counts aren&apos;t the number of Facebook comments or page visits.</p>
            </div>
          </div>
          {data ? (
            <>
              <div className={styles.gridTwo}>
                {items.map((item) => (
                  <div className={styles.tile} key={item.key}>
                    <strong style={{ fontSize: "2.4rem", fontWeight: 900, lineHeight: 1.2, display: "block" }}>
                      {data[item.key].toLocaleString()}
                    </strong>
                    <strong>{item.name}</strong>
                    <p>{item.meaning}</p>
                  </div>
                ))}
              </div>
              <p className={styles.minor}>
                Checked at {new Date(data.checked_at).toISOString().replace("T", " ").slice(0, 19)} UTC. Figures reflect the live project ledger.
              </p>
            </>
          ) : (
            <p className={styles.warning} role="alert">
              The live counts are unavailable right now. No numbers are shown rather than guessing.
              Please try refreshing this page.
            </p>
          )}
          <div className={styles.info}>
            <strong>Sent in a manual task report?</strong>
            <p>
              Thank you. Reports emailed from the <Link href="/try">simple
              no-connector task</Link> are reviewed separately and are
              <strong> not included in these AI connection counts</strong>.
              A zero here doesn't mean nobody volunteered or emailed a report.
            </p>
          </div>
          <div className={styles.buttonRow}>
            <a className={styles.primary} href="/status">Check latest numbers</a>
            <Link className={styles.secondary} href="/try">Try a simple task</Link>
          </div>
          <hr className={styles.divider} />
          <h2>What counts as real impact?</h2>
          <p>Registering is not completing a task. Submitting is not independent acceptance. And an accepted result isn&apos;t proof that someone actually used it or benefited from it. We track those separately and won&apos;t pretend otherwise.</p>
          <p className={styles.muted}>This page never displays names, emails, AI chat logs, private access tokens, task contents, or individual participant histories.</p>
        </section>
        <footer className={styles.footer}>
          <span>Humanity Loop · Real work. Verified results.</span>
          <span><Link href="/beta">Friend beta</Link> · <Link href="/">Homepage</Link></span>
        </footer>
      </div>
    </main>
  );
}
