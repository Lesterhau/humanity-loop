'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const s=fs.readFileSync('FIRST-INDEPENDENT-BETA.md','utf8');

test('beta guide never treats an expired example as a guaranteed assignment',()=>{
 assert.match(s,/Texas WIC.*expired \*\*November 6, 2026\*\*/s);
 assert.match(s,/Do only the Tier-0 task actually assigned by the live tool/);
 assert.match(s,/report `idle`/);
 assert.doesNotMatch(s,/intended first useful task is the \[Texas WIC/);
});

test('consent, retention and safe one-off work remain explicit',()=>{
 assert.match(s,/Revocation is not deletion/);
 assert.match(s,/no verified fixed retention or full-erasure deadline/);
 assert.match(s,/no-registration issue #29/);
 assert.match(s,/independently validate|separate review/);
 assert.match(s,/Do \*\*not\*\* schedule/);
});

test('no invented permanent availability or impact from extension',()=>{
 assert.match(s,/December 5, 2026/);
 assert.match(s,/This dated inventory is informational and must not be treated as real-time availability/);
 assert.match(s,/zero node submissions/);
});
