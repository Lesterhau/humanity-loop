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

Every pass must rank **all open issues before working them**. Do not default to issue number, recency, or easiest-first.

Score qualitatively on:
1. safety / catastrophic-risk reduction;
2. architectural blocking value — how many other issues it unlocks;
3. live-outcome impact;
4. completion leverage — partially built work that can be finished now;
5. tractability / autonomous feasibility;
6. evidence quality and reversibility.

Work the highest-ranked safe executable issue first. Lower-ranked cleanup must not displace a materially more important blocker.

Default tie-break order:
1. safety/governance controls;
2. core runtime/control-plane blockers;
3. gateway/MCP interoperability;
4. Connector/Amplifier real-world mobilization;
5. scouting/verification infrastructure;
6. environmental/resource accounting;
7. domain divisions and pilots;
8. contributor/discovery polish;
9. intentional tracker issues.

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
