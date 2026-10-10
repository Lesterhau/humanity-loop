"use strict";
// Humanity Loop independent Ops Sentinel. No AI/provider credentials required.
const fs = require("node:fs");
const crypto = require("node:crypto");
const CHECKS = [
  ["CAP Daily Audit", "runtime/cap-daily-audit/latest.json", 40],
  ["Federal Policy Delta", "runtime/federal-policy-delta/latest-run.json", 40],
  ["Critical Guidance Delta", "runtime/critical-guidance-delta/latest-run.json", 12],
];
const WORKER = "runtime/ops/hourly-worker.json";
const GRACE_END = Date.parse("2026-10-11T09:00:00Z");
const ALERT_TITLE = "[Ops Sentinel] Humanity Loop needs maintenance attention";
const ROOT = "https://github.com/Lesterhau/humanity-loop";
function parseDate(v) {
  if (typeof v !== "string" || !(/Z$|[+-]\d\d:\d\d$/.test(v))) throw Error("missing timezone");
  const ms = Date.parse(v);
  if (!Number.isFinite(ms)) throw Error("invalid timestamp");
  return ms;
}
function readJSON(path) {
  return JSON.parse(fs.readFileSync(path, "utf8"));
}
function receiptCheck(name, path, limitHours, nowMs, read = readJSON) {
  const out = { name, path, status: "ok", detail: "" };
  try {
    const r = read(path);
    const age = (nowMs - parseDate(r.runAt)) / 3600000;
    if (age < -5 / 60) throw Error("future timestamp");
    if (age > limitHours) {
      out.status = "critical";
      out.detail = "No fresh receipt for " + age.toFixed(1) + " hours (limit " + limitHours + ")";
    } else if ((r.failuresCount || 0) > 0) {
      out.status = "warning";
      out.detail = "Latest run recorded " + r.failuresCount + " source failure(s)";
    } else if (path.includes("cap-daily") && (r.findingsCount !== r.findings.length)) {
      throw Error("CAP totals disagree");
    } else if (!path.includes("cap-daily") && (r.changesDetected !== r.changes.length)) {
      throw Error("Change totals disagree");
    } else {
      out.detail = "Receipt " + r.runAt + " (" + age.toFixed(1) + "h old)";
    }
  } catch (e) {
    out.status = "critical";
    out.detail = "Missing/invalid saved result (" + (e.code || e.message || "unknown") + ")";
  }
  return out;
}
function heartbeatCheck(nowMs, read = readJSON) {
  const out = { name: "ChatGPT hourly worker", path: WORKER, status: "ok", detail: "" };
  let r;
  try { r = read(WORKER); } catch (_) {
    out.status = nowMs < GRACE_END ? "info" : "warning";
    out.detail = "No verifiable heartbeat. This does not prove that the worker stopped.";
    return out;
  }
  try {
    if (r.schemaVersion !== 1 || !["worked", "no-op", "blocked"].includes(r.status)) throw Error("schema");
    const age = (nowMs - parseDate(r.runAt)) / 3600000;
    if (age < -5 / 60) throw Error("future time");
    if (age > 6) {
      out.status = "warning";
      out.detail = "Last reported activity " + age.toFixed(1) + "h ago; cannot verify current worker health.";
    } else {
      out.detail = "Heartbeat " + age.toFixed(1) + "h ago; does not independently prove productivity.";
    }
    if (r.lastVerifiedAt && (nowMs - parseDate(r.lastVerifiedAt)) > 30 * 3600000 && out.status === "ok") {
      out.status = "warning";
      out.detail = "No independently confirmed action reported by worker in over 30h.";
    }
    if (!r.lastVerifiedAt && nowMs > GRACE_END + 86400000 && out.status === "ok") {
      out.status = "warning";
      out.detail = "Worker reports activity but has supplied no independent success evidence.";
    }
  } catch (e) {
    out.status = "warning"; out.detail = "Invalid hourly-worker heartbeat; activity not verified.";
  }
  return out;
}
function evaluate(nowMs = Date.now(), read = readJSON) {
  const checks = CHECKS.map(v => receiptCheck(v[0], v[1], v[2], nowMs, read));
  checks.push(heartbeatCheck(nowMs, read));
  const status = checks.some(x => x.status === "critical") ? "critical" :
    checks.some(x => x.status === "warning") ? "warning" : "healthy";
  const signature = checks.map(x => [x.name, x.status]);
  const fingerprint = crypto.createHash("sha256").update(JSON.stringify(signature)).digest("hex").slice(0, 12);
  return {
    schemaVersion: 1, runAt: new Date(nowMs).toISOString(), status, fingerprint, checks,
    limitation: "Checks saved GitHub detector results and a worker self-report. Does NOT verify AppDeploy Foundry model execution.",
  };
}
function alertBody(r) {
  const broken = r.checks.filter(c => ["critical", "warning"].includes(c.status));
  const lines = [
    "## Something needs attention", "",
    "The independent checker found a late, missing, or inconsistent record. This does NOT prove the entire system stopped.", "",
    "## Specifically", "",
    ...broken.map(c => "- **" + c.name + "**: " + c.detail + " (" + c.path + ")"),
    "", "## What to do (no coding required)", "",
    "1. Open [GitHub Actions](" + ROOT + "/actions) and look for any red X beside the CAP, Federal, Critical, or Ops Sentinel runs.",
    "2. Open [the latest saved watchdog report](" + ROOT + "/blob/main/runtime/ops-sentinel/latest.json).",
    "3. If a worker heartbeat is missing, check the ChatGPT hourly worker's recent task runs. Do not assume it is dead from this warning alone.",
    "4. Ask a maintainer to examine the named failure and verify any repair before closing this issue.",
    "5. Do **not** automatically disable jobs, send emails, spend money, restart Foundry, or create a second worker.", "",
    "**Checked:** " + r.runAt, "",
    "**Coverage limit:** " + r.limitation, "",
    "<!-- sentinel:" + r.fingerprint + " -->",
  ];
  return lines.join("\n");
}
function persistReport(r, path = "runtime/ops-sentinel/latest.json") {
  let old;
  try { old = readJSON(path); } catch (_) { /* first run */ }
  if (old && old.runAt.slice(0, 10) === r.runAt.slice(0, 10) && old.fingerprint === r.fingerprint) return false;
  fs.mkdirSync(require("node:path").dirname(path), {recursive:true});
  fs.writeFileSync(path, JSON.stringify(r, null, 2) + "\n");
  return true;
}
module.exports = {CHECKS, WORKER, GRACE_END, ALERT_TITLE, receiptCheck, heartbeatCheck, evaluate, alertBody, persistReport};
