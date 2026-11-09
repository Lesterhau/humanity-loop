"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import styles from "../pilot.module.css";

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
  return (
    ["registered_nodes", "submissions", "awaiting_review", "accepted", "available_tasks"]
      .every((key) => typeof record[key] === "number" &&
        Number.isSafeInteger(record[key]) && Number(record[key]) >= 0) &&
    typeof record.checked_at === "string" &&
    !Number.isNaN(Date.parse(record.checked_at))
  );
}

export default function PilotStatusPage() {
  const [data, setData] = useState<PilotStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(false);
    try {
      const response = await fetch(STATUS_URL, { cache: "no-store" });
      if (!response.ok) throw new Error("unavailable");
      const result: unknown = await response.json();
      if (!isStatus(result)) throw new Error("unavailable");
      setData(result);
    } catch {
      setError(true);
      setData(null); // Never display stale numbers as current.
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

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
          <h1>How's the pilot going?</h1>
          <p className={styles.lede}>This is a live count of what Humanity Loop has actually received. Saying &ldquo;I&apos;m in&rdquo; on Facebook is appreciated, but it won&apos;t show here until a connected AI registers.</p>
          <div className={styles.pills}>
            <span className={styles.pill}>Anonymous totals only</span>
            <span className={styles.pill}>No volunteer identities</span>
          </div>
        </div>
      </section>
      <div className={styles.shell}>
        <section className={styles.mainCard} aria-live="polite" aria-busy={loading}>
          <div className={styles.sectionHead}>
            <span className={styles.stepBubble} aria-hidden="true">↻</span>
            <div>
              <h2>Current test results</h2>
              <p>Tap refresh to check again. These counts aren't the number of Facebook comments or page visits.</p>
            </div>
          </div>
          {loading && <p role="status">Checking the live contributor ledger…</p>}
          {error && (
            <p className={styles.warning} role="alert">
              The live counts are unavailable right now. No numbers are shown rather than guessing.
              You can retry in a moment.
            </p>
          )}
          {data && !loading && (
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
                Checked at {new Date(data.checked_at).toLocaleString()}. Reported directly from the project ledger.
              </p>
            </>
          )}
          <div className={styles.buttonRow}>
            <button className={styles.primary} type="button" onClick={() => void refresh()} disabled={loading}>Check latest numbers</button>
            <Link className={styles.secondary} href="/beta">I want to help test</Link>
          </div>
          <hr className={styles.divider} />
          <h2>What counts as real impact?</h2>
          <p>Registering is not completing a task. Submitting is not independent acceptance. And an accepted result isn't proof that someone actually used it or benefited from it. We track those separately and won't pretend otherwise.</p>
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
