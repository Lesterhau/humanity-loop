"use strict";
const {test} = require("node:test");
const assert = require("node:assert/strict");
const s = require("./ops_sentinel");
const NOW = Date.parse("2026-10-12T15:00:00Z");
const fresh = new Date(NOW - 3600000).toISOString();
function fixture(overrides = {}) {
  const records = {};
  for (const [name, path] of s.CHECKS) {
    records[path] = path.includes("cap-daily") ?
      {runAt:fresh, findingsCount:0, findings:[]} :
      {runAt:fresh, changesDetected:0, changes:[], failuresCount:0};
  }
  records[s.WORKER] = {schemaVersion:1,runAt:fresh,status:"worked",lastVerifiedAt:fresh};
  return (p) => {
    if (Object.prototype.hasOwnProperty.call(overrides,p)) {
      if (overrides[p] === null) throw Error("missing file");
      return overrides[p];
    }
    if (!(p in records)) throw Error("missing");
    return records[p];
  };
}
test("all fresh checks healthy",() => assert.equal(s.evaluate(NOW,fixture()).status,"healthy"));
test("missing critical receipt alarms",() => assert.equal(s.evaluate(NOW,fixture({[s.CHECKS[2][1]]:null})).status,"critical"));
test("stale CAP alarms",() => assert.equal(s.evaluate(NOW,fixture({[s.CHECKS[0][1]]:{runAt:new Date(NOW - 42*3600000).toISOString(),findingsCount:0,findings:[]}})).status,"critical"));
test("federal source failure is warning",() => assert.equal(s.evaluate(NOW,fixture({[s.CHECKS[1][1]]:{runAt:fresh,changesDetected:0,changes:[],failuresCount:1}})).status,"warning"));
test("incoherent CAP counts are critical",() => assert.equal(s.evaluate(NOW,fixture({[s.CHECKS[0][1]]:{runAt:fresh,findingsCount:2,findings:[]}})).status,"critical"));
test("future receipt is critical",() => assert.equal(s.evaluate(NOW,fixture({[s.CHECKS[0][1]]:{runAt:new Date(NOW+3600000).toISOString(),findingsCount:0,findings:[]}})).status,"critical"));
test("worker not present warns after grace",() => assert.equal(s.evaluate(NOW,fixture({[s.WORKER]:null})).status,"warning"));
test("worker not present is informational before grace",() => {
  const before = Date.parse("2026-10-10T15:00:00Z");
  assert.equal(s.heartbeatCheck(before,fixture({[s.WORKER]:null})).status,"info");
});
test("late worker heartbeat warns",() => assert.equal(s.evaluate(NOW,fixture({[s.WORKER]:{schemaVersion:1,runAt:new Date(NOW-8*3600000).toISOString(),status:"worked"}})).status,"warning"));
test("late verified action warns despite fresh heartbeat",() => assert.equal(s.evaluate(NOW,fixture({[s.WORKER]:{schemaVersion:1,runAt:fresh,status:"worked",lastVerifiedAt:new Date(NOW-31*3600000).toISOString()}})).status,"warning"));
test("alert instructions are plain language, never auto-escalation",() => {
  const r=s.evaluate(NOW,fixture({[s.CHECKS[0][1]]:null}));
  const text=s.alertBody(r);
  assert.match(text,/Do not automatically disable jobs/i);
  assert.match(text,/CAP Daily Audit/);
  assert.match(text,/sentinel:/);
});
test("stable alert fingerprint across elapsed hours",()=>{
  const a=s.evaluate(NOW,fixture({[s.WORKER]:null}));
  const b=s.evaluate(NOW+3600000,fixture({[s.WORKER]:null}));
  assert.equal(a.fingerprint,b.fingerprint);
});
