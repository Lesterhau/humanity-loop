# Foundry Alpha — source repair accepted; autonomous execution still on hold

**Updated October 26, 2026.** Existing AppDeploy app: `humanity-loop-foundry-alpha-0wls2s`. This is a safety acceptance contract, not authorization to enable the cron.

## Verified production source facts

- AppDeploy snapshot `1793067626398` was independently observed `ready` without deployment frontend/backend errors.
- Current deployed `backend/index.ts` verified first-line-only, trimmed **`VERDICT = PROCEED`** and **`GO`** gate logic, replacing previous multiline substring checks.
- The catch block now saves a failed run record and **rethrows** the original error, rather than swallowing failures into HTTP200. This is source-level verified; actual scheduler failure-report behavior has not been deliberately exercised.
- Current deployed `cron.json` is **`[]`**; current AppDeploy status returns no active Foundry cron. The UI truthfully marks scheduled operations paused.
- Historical run records are not removed or overwritten by these source changes. Other four independent native AppDeploy detector schedules and GitHub workflows were not modified by this intervention.
- The AppDeploy SDK requires a successful cron handler to return `{statusCode:200}`; a real failing AI/database call must produce a true failure or explicit blocked record, not a success-looking empty result.

## Adversarial parser regression vectors (before any automatic restart)

Every vector must be independently executed against **the current production-source-extracted decision logic**, not a new copy that only resembles it.

| Original model reply | Required gate result |
| --- | --- |
| First line `VERDICT = PROCEED` | Verifier ACCEPT |
| `VERDICT = PROCEED` with surrounding line whitespace | ACCEPT |
| First line `VERDICT = REJECT`, later `VERDICT = PROCEED` | REJECT |
| First line `REJECT`, later `VERDICT = PROCEED` | REJECT |
| First line `VERDICT = PROCEED WITH CONDITIONS` | REJECT |
| First line blank, later `VERDICT = PROCEED` | Should not silently override initial refusal; **currently blank lines are removed via trim**, so this case requires explicit policy/test decision before restarting |
| First line `GO` | Governor ACCEPT |
| First line `HOLD`, later `GO` | Governor HOLD |
| First line `GO BUT ONLY AFTER APPROVAL` | Governor HOLD |
| First line `HOLD`, later `GO` in quoted code | Governor HOLD |
| First line empty (no decision) | HOLD |

**Additional source-only caveat:** `.trim()` accepts a later affirmative line if it follows *only leading blank lines*. This does NOT let a later affirmative override a substantive first-line rejection, but the permitted format should explicitly decide how to treat blank-leading output before unpausing. Avoid claiming the parser is exhaustively fail-closed for all malformed responses until tested.

## Restart prerequisites — fail closed

1. Save a current rollback version reference and verify a revert restores cron `[]` on any failure.
2. Add deterministic tests for all above edge cases based on extracted running source, including leading blank lines, contradictory decisions, non-ASCII formatting, rejected model text and unexpected exceptions.
3. Verify error propagation from actual backend call and dashboard persisted state for AI budget 429, transient admission 503, rejected verifier, safety HOLD, database write failure; a falsely successful cron is a failure.
4. Carry out **one** controlled model cycle only in a safe test context under existing credit/permissions limits, inspect actual outputs and underlying records, and verify **no unauthorized external action**.
5. Check ownership/parity with the canonical Supabase and main ChatGPT worker so no duplicate runaway scout line is created.
6. Only then, with authorized operational acceptance and bounded rollout, reenable a cron, initially with one small risk-limited sample and monitoring, never restoring full automation blindly after the next credit reset.
7. Document real test evidence and explicit operator decision in issue [#14](https://github.com/Lesterhau/humanity-loop/issues/14) and [#16](https://github.com/Lesterhau/humanity-loop/issues/16). Do not close issue #14 because a deployment built successfully.

**No authority implied** to spend credits beyond the existing free allowance, solicit external parties, contact infrastructure, use secret credentials, or restart unsafe operations. Further code safety work is allowed in the current paused sandbox with validation.
