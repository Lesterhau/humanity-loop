"use strict";
/*
 * Trusted-base PR gate. NEVER checkout or run PR-authored code.
 * The only untrusted payload is fetched as JSON data from the PR head.
 */
const fs = require("node:fs");
const https = require("node:https");
const {validate} = require("./validate_case_steward_receipt");

const ALLOWED = "runtime/case-steward/latest.json";
const MAX_BYTES = 12 * 1024;

function ensure(ok, why) {
  if (!ok) throw new Error(why);
}

function verifyFiles(files) {
  ensure(Array.isArray(files), "PR files response must be an array");
  ensure(files.length === 1, "Case Steward PR may change exactly one file");
  const file = files[0];
  ensure(file && file.filename === ALLOWED, "PR changes a non-allowlisted path");
  ensure(file.status === "added" || file.status === "modified", "Receipt must be added or modified, not renamed or removed");
  ensure(Number.isInteger(file.changes) && file.changes <= 600, "Oversized or malformed PR patch");
  return true;
}

function parseContent(blob) {
  ensure(blob && blob.type === "file", "PR receipt is not a normal file");
  ensure(blob.encoding === "base64" && typeof blob.content === "string", "PR receipt is not base64 content");
  ensure(Number.isInteger(blob.size) && blob.size <= MAX_BYTES, "PR receipt exceeds size limit");
  const raw = Buffer.from(blob.content.replace(/\s+/g, ""), "base64");
  ensure(raw.length === blob.size, "Receipt encoding/length mismatch");
  ensure(raw.length <= MAX_BYTES, "Receipt exceeds limit");
  return JSON.parse(raw.toString("utf8"));
}

function verifyEvent(event, repo) {
  ensure(event && typeof event === "object" && event.pull_request, "Only a PR event is supported");
  const pr = event.pull_request;
  ensure(event.repository && event.repository.full_name === repo, "Repository identity mismatch");
  ensure(pr.base && pr.base.repo && pr.base.repo.full_name === repo, "PR base is not the canonical repository");
  ensure(Number.isInteger(pr.number) && pr.number > 0, "Invalid pull request number");
  ensure(pr.head && /^[a-f0-9]{40}$/.test(pr.head.sha || ""), "Invalid immutable PR head SHA");
  return {number:pr.number, headSha:pr.head.sha};
}

function ghGet(path,token){
  return new Promise((resolve,reject)=>{
    const req=https.get({
      hostname:"api.github.com",path,
      headers:{"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
        "X-GitHub-Api-Version":"2022-11-28","User-Agent":"HumanityLoop-CaseSteward-BaseGuard"}
    },res=>{
      let raw="";
      res.setEncoding("utf8");
      res.on("data",chunk=>{
        raw+=chunk;
        if(raw.length>200000){req.destroy(new Error("API response too large"));}
      });
      res.on("end",()=>{
        if(res.statusCode!==200)return reject(new Error("GitHub API HTTP "+res.statusCode));
        try {resolve(JSON.parse(raw));} catch(e){reject(e);}
      });
    });
    req.on("error",reject);
    req.setTimeout(20000,()=>req.destroy(new Error("GitHub API timed out")));
  });
}

async function inspect({event,repo,token,get=ghGet,nowMs=Date.now()}){
  ensure(typeof token === "string" && token.length>0, "Missing read-only GitHub token");
  ensure(/^[-\w.]+\/[-\w.]+$/.test(repo||""), "Invalid repository");
  const {number,headSha}=verifyEvent(event,repo);
  const prefix="/repos/"+repo;
  // Single changed-file constraint. Second page nonempty is automatic rejection.
  const files=await get(prefix+"/pulls/"+number+"/files?per_page=100&page=1",token);
  verifyFiles(files);
  const next=await get(prefix+"/pulls/"+number+"/files?per_page=100&page=2",token);
  ensure(Array.isArray(next) && next.length===0, "Extra PR files detected");
  // Read the PR content *as DATA*, while validator and this script come from
  // trusted BASE (checkout ref github.event.pull_request.base.sha).
  const blob=await get(prefix+"/contents/"+ALLOWED+"?ref="+headSha,token);
  const accepted=validate(parseContent(blob),nowMs);
  return {pr:number,headSha,checkedFile:ALLOWED,accepted,executedPrCode:false};
}
async function main(){
  try{
    const event=JSON.parse(fs.readFileSync(process.env.GITHUB_EVENT_PATH,"utf8"));
    const result=await inspect({event,repo:process.env.GITHUB_REPOSITORY,token:process.env.GITHUB_TOKEN});
    console.log(JSON.stringify({status:"safe-for-review",...result}));
  }catch(e){
    console.error("Case Steward PR REJECTED:",e.message);
    process.exitCode=1;
  }
}
if(require.main===module)main();
module.exports={ALLOWED,verifyFiles,parseContent,verifyEvent,inspect};
