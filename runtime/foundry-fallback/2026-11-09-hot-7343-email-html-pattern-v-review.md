# HOT Tasking Manager #7340 / draft PR #7343 — HTML pattern UnicodeSets regression review (2026-11-09 UTC)

## Mission and precise status
- External public-interest organization: Humanitarian OpenStreetMap Team, Tasking Manager.
- Reported defect: [#7340](https://github.com/hotosm/tasking-manager/issues/7340) — valid .berlin profile email rejected.
- Existing external fix proposal: [draft PR #7343](https://github.com/hotosm/tasking-manager/pull/7343), OPEN, draft, unmerged, head b15980c251598f7e5370427754500747da0a5a5d when read.
- This is a new, independently reproduced candidate regression in the existing PR, not an upstream patch or maintainer acceptance. Do not duplicate the existing PR.

## Primary-source evidence
1. [PR #7343 changed files and diff](https://github.com/hotosm/tasking-manager/pull/7343/files): frontend/src/utils/emailValidation.js introduces a JavaScript regex with unescaped hyphens in the two character classes [a-zA-Z0-9+_.-] and [a-zA-Z0-9-]; personalInformation.js sets an HTML email input pattern from EMAIL_INPUT_PATTERN = EMAIL_REGEX.source. Original form had an inline pattern with escaped hyphens and a {2,4} TLD limit.
2. [WHATWG HTML Standard, pattern attribute](https://html.spec.whatwg.org/multipage/input.html#the-pattern-attribute): browsers compile the HTML pattern using RegExpCreate(pattern, "v"); on a syntax error there is no compiled pattern (so no custom pattern-mismatch validation). This is separate from type=email built-in validation, which still applies.
3. [MDN HTML pattern reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/pattern): literal hyphens in character classes must be escaped under the v flag.
4. PR #7343 additionally changes openEditor.js and its tests for unrelated imagery issue #7228. The draft PR's SonarQube bot reported a failed maintainability quality gate on September 29; pre-commit.ci reports success at the checked head. A full current CI matrix was not independently inspected.

## Reproduction and minimal candidate
Source: exact regex literal from the PR head file frontend/src/utils/emailValidation.js, fetched by the connected GitHub repository reader. Tested in Node.js v22.16.0:
- EMAIL_REGEX.test("htm@klose.berlin") PASSES in default JavaScript regex mode (the PR's unit-test approach).
- new RegExp(EMAIL_REGEX.source, "v") FAILS with SyntaxError: Invalid character in character class. Thus the PR's tests can pass while the HTML pattern fails to compile in standards-conforming browsers.
- A narrow candidate escaping the two literal hyphens as backslash-hyphen compiles with v, accepts .berlin and .com, and rejects a string lacking @. These are isolated runtime checks, not full application or browser acceptance.
- [Runnable standalone regression tests](2026-11-09-hot-7343-email-html-pattern-v.test.cjs) encode the known PR failure as an expected throw and the candidate's basic success. Execute with: node --test runtime/foundry-fallback/2026-11-09-hot-7343-email-html-pattern-v.test.cjs. No external dependencies.

**Critical distinction:** This is not evidence of arbitrary malformed emails being accepted by the backend. If the custom HTML pattern fails to compile, the browser's built-in type=email syntax checks remain. The specific risk is loss of the intended custom validation and a misleadingly green JavaScript-only test suite.

## Attempted independent browser check / blocker
An ordinary headless Chromium local-file check was attempted, but local-file navigation returned net::ERR_BLOCKED_BY_ADMINISTRATOR. Stopped at the environment block; did not bypass the restriction or claim a browser result. The Node.js v-mode test and HTML standard are the independently available evidence. Browser-specific behavior and actual form submission remain unverified.

## Review verdict / eight-role single-model fallback
- Scout: relevant public-interest user-access bug already tracked upstream.
- Verifier: fetched exact PR head source and compared against normative HTML spec; confirmed syntax incompatibility in Node v mode.
- PM: do not duplicate or replace the existing upstream draft PR.
- Builder: created one standalone reproducible regression-test artifact in Humanity Loop's own public repository, not in HOT.
- 10th Man: removing pattern and relying on built-in type=email is an alternative, but changes intended validation; merely escaping two hyphens may preserve other pre-existing regex limitations. Test the whole form and review expected email acceptance policy.
- Safety: no live accounts, personal data, messages, upstream writes, deployed changes, AppDeploy/Foundry AI, or costs.
- Revision: recommend a small PR-head correction to escape literal hyphens in both character classes; add a new RegExp(EMAIL_INPUT_PATTERN, "v") assertion to regression tests and review whether unrelated imagery change should be separated.
- Outcome: review-only finding, not an accepted contribution or a fix for an affected mapper.

## Next unchecked step
A human reviewer or separately authorized upstream contributor should verify the v-mode failure in the actual profile form in Safari/Chrome, confirm the exact PR head is still current, run the frontend Jest/ESLint suite, then propose the narrow fix within existing PR #7343 rather than opening a duplicate. No external contact is authorized by this artifact.
