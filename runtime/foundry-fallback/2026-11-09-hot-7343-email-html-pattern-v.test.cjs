// Review-only reproduction of HOT Tasking Manager PR #7343 at head b15980c.
// This is NOT an upstream patch, browser acceptance test, or production code.
// Run: node --test 2026-11-09-hot-7343-email-html-pattern-v.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');

// Exact EMAIL_REGEX expression from PR #7343, frontend/src/utils/emailValidation.js.
const proposed = /^([a-zA-Z0-9+_.-]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9-]+\.)+))([a-zA-Z]{2,}|[0-9]{1,3})(\]?)$/;

// Narrow candidate: escape literal '-' in BOTH character classes.
// This does not resolve other pre-existing email-format limitations.
const candidate = /^([a-zA-Z0-9+_.\-]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,}|[0-9]{1,3})(\]?)$/;

test('PR JavaScript regex accepts the reported .berlin address', () => {
  assert.equal(proposed.test('htm@klose.berlin'), true);
});
test('PR pattern source FAILS HTML required UnicodeSets/v compilation', () => {
  assert.throws(() => new RegExp(proposed.source, 'v'), SyntaxError);
});
test('escaped-hyphen candidate compiles as HTML pattern /v', () => {
  assert.doesNotThrow(() => new RegExp(candidate.source, 'v'));
});
test('candidate accepts .berlin and .com', () => {
  const htmlPattern = new RegExp(candidate.source, 'v');
  assert.equal(htmlPattern.test('htm@klose.berlin'), true);
  assert.equal(htmlPattern.test('user@example.com'), true);
});
test('candidate rejects a missing @ sign', () => {
  assert.equal(new RegExp(candidate.source, 'v').test('not-an-email'), false);
});
