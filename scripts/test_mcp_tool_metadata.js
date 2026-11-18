'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const source = fs.readFileSync('mcp-server/app/api/mcp/route.ts','utf8');
const names = ['get_protocol','list_actions','get_action','list_live_projects','get_project','get_replication_prompt',
 'contributor_register','contributor_checkin','contributor_submit','contributor_set_status','search_dead_ends'];
const readTools = new Set(['get_protocol','list_actions','get_action','list_live_projects','get_project','get_replication_prompt','search_dead_ends']);
const blocks = {};
for(const part of source.split(/server\.registerTool\(/).slice(1)){
 const match=part.match(/^\s*"([a-z_]+)"/);
 if(match)blocks[match[1]]=part;
}
test('all eleven known public MCP tools must have truthful safety annotations',()=>{
 assert.deepEqual(Object.keys(blocks).sort(),names.slice().sort());
 for(const name of names){
  const part=blocks[name];
  assert.match(part,/annotations:\s*\{/);
  assert.match(part,new RegExp('readOnlyHint:\\s*'+(readTools.has(name)?'true':'false')+'\\b'));
  assert.match(part,new RegExp('destructiveHint:\\s*'+(name==='contributor_set_status'?'true':'false')+'\\b'));
  assert.match(part,new RegExp('idempotentHint:\\s*'+(readTools.has(name)?'true':'false')+'\\b'));
  assert.match(part,/openWorldHint:\s*false/);
 }
});
test('all 25 input parameters have agent-friendly metadata',()=>{
 assert.equal((source.match(/\.describe\(/g)||[]).length,25);
 const expected={list_actions:1,get_action:1,get_project:1,contributor_register:8,
  contributor_checkin:5,contributor_submit:6,contributor_set_status:2,search_dead_ends:1};
 for(const [name,n] of Object.entries(expected)){
  assert.equal((blocks[name].match(/\.describe\(/g)||[]).length,n,name+' description count');
 }
});
test('operations that modify the private ledger are not labeled read-only',()=>{
 for(const name of ['contributor_register','contributor_checkin','contributor_submit','contributor_set_status']){
  assert.match(blocks[name],/readOnlyHint:\s*false/);
  assert.match(blocks[name],/Writes? to Humanity Loop/);
 }
});
test('revoke is destructive and retention limitations remain explicit',()=>{
 assert.match(blocks.contributor_set_status,/destructiveHint:\s*true/);
 assert.match(blocks.contributor_set_status,/does not delete historical audit records/);
 assert.match(blocks.contributor_register,/Stage-0 rejects higher-risk permissions/);
});
