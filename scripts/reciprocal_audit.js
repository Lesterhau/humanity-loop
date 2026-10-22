'use strict';
// PUBLIC Humanity Loop repo only. No read/clone/fetch/auth to private Morrow.
const fs=require('node:fs');
const path=require('node:path');
const RECEIPT='runtime/reciprocal-audit/latest.json';
const SEVEN_DAYS=7*24*60*60*1000;
const METHODS=Object.freeze([
 {id:'bounded-experiment',description:'Prefer low-risk reversible improvements with tests'},
 {id:'failure-recovery',description:'Record failures and retry only when conditions change'},
 {id:'evidence-honesty',description:'Distinguish technical progress from verified public benefit'},
 {id:'continuity',description:'Persist operating instructions, tests and real receipts'},
 {id:'privacy-boundary',description:'Never transfer private commercial material to a public repo'}
]);
function safeRead(file,root='.') { return fs.readFileSync(path.join(root,file),'utf8'); }
function due(last,nowMs) {
 if(!last||typeof last.runAt!=='string')return true;
 const t=Date.parse(last.runAt);
 if(!Number.isFinite(t)||t>nowMs+5*60*1000)return true;
 return nowMs-t>=SEVEN_DAYS;
}
function evaluate(files,now=new Date()) {
 const prompt=files.prompt||'',state=files.state||'',gov=files.governance||'',workflow=files.workflow||'',scout=files.scout||'';
 const findings=[];
 function add(id,evidence,action){findings.push({id,severity:'review',evidence,action});}
 const stale=[
  'native AppDeploy CAP cron is ALSO enabled',
  'native cron is enabled',
  'native AppDeploy Critical Guidance cron is enabled'
 ].filter(s=>prompt.includes(s));
 if(stale.length)add('contradictory-native-cron-docs',
   stale.length+' unqualified enabled-claims conflict with the canonical October 20 credits-exhausted incident',
   'Verify current app status; then change the outdated assertion. Never restart a cron just to make docs true.');
 if(!prompt.includes('claim timestamps, not verified completed scans')||
    !scout.includes('claims, not verified finished research'))
   add('scout-claim-not-completion','Scout documentation may conflate a claim with completed research',
     'Repair documentation and completion acceptance tests; do not manufacture live Scout timestamps.');
 if(!prompt.includes('Case Steward'))
   add('case-delegation-absent','No named Case Steward lane detected in the canonical operating prompt',
     'Define one bounded due-date-driven case owner; do not imply an independent Claude scheduler exists.');
 if(!state.includes('Foundry')||!gov.includes('Tier')||!workflow.includes('schedule:'))
   add('missing-operational-guard','Could not verify one or more public-repository process safeguards',
     'Inspect the missing guard and test a narrow fix without deploying unsafe workloads.');
 const first=findings[0];
 return {
  schemaVersion:1,runAt:now.toISOString(),status:first?'action-proposed':'checks-passed',
  boundary:'Only the public Humanity Loop repository was read. No private Morrow files, APIs, tokens or business intelligence accessed.',
  methodSource:'Owner-approved general principles; no private implementation transplanted',
  methods:METHODS.map(x=>x.id),checksPerformed:5,findings,
  selectedAction:first?{id:first.id,scope:'Humanity Loop only',risk:'bounded internal review',status:'not-executed',next:first.action}:null,
  evidenceLimit:'A local process scan is not proof of two-way model learning, an executed repair or real-world public benefit.'
 };
}
function main(now=new Date(),root='.') {
 const p=path.join(root,RECEIPT);let prev;
 try{prev=JSON.parse(fs.readFileSync(p,'utf8'));}catch(_){prev=null;}
 if(!due(prev,now.getTime())){console.log('Cross-audit already completed within seven days; no new receipt.');return {ran:false,receipt:prev};}
 // Fixed, local PUBLIC Humanity Loop file allowlist. No arbitrary paths or private-repo source.
 const files={
  prompt:safeRead('AUTOMATION-PROMPT.md',root),
  state:safeRead('PROJECT-STATE.md',root),
  governance:safeRead('GOVERNANCE.md',root),
  workflow:safeRead('.github/workflows/ops-sentinel.yml',root),
  scout:safeRead('SCOUT-MESH.md',root)
 };
 const report=evaluate(files,now);
 fs.mkdirSync(path.dirname(p),{recursive:true});
 fs.writeFileSync(p,JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({status:report.status,findings:report.findings.length,scope:'public-only',runAt:report.runAt}));
 return {ran:true,receipt:report};
}
if(require.main===module){
 if(!process.argv.includes('--if-due')){console.error('Use --if-due for bounded operation.');process.exitCode=2;}
 else main();
}
module.exports={RECEIPT,SEVEN_DAYS,METHODS,due,evaluate,main};
