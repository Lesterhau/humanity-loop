'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {scan,body,WATCH}=require('./contributor_intake_sla');
const NOW=Date.parse('2026-11-17T18:00:00Z');
const comment=(id,login,time,text='')=>({id,user:{login},created_at:time,body:text});
const issue=(number,comments,state='open')=>({number,comments,state});
test('only three existing contributor issues are watched',()=>assert.deepEqual(WATCH,[29,33,34]));
test('external offer older than two hours alerts with public metadata only',()=>{
  const p=scan([issue(33,[comment(6778587287,'VibeMirror-coder','2026-11-10T18:00:00Z','sensitive body')])],NOW);
  assert.equal(p.length,1);assert.equal(p[0].id,6778587287);assert.ok(!JSON.stringify(p).includes('sensitive'));
  assert.ok(!body(p,new Date(NOW).toISOString()).includes('sensitive'));
});
test('unrelated owner update does not suppress outside offer',()=>{
  const p=scan([issue(33,[comment(1,'outside','2026-11-15T10:00:00Z'),comment(2,'Lesterhau','2026-11-16T10:00:00Z','Routine status')])],NOW);
  assert.equal(p.length,1);
});
test('owner comment with original permalink suppresses after direct response',()=>{
  const p=scan([issue(33,[comment(6778587287,'VibeMirror-coder','2026-11-10T18:00:00Z'),comment(6956658972,'Lesterhau','2026-11-17T12:00:00Z','Thanks for #issuecomment-6778587287; here is your response')])],NOW);
  assert.deepEqual(p,[]);
});
test('fresh, old, owner, bot, and closed issue comments not alerted',()=>{
  const p=scan([issue(29,[comment(1,'outside','2026-11-17T17:30:00Z')]),issue(33,[comment(2,'github-actions[bot]','2026-11-15T11:00:00Z'),comment(3,'Lesterhau','2026-11-15T11:00:00Z'),comment(4,'other','2026-10-01T11:00:00Z')]),issue(34,[comment(5,'outside','2026-11-16T10:00:00Z')],'closed')],NOW);
  assert.deepEqual(p,[]);
});
test('alerts do not imply permission to message or accept volunteer',()=>{
  const msg=body([{issue:33,id:101,ageHours:9,url:'https://github.com/Lesterhau/humanity-loop/issues/33#issuecomment-101'}],'2026-11-17T18:00:00Z');
  assert.match(msg,/NOT verified consent/);assert.match(msg,/No automated reply/);assert.match(msg,/\n/);
});
