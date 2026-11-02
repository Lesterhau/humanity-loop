"use client";

import { useEffect, useState } from "react";
import styles from "../page.module.css";

type Win = { id: string; title: string };
type Case = { id: string; title: string; status: string };

const raw = "https://raw.githubusercontent.com/Lesterhau/humanity-loop/main/";
const github = "https://github.com/Lesterhau/humanity-loop/blob/main/";

function verifiedWinHeadings(markdown: string): Win[] {
  const matches = [...markdown.matchAll(/^## (WIN-\d+) — (.+)$/gm)];
  const ids = new Set<string>();
  return matches.filter(m => { if (ids.has(m[1])) return false; ids.add(m[1]); return true; })
    .map(m => ({ id: m[1], title: m[2].trim() }));
}

function trackCaseHeadings(markdown: string): Case[] {
  const matches = [...markdown.matchAll(/^### (OT-\d+) — (.+)$/gm)];
  return matches.map((m, i) => {
    const begin = (m.index || 0) + m[0].length;
    const end = matches[i+1]?.index ?? markdown.length;
    const section = markdown.slice(begin, end);
    const statusLines = [...section.matchAll(/^\s*-\s*(?:\*\*)?Status:?(?:\*\*)?\s*(.+)$/gmi)]
      .map(z => z[1].trim().replace(/^\*\*|\*\*$/g, ""));
    return { id: m[1], title: m[2].trim(), status: statusLines.at(-1) || "See current source record" };
  });
}

export default function LiveLedgerFeed() {
  const [wins, setWins] = useState<Win[] | null>(null);
  const [cases, setCases] = useState<Case[] | null>(null);
  useEffect(() => {
    let cancelled = false;
    Promise.allSettled([
      fetch(raw + "WIN-LEDGER.md", { cache: "no-store" }).then(async r => {
        if (!r.ok) throw new Error("win ledger unavailable");
        return verifiedWinHeadings(await r.text());
      }),
      fetch(raw + "OUTCOME-TRACKER.md", { cache: "no-store" }).then(async r => {
        if (!r.ok) throw new Error("outcome tracker unavailable");
        return trackCaseHeadings(await r.text());
      })
    ]).then(results => {
      if (cancelled) return;
      if (results[0].status === "fulfilled") setWins(results[0].value);
      if (results[1].status === "fulfilled") setCases(results[1].value);
    });
    return () => { cancelled = true; };
  }, []);
  return (
    <section className={styles.panel} aria-label="Source-linked live progress register" style={{ marginTop: 24 }}>
      <span className={styles.number}>PUBLIC RECORDS · SOURCE-LINKED FEED</span>
      <h3>What's changed since the last website update?</h3>
      <p>The public register is read from Humanity Loop's reviewed GitHub records when you open this page. A new verified win or tracker status can appear here without editing the website's code. This is a record of documentation, not a real-time agency monitor.</p>
      {wins ? (
        <details>
          <summary>Verified win ledger — {wins.length} records currently published</summary>
          <ul>
            {wins.map(w => <li key={w.id}><strong>{w.id}:</strong> {w.title}</li>)}
          </ul>
          <p>New wins require independent evidence before anyone adds them to the ledger. <a href={github + "WIN-LEDGER.md"} target="_blank" rel="noopener noreferrer">Read the source record</a>.</p>
        </details>
      ) : <p>The latest public win ledger could not be refreshed in this visit. The verified S.T.A.R. case examples above remain available.</p>}
      {cases ? (
        <details>
          <summary>Outcome Tracker — {cases.length} tracked cases</summary>
          <ul>
            {cases.map(c => <li key={c.id}><strong>{c.id}:</strong> {c.title} — <em>{c.status}</em></li>)}
          </ul>
          <p>Case titles and statuses reflect the published tracker, not independently confirmed fresh agency changes. <a href={github + "OUTCOME-TRACKER.md"} target="_blank" rel="noopener noreferrer">Inspect the exact current record</a>.</p>
        </details>
      ) : <p>The public tracker could not be refreshed. Agency acknowledgments and changes must still be independently corroborated.</p>}
      <p style={{ fontSize: "0.8rem", color: "#57535c" }}>Only previously published public source files are read. No visitor account, private beneficiary data or GitHub login is needed. Updates to public GitHub records may take time to appear due to caching.</p>
    </section>
  );
}
