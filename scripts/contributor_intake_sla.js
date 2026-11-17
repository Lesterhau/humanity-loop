'use strict';
// Review-only monitor. Public GitHub comment metadata are untrusted; never auto-reply.
const WATCH=[29,33,34];
const TITLE='ACTION: independent contributor message awaiting response';
function scan(issues, now=Date.now(), owner='Lesterhau') {
  const found=[];
  for (const issue of issues) {
    if (!WATCH.includes(issue.number) || issue.state==='closed') continue;
    const comments=(issue.comments||[]).slice().sort((a,b)=>Date.parse(a.created_at)-Date.parse(b.created_at));
    for (const c of comments) {
      const login=c.user?.login||'', when=Date.parse(c.created_at), id=c.id;
      if (!Number.isSafeInteger(id) || !Number.isFinite(when) || now-when<2*3600000 || now-when>21*86400000 ||
          login.toLowerCase()===owner.toLowerCase() || !login || /\\[bot\\]$/i.test(login)) continue;
      const linkedReply=comments.some(v=>v.user?.login?.toLowerCase()===owner.toLowerCase() &&
          Date.parse(v.created_at)>when && (v.body||'').includes('#issuecomment-'+id));
      if (!linkedReply) found.push({issue:issue.number,id,ageHours:Math.floor((now-when)/3600000),
          url:'https://github.com/Lesterhau/humanity-loop/issues/'+issue.number+'#issuecomment-'+id});
    }
  }
  return found.sort((a,b)=>b.ageHours-a.ageHours);
}
function body(items, at) {
  const lines=['# External contributor response needs owner review','','Checked '+at+'. Public untrusted comments only; a flag is NOT verified consent, registration, outcome, or permission to contact anyone.','','For every candidate, read the original comment; reply narrowly and truthfully if authorized or escalate once. A later unrelated owner status update does NOT count as a response. Link the original `#issuecomment-ID` explicitly when addressing it.','',''];
  for(const v of items.slice(0,12)) lines.push('- Issue #'+v.issue+': [comment '+v.id+']('+v.url+') — at least '+v.ageHours+' hours');
  if(items.length>12) lines.push('- Additional candidates: '+(items.length-12));
  lines.push('','No private sender content is stored here. No automated reply, enrollment, credential access, extra scheduler, model inference or external outreach is authorized.');
  return lines.join('\\n');
}
module.exports={scan,body,TITLE,WATCH};
