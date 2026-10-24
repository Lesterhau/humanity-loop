"use strict";
const {test}=require("node:test");
const assert=require("node:assert/strict");
const g=require("./check_case_steward_pr");
const BASE="Lesterhau/humanity-loop";
const SHA="1".repeat(40);
const NOW=Date.parse("2026-10-24T12:00:00Z");
const payload=()=>({
 schemaVersion:1,producer:"Claude Case Steward",runId:"synthetic-pr-validation-test",
 runAt:"2026-10-24T11:00:00Z",status:"reviewed",caseId:"OT-006",
 finding:"Synthetic test only; no factual outcome is asserted.",
 nextAction:"Continue review after real evidence is collected.",
 nextReviewAt:"2026-10-31T11:00:00Z",evidence:[],
 creditLevel:"pending",impactRationale:null,noWriteClaim:true
});
const file=(name=g.ALLOWED,status="modified")=>({filename:name,status,changes:15});
const event=()=>({
 repository:{full_name:BASE},
 pull_request:{number:37,base:{repo:{full_name:BASE}},head:{sha:SHA}}
});
const data=(p=payload())=>{
 const buf=Buffer.from(JSON.stringify(p));
 return {type:"file",encoding:"base64",size:buf.length,content:buf.toString("base64")};
};
function client({files=[file()],other=[],body=data()}={}){
 return async path=>{
  if(path.includes("/files?")&&/[?&]page=1(?:&|$)/.test(path))return files;
  if(path.includes("/files?")&&/[?&]page=2(?:&|$)/.test(path))return other;
  if(path.includes("/contents/"))return body;
  throw Error("Unexpected untrusted URL");
 };
}
const check=async params=>g.inspect({event:event(),repo:BASE,token:"test-token",get:client(params),nowMs:NOW});

test("accepts a strictly single-file synthetic receipt using trusted-base validator",async()=>{
 const r=await check();
 assert.equal(r.accepted.acceptedForReview,true);
 assert.equal(r.executedPrCode,false);
 assert.equal(r.checkedFile,g.ALLOWED);
});

test("rejects any edits to the validator, tests, or workflow even alongside valid JSON",async()=>{
 for(const forbidden of ["scripts/validate_case_steward_receipt.js",
  "scripts/test_case_steward_receipt.js",".github/workflows/case-steward-receipt-guard.yml",
  "AUTOMATION-PROMPT.md"]){
  await assert.rejects(check({files:[file(),file(forbidden)]}),/exactly one file/);
  await assert.rejects(check({files:[file(forbidden)]}),/non-allowlisted/);
 }
});

test("rejects hidden second page and receipt rename/delete",async()=>{
 await assert.rejects(check({other:[file("README.md")]}),/Extra PR files/);
 await assert.rejects(check({files:[file(g.ALLOWED,"removed")]}),/added or modified/);
 await assert.rejects(check({files:[file(g.ALLOWED,"renamed")]}),/added or modified/);
});

test("rejects wrong PR base, invalid head SHA, or mismatched repository",async()=>{
 const e=event();
 e.pull_request.base.repo.full_name="another/repository";
 assert.throws(()=>g.verifyEvent(e,BASE),/base/);
 e.pull_request.base.repo.full_name=BASE;
 e.pull_request.head.sha="not-a-real-sha";
 assert.throws(()=>g.verifyEvent(e,BASE),/SHA/);
 e.pull_request.head.sha=SHA;
 e.repository.full_name="another/repository";
 assert.throws(()=>g.verifyEvent(e,BASE),/identity/);
});

test("rejects mismatched, oversized, or non-base64 PR content",async()=>{
 await assert.rejects(check({body:{...data(),size:999}}),/length mismatch/);
 await assert.rejects(check({body:{...data(),size:15000}}),/exceeds/);
 await assert.rejects(check({body:{...data(),encoding:"none"}}),/base64/);
});

test("rejects untrusted extra fields and false impact claims",async()=>{
 const unsafe={...payload(),personalCorrespondence:"Private email contents"};
 await assert.rejects(check({body:data(unsafe)}),/unapproved field/);
 const falseWin={...payload(),status:"impact_candidate",creditLevel:"confirmed_contributor",
 impactRationale:"We fixed everything",evidence:[]};
 await assert.rejects(check({body:data(falseWin)}),/independent before\/after source references/);
});

test("rejects missing token, wrong head content, oversized patch",async()=>{
 await assert.rejects(g.inspect({event:event(),repo:BASE,token:"",get:client(),nowMs:NOW}),/Missing/);
 await assert.rejects(check({files:[{...file(),changes:1000}]}),/Oversized/);
 await assert.rejects(check({body:{...data(),type:"dir"}}),/normal file/);
});
