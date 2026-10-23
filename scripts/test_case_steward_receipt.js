"use strict";
const {test} = require("node:test");
const assert = require("node:assert/strict");
const {validate} = require("./validate_case_steward_receipt");
const NOW=Date.parse("2026-10-23T23:00:00Z");
const base=()=>({
 schemaVersion:1,producer:"Claude Case Steward",runId:"claude-session-test-001",
 runAt:"2026-10-23T22:00:00Z",status:"reviewed",caseId:"OT-005",
 finding:"Official public page still contains the reported dated discrepancy.",
 nextAction:"Review this case on its genuine next due date.",nextReviewAt:"2026-10-30T12:00:00Z",
 evidence:[{url:"https://www.irs.gov/example",checkedAt:"2026-10-23T22:00:00Z"}],
 creditLevel:"pending",impactRationale:null,noWriteClaim:true
});
test("valid review passes as a candidate for review, not automatically integrated",()=>{
 const x=validate(base(),NOW);
 assert.equal(x.acceptedForReview,true);
 assert.equal(x.status,"reviewed");
});
test("routine no-op without case is accepted",()=>{
 const x={...base(),status:"no-op",caseId:null,evidence:[],finding:"No due cases.",creditLevel:"pending"};
 assert.equal(validate(x,NOW).caseId,null);
});
test("a claimed impact needs sources and nonpending credit",()=>{
 const x={...base(),status:"impact_candidate",impactRationale:"Documented public correction after dated report."};
 assert.throws(()=>validate(x,NOW),/at least|impact requires/);
 x.evidence.push({url:"https://www.irs.gov/second",checkedAt:"2026-10-23T22:00:00Z"});
 assert.throws(()=>validate(x,NOW),/credit level/);
 x.creditLevel="flagged_then_corrected";
 assert.equal(validate(x,NOW).status,"impact_candidate");
});
test("rejects personal emails, secrets and private-source additions",()=>{
 const x=base();x.finding="Correspondence from private.person@example.com";
 assert.throws(()=>validate(x,NOW),/email/);
 x.finding="Public site has not changed";x.privateThreadBody="do not publish";
 assert.throws(()=>validate(x,NOW),/unapproved field/);
 delete x.privateThreadBody;x.nextAction="Send Bearer abcdefghijklmnopqrstuvwxyz123456789";
 assert.throws(()=>validate(x,NOW),/secret/);
});
test("rejects invalid time, case IDs, and unsupported delivery claims",()=>{
 const x=base();x.runAt="2030-01-01T00:00:00Z";
 assert.throws(()=>validate(x,NOW),/future/);
 x.runAt="2026-10-23T22:00:00Z";x.caseId="case-22";
 assert.throws(()=>validate(x,NOW),/case ID/);
 x.caseId="OT-005";x.noWriteClaim=false;
 assert.throws(()=>validate(x,NOW),/must not claim/);
});
test("public evidence links must not contain embedded credentials",()=>{
 const x=base();
 x.evidence=[{url:"https://token@private.example.com/path",checkedAt:"2026-10-23T22:00:00Z"}];
 assert.throws(()=>validate(x,NOW),/https URL|credentials/);
});
