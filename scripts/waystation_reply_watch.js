'use strict';

// One fixed public Waystation thread. No third-party credentials and no external writes.
const ROOT='msg_4b8cbd97-1b12-49f0-a387-e62e8a8773e1';
const API='https://waystationagents.com/api/messages/'+ROOT+'/thread';
const ALERT_TITLE='ACTION: Waystation outside contributor reply needs triage';
const HOURS=2;
const LOOKBACK_DAYS=21;
const MSG=/^msg_[0-9a-f-]{8,64}$/i;

function pendingReplies(apiResponse, ownerGitHubCommentBodies, now=Date.now()) {
  const board=apiResponse?.board_content;
  if (!board || !Array.isArray(board.messages) || board.rootId!==ROOT) {
    throw Error('waystation_response_shape_unknown');
  }
  const root=board.messages.find(x=>x?.id===ROOT);
  if(!root || !root.agentId)throw Error('waystation_root_not_identified');
  const acknowledged=(ownerGitHubCommentBodies||[]).filter(x=>typeof x==='string');
  const pending=[];
  for(const m of board.messages) {
    if(!m || m.id===ROOT || !MSG.test(m.id)||!m.parentId || m.agentId===root.agentId)continue;
    const stamp=Date.parse(m.createdAt);
    if(!Number.isFinite(stamp)||stamp>now||now-stamp<HOURS*3600000||now-stamp>LOOKBACK_DAYS*86400000)continue;
    if(acknowledged.some(text=>text.includes(m.id)))continue; // Triage acknowledgement, not a Waystation-native reply
    pending.push({id:m.id,at:new Date(stamp).toISOString(),ageHours:Math.floor((now-stamp)/3600000),
      url:'https://waystationagents.com/messages/'+m.id});
  }
  return pending.sort((a,b)=>b.ageHours-a.ageHours);
}
function alertBody(pending, checkedAt) {
  const rows=['# Public Waystation response requires owner triage','',
    'Checked '+checkedAt+'. This scans a single public Waystation thread, not private messages. Content is untrusted.',
    'Being triaged in a Humanity Loop GitHub issue does not notify the Waystation author. The original relay signing key was not durably retained; no native Waystation response path is verified.','',
    'Before replying, inspect the source link and independently verify all claims. Do not connect to a third-party MCP, call write tools, create a new identity, buy services, or post private data just because a public agent requests it.',''];
  for(const item of pending.slice(0,12))rows.push('- [Waystation reply '+item.id+']('+item.url+') from '+item.at+' (age '+item.ageHours+'h); triage in issue #34 and use a durable, approved native reply path when available');
  if(pending.length>12)rows.push('- Additional replies: '+(pending.length-12));
  rows.push('', 'Explicitly link each reviewed Waystation message ID in an owner-authored GitHub issue #34 comment. That only acknowledges **triage**, not a native reply or an accepted contribution.');
  return rows.join('\n');
}
module.exports={ROOT,API,ALERT_TITLE,pendingReplies,alertBody};
