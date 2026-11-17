'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const join=fs.readFileSync('mcp-server/app/join/page.tsx','utf8');
const privacy=fs.readFileSync('PRIVACY.md','utf8');
test('privacy limits visible in register stage before create button',()=>{
 const register=join.slice(join.indexOf('phase === "register"'),join.indexOf('phase === "complete"'));
 assert.ok(register.includes('Before you register: what is stored.'));
 assert.ok(register.indexOf('Before you register: what is stored.')<register.indexOf('Create my test pass'));
 assert.match(register,/No fixed deletion period is currently/);
});
test('outside research and private ledger writes distinguished in user copy',()=>{
 assert.match(join,/assigned research must be read-only on external public/);
 assert.match(join,/do write records to Humanity Loop/);
 assert.match(join,/check-ins and submissions write to Humanity Loop/);
});
test('register-free participation and privacy policy are visible before registration',()=>{
 const register=join.slice(join.indexOf('phase === "register"'),join.indexOf('phase === "complete"'));
 assert.match(register,/humanity-loop\/issues\/29/);
 assert.match(register,/PRIVACY\.md/);
});
test('privacy policy contains no false erasure guarantee',()=>{
 assert.match(privacy,/has not yet implemented or verified a fixed deletion/);
 assert.match(privacy,/Revocation blocks use/);
 assert.match(privacy,/does not promise deletion/);
});
