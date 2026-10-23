"use strict";
// A minimal public-only Case Steward receipt validator. An approved PR + human
// review is still required; this is not a confidentiality or truth guarantee.
const fs = require("node:fs");
const VALID = new Set(["no-op", "reviewed", "blocked", "impact_candidate", "approval_required"]);
const CREDIT = new Set(["pending", "flagged_then_corrected", "plausible_contributor", "confirmed_contributor"]);
function assert(ok, why) { if (!ok) throw Error(why); }
function date(s, name) {
  assert(typeof s === "string" && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(s) &&
    Number.isFinite(Date.parse(s)), name+" must be an ISO UTC timestamp");
}
function url(u, name) {
  assert(typeof u === "string" && u.length < 700 && /^https:\/\/[^ @\s/#?]+(?:[/?#][^\s]*)?$/i.test(u),
    name+" must be a public https URL");
  assert(!/@/.test(u), name+" must not contain credentials/email addresses");
}
function shortText(s, name, max = 1100) {
  assert(typeof s === "string" && s.trim().length && s.length <= max, name+" empty or too long");
  assert(!/[\r\n]/.test(s), name+" must be one line, not raw correspondence");
  assert(!/[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/.test(s), name+" has an email address; do not publish");
  assert(!/(?:sk-[A-Za-z0-9_-]{15,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9_.-]{20,})/i.test(s),
    name+" resembles a secret");
}
function validate(d, nowMs = Date.now()) {
  assert(d && typeof d === "object" && !Array.isArray(d), "object required");
  const allowed = ["schemaVersion","producer","runId","runAt","status","caseId","finding",
    "nextAction","nextReviewAt","evidence","creditLevel","impactRationale","noWriteClaim"];
  assert(Object.keys(d).every(k=>allowed.includes(k)), "unapproved field: possible private content");
  assert(d.schemaVersion === 1, "schemaVersion=1 required");
  assert(d.producer === "Claude Case Steward", "wrong producer");
  shortText(d.runId, "runId", 150);
  date(d.runAt, "runAt");
  assert(Date.parse(d.runAt) <= nowMs + 5 * 60 * 1000, "future run time");
  assert(VALID.has(d.status), "unknown status");
  assert(d.caseId === null || (typeof d.caseId === "string" && /^OT-\d{3}$/.test(d.caseId)), "invalid case ID");
  assert(d.caseId !== null || d.status === "no-op", "case required unless no-op");
  shortText(d.finding, "finding");
  shortText(d.nextAction, "nextAction");
  assert(d.nextReviewAt === null || d.nextReviewAt === undefined || typeof d.nextReviewAt === "string", "nextReviewAt type");
  if (d.nextReviewAt) date(d.nextReviewAt, "nextReviewAt");
  assert(Array.isArray(d.evidence) && d.evidence.length <= 8, "evidence must be an array <= 8");
  for (const [i,e] of d.evidence.entries()) {
    assert(e && typeof e === "object" && Object.keys(e).sort().join(",") === "checkedAt,url", "unexpected evidence properties");
    url(e.url, "evidence["+i+"].url");
    date(e.checkedAt, "evidence["+i+"].checkedAt");
  }
  assert(CREDIT.has(d.creditLevel), "unknown credit level");
  assert(d.noWriteClaim === true, "untrusted receipt must not claim it was accepted or acted on");
  if (d.status === "impact_candidate") {
    assert(d.evidence.length >= 2, "impact requires independent before/after source references");
    shortText(d.impactRationale, "impactRationale");
    assert(d.creditLevel !== "pending", "impact requires documented credit level");
  } else assert(d.impactRationale === null, "impact rationale only for impact candidates");
  return {acceptedForReview:true,caseId:d.caseId,status:d.status};
}
if (require.main === module) {
  try {
    const p=process.argv[2] || "runtime/case-steward/latest.json";
    console.log(JSON.stringify(validate(JSON.parse(fs.readFileSync(p,"utf8")))));
  } catch(e) {
    console.error("Case Steward receipt NOT accepted for review:",e.message);
    process.exitCode=1;
  }
}
module.exports={validate};
