"use client";

import { useEffect, useState } from "react";
import styles from "../page.module.css";

type IssueComment = { body?: string; created_at?: string; html_url?: string };
type LiveState = { status: string; details: string; link: string; refreshed: boolean };

const issueUrl = "https://github.com/Lesterhau/humanity-loop/issues/49";
const apiUrl = "https://api.github.com/repos/Lesterhau/humanity-loop/issues/49/comments?per_page=100";
const initial: LiveState = {
  status: "Acknowledged · correction pending",
  details: "Alameda County Social Services replied October 30 that it would forward our outdated Spanish CalFresh figures report to the appropriate team. The revised page has not been independently confirmed.",
  link: issueUrl,
  refreshed: false
};

export default function LiveCaseUpdates() {
  const [caseStatus, setCaseStatus] = useState<LiveState>(initial);
  useEffect(() => {
    let cancelled = false;
    async function refresh() {
      try {
        const res = await fetch(apiUrl, { headers: { Accept: "application/vnd.github+json" }, cache: "no-store" });
        if (!res.ok) return;
        const comments = (await res.json()) as IssueComment[];
        if (!Array.isArray(comments) || cancelled) return;
        const officialAcknowledgment = comments.find(c =>
          /verified agency acknowledgment/i.test(c.body || "") &&
          /Alameda County Social Services Agency/i.test(c.body || "")
        );
        const independentlyVerifiedCorrection = comments.find(c =>
          /independently verified (?:page )?correction/i.test(c.body || "") &&
          /FY2027/i.test(c.body || "") && /Spanish/i.test(c.body || "")
        );
        if (independentlyVerifiedCorrection) {
          setCaseStatus({
            status: "Correction documented · review official evidence",
            details: "The public case record now reports a checked FY2027 Spanish-page correction. Follow the source receipt for scope, dates and any remaining limitations; this does not imply beneficiary impact.",
            link: independentlyVerifiedCorrection.html_url || issueUrl,
            refreshed: true
          });
        } else if (officialAcknowledgment) {
          setCaseStatus({
            status: "Agency acknowledged · correction not verified",
            details: "Alameda County's Office of Public Affairs acknowledged the October 30 report and said it would forward the issue. Public correction and downstream benefit remain unverified.",
            link: officialAcknowledgment.html_url || issueUrl,
            refreshed: true
          });
        }
      } catch {
        // Keep the explicitly labeled, source-reviewed fallback instead of inventing a fresh update.
      }
    }
    refresh();
    return () => { cancelled = true; };
  }, []);

  return (
    <section aria-labelledby="alameda-live-heading" className={styles.panel} style={{ marginTop: 24, marginBottom: 24 }}>
      <span className={styles.number}>AGENCY FEEDBACK · SOURCE-LINKED STATUS</span>
      <h3 id="alameda-live-heading">Alameda County Spanish CalFresh information</h3>
      <p><strong>{caseStatus.status}.</strong> {caseStatus.details}</p>
      <p><a href={caseStatus.link} target="_blank" rel="noopener noreferrer">Read the public case receipt and latest replies →</a></p>
      <p style={{ fontSize: "0.8rem", color: "#57535c" }}>
        {caseStatus.refreshed ? "Checked against the public issue discussion on this visit." : "Last independently documented status: October 30, 2026; live refresh not confirmed."}
        {" "}New case notes can appear here without a website build. Status changes still require independently documented evidence.
      </p>
    </section>
  );
}
