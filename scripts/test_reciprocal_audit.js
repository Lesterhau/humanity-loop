'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const a=require('./reciprocal_audit');
const now=new Date('2026-10-22T23:00:00Z');
const fixture={
 prompt:'Case Steward; claim timestamps, not verified completed scans. Last verified native jobs disabled.',
 state:'Foundry is offline',governance:'Tier 0, Tier 1 and Tier 2',workflow:'schedule:\n - cron: 41',
 scout:'The timestamps are claims, not verified finished research.'
};
test('first, overdue, bad/future receipt runs; early repeat does not',()=>{
 assert.equal(a.due(null,now.getTime()),true);
 assert.equal(a.due({runAt:'2026-10-21T00:00:00Z'},now.getTime()),false);
 assert.equal(a.due({runAt:'2026-10-10T00:00:00Z'},now.getTime()),true);
 assert.equal(a.due({runAt:'bad'},now.getTime()),true);
 assert.equal(a.due({runAt:'2026-11-10T00:00:00Z'},now.getTime()),true);
});
test('healthy docs yield explicit no-op, not manufactured change',()=>{
 const r=a.evaluate(fixture,now);
 assert.equal(r.status,'checks-passed');
 assert.equal(r.selectedAction,null);
 assert.equal(r.findings.length,0);
 assert.match(r.boundary,/No private Morrow/);
});
test('contradictory native cron assertion is detected and not silently fixed',()=>{
 const r=a.evaluate({...fixture,prompt:fixture.prompt+' native AppDeploy CAP cron is ALSO enabled'},now);
 assert.equal(r.selectedAction.id,'contradictory-native-cron-docs');
 assert.equal(r.selectedAction.status,'not-executed');
});
test('Scout claim timestamp is not equivalent to completed research',()=>{
 const r=a.evaluate({...fixture,scout:'Each claim completes a scan'},now);
 assert.equal(r.findings[0].id,'scout-claim-not-completion');
});
test('case-delegation omission is actionable rather than new bot spawning',()=>{
 const r=a.evaluate({...fixture,prompt:fixture.prompt.replace('Case Steward; ','')},now);
 assert.equal(r.findings[0].id,'case-delegation-absent');
});
test('only fixed local Humanity Loop files; readback and 7-day dedup',()=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'hl-reciprocal-'));
 const files={'AUTOMATION-PROMPT.md':fixture.prompt,'PROJECT-STATE.md':fixture.state,
  'GOVERNANCE.md':fixture.governance,'.github/workflows/ops-sentinel.yml':fixture.workflow,'SCOUT-MESH.md':fixture.scout};
 try{
  for(const [p,v] of Object.entries(files)){const f=path.join(root,p);fs.mkdirSync(path.dirname(f),{recursive:true});fs.writeFileSync(f,v);}
  const first=a.main(now,root),again=a.main(new Date(now.getTime()+3600000),root);
  assert.equal(first.ran,true);assert.equal(again.ran,false);
  const r=JSON.parse(fs.readFileSync(path.join(root,a.RECEIPT),'utf8'));
  assert.equal(r.status,'checks-passed');
  assert.equal(r.methodSource,'Owner-approved general principles; no private implementation transplanted');
  assert.ok(!fs.existsSync(path.join(root,'morrow-engine')));
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
