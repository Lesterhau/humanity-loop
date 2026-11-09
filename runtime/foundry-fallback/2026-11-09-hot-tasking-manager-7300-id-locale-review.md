# Humanity Loop — HOT Tasking Manager #7300 iD Dutch locale candidate
Date: 2026-11-09 UTC. Status: **review-only candidate; no upstream submission, production deployment or accepted fix**.

## External public-interest problem and source
- HOT Tasking Manager's [open issue #7300](https://github.com/hotosm/tasking-manager/issues/7300) reports Dutch iD editor showing `Missing en translation:` rather than Dutch or English fallback. This is a volunteer humanitarian-mapping usability problem, not evidence that mapping data were lost.
- At HOT's observed default-branch source revision `cbf2ec89c38bf876bbc4de048f782978247ecfd9`, [internationalization.js](https://github.com/hotosm/tasking-manager/blob/cbf2ec89c38bf876bbc4de048f782978247ecfd9/frontend/src/utils/internationalization.js) advertises `nl_NL` and [editor.js](https://github.com/hotosm/tasking-manager/blob/cbf2ec89c38bf876bbc4de048f782978247ecfd9/frontend/src/components/editor.js) passes that value directly to iD's `.locale(locale)`; [sandboxEditor.js](https://github.com/hotosm/tasking-manager/blob/cbf2ec89c38bf876bbc4de048f782978247ecfd9/frontend/src/components/sandboxEditor.js) does likewise.
- HOT pins [@openstreetmap/id 2.41.2](https://github.com/hotosm/tasking-manager/blob/cbf2ec89c38bf876bbc4de048f782978247ecfd9/frontend/package.json). Its [tagged iD localizer](https://github.com/openstreetmap/iD/blob/v2.41.2/modules/core/localizer.js) calls `new Intl.Locale(locale)` on requested locales and catches loading errors. JavaScript `new Intl.Locale('nl_NL')` throws `RangeError`, while `new Intl.Locale('nl-NL')` works and exposes base language `nl`. This is a **plausible source-level causal chain**, not a verified browser reproduction.

## Builder deliverable
[Small candidate patch](2026-11-09-hot-tasking-manager-7300-id-locale-candidate.patch) adds `normalizeIdEditorLocale` to the existing shared iD context utility, normalizes underscores to BCP47 hyphens with `Intl.getCanonicalLocales`, falls back to `en` on invalid inputs, and calls it only at the two embedded iD boundaries. Tasking Manager's React Intl/Transifex identifiers and persisted preferences are unchanged. Includes five Jest regression tests in the proposed upstream patch.

## Independent local tests and limitations
- Executed a **separate Node v22.16.0 isolated test harness** of the same helper logic with `node --test`: **5/5 pass**, including the original Dutch `Intl.Locale` failure, normalized Dutch, two other underscore locales, existing valid locales, and malformed/missing inputs.
- `git apply --check` of the candidate patch passed against a **minimal locally reconstructed source-context fixture**, not a complete HOT repository checkout. The GitHub patch was independently read back from Humanity Loop main.
- **NOT RUN:** HOT's actual Jest/ESLint build, the bundled iD 2.41.2 locale asset loading, real Dutch browser UI, sandbox end-to-end flow, production behavior, or maintainer acceptance. The iD bundle may have additional causes for the issue; the candidate must be rejected if browser evidence contradicts it.
- Deduplication: #7300 remains open, its visible comments did not identify a fix PR; GitHub PR search for Dutch iD locale returned none. This is not proof no unindexed work exists.

## Single-model fallback control sequence (NOT independent multi-LLM review)
1. **Scout:** Selected HOT's documented mapping-accessibility bug instead of repeating an internal website audit.
2. **Verifier:** Source code and upstream iD localizer support a testable hypothesis; causal proof still needs real runtime.
3. **PM:** Acceptance is Dutch and English fallback in both embedded editors, unchanged TM locale storage, no regression to other locales.
4. **Builder:** Patch and tests linked above; no upstream write.
5. **10th Man:** `Intl.Locale` normalization may not fix missing translation assets, and a locale change can restart iD, potentially affecting unsaved edits. Need manual regression checks; don't change live editors.
6. **Safety:** Tier-0 code proposal only; no logins, live map edits, secrets, outreach, or production mutation. **GO** for public-safe candidate preservation; **HOLD** for upstream PR/production release until verified.
7. **Revision:** Normalize at iD boundary, not in global user preferences; preserve `en` fallback.
8. **Outcome:** Candidate artifact and isolated tests verified. **Zero external acceptance, zero measured mapper benefit**.

## Next unchecked step
In an isolated **complete HOT Tasking Manager checkout** at the cited revision, apply the patch, run the frontend Jest suite and ESLint, then use an ordinary browser with the pinned iD bundle to confirm Dutch `nl_NL` loads translated strings (or English fallback) without affecting editing state; also check Czech and sandbox. If it passes, request maintainer/human review before any separately authorized external PR. If it fails, record exact failure and reject/revise. No AppDeploy or Foundry AI is required.

Cost/authority: $0 new cash, no paid model calls, no production changes, no external contact. Existing Humanity Loop hourly worker unchanged.
