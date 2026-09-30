# GitHub Issue Stewardship

The Humanity Loop issue tracker is an execution queue, not a museum.

## Cadence

Inspect all open Humanity Loop issues several times per day.

## Each pass

1. list every open issue;
2. compare each issue's success criteria against current repo/runtime/outcome state;
3. classify:
   - **close-ready** — success criteria objectively met and verified;
   - **advance-ready** — concrete next step is executable now;
   - **blocked** — specific dependency prevents progress;
   - **tracker** — intentionally remains open (for example a canonical watch thread);
4. close verified completed issues with a concise evidence note;
5. do not close tracker issues merely because the implementation exists;
6. advance at least one highest-value `advance-ready` issue when safe and non-duplicative;
7. update the issue with real implementation evidence, not vague status prose;
8. reconcile `PROJECT-STATE.md`, ledgers, and docs when issue state changes materially.

## Priority

Prefer:
1. completion of partially built work;
2. blockers affecting live outcomes;
3. Connector/Amplifier mobilization;
4. MCP/contributor infrastructure;
5. validated domain work;
6. speculative new infrastructure.

Do not create issues faster than the system can close or materially advance them.

## Close rule

An issue is close-ready only when:
- the required artifact/runtime exists;
- its stated success criteria are met;
- the result is verified;
- no critical acceptance criterion remains undocumented.

A deployed prototype is not automatically "done" if the issue requires lineage, safety, outcome, or interoperability controls that are still missing.

## Comments

Use issue comments for:
- verified completion evidence;
- concrete blocker diagnosis;
- durable next-step handoff.

Avoid hourly "still working" noise.
