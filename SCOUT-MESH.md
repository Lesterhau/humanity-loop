# STEEP+ Scout Mesh Runtime

Humanity Loop's Scout Mesh is a bounded weak-signal discovery system. It is designed to find useful, falsifiable emerging signals without turning every novelty into a project.

## Live control-plane state

Backend: Supabase/Postgres project `jxtcccrlnhkcjfnwlfea`  
Schema: `hl_control`

Tables:
- `scout_cells` — bounded geography × language × domain scan cells;
- `scout_signals` — structured candidate/verified/rejected/escalated signals.

Claim primitive:
- `hl_control.claim_due_scout_cell()` claims one due cell using `FOR UPDATE SKIP LOCKED`;
- exactly one cell is advanced per claim;
- a regression test verified one-cell-only mutation after an early ambiguous-column bug was detected and repaired before any scouting output was accepted.

## Initial deliberately small matrix

| Cell | Geography | Language | Domain |
|---|---|---|---|
| global-en-ai-infra | Global | English | AI infrastructure / compute / data centers |
| latam-es-public-health | Latin America | Spanish | public health / health-system access |
| west-africa-fr-climate | West Africa | French | climate adaptation / water / energy |
| se-asia-id-civic | Southeast Asia | Indonesian | civic access / digital public infrastructure |
| south-asia-en-education | South Asia | English | education / skills / learning systems |
| global-en-science-integrity | Global | English | science integrity / research infrastructure |

Do not scale the matrix merely because more cells are easy to add. Expand only after the existing cells produce useful, non-duplicative signals.

## Required signal fields

Every accepted Scout signal includes:
- provenance/source URL(s) and source date;
- geography/language/domain cell;
- signal type: weak signal, emerging issue, wild card, trend break, anomaly, or TIPPO;
- STEEP+ dimensions, including Values/Ethical/Demographic/Legal when relevant;
- TIPPO dimensions;
- Three Horizons placement;
- Futures Triangle push/pull/weight;
- cross-impacts;
- uncertainty;
- novelty score;
- usefulness score;
- evidence-quality score;
- existing-solutions check;
- falsification criteria;
- escalation recommendation;
- verifier note/status.

## Scoring

Scores are heuristic decision-support values from 0–1, not scientific measurements.

### Novelty
- 0.0–0.3: established/duplicative;
- 0.3–0.6: meaningful variation or underused development;
- 0.6–0.8: emerging combination, transition, or capability shift;
- 0.8–1.0: unusually novel and independently evidenced.

### Usefulness
Estimate whether the signal could materially improve project selection, prevention, resource allocation, transition planning, or a measurable intervention.

### Evidence quality
Weight primary/official/peer-reviewed evidence highest; community/industry observations can support a signal but should not independently justify consequential escalation.

### Uncertainty
Represents uncertainty in interpretation/trajectory, not whether the cited event exists.

## Escalation

A signal does not become a project automatically.

Default flow:
Scout → Verify → existing-solutions check → cross-impact/leverage review → appropriate Foundry specialist.

Escalate only when:
- evidence clears the relevant threshold;
- novelty/usefulness beats duplication cost;
- the next action is proportionate and reversible;
- falsification criteria are explicit.

## First verified signal

Cell: `global-en-ai-infra`

Signal:
**Water-free megawatt-rack cooling is moving from isolated prototypes toward coordinated validation.**

Evidence combines:
- DOE COOLERCHIPS 1.5 movement toward validation of water-free advanced cooling at up to 1 MW/rack;
- Open Compute Project demonstrations of working high-density cooling prototypes.

The signal is deliberately narrow: it does **not** claim that water-free/two-phase cooling has won or that net environmental benefits are proven.

Scores:
- novelty: 0.70
- usefulness: 0.85
- evidence quality: 0.88
- uncertainty: 0.35

Escalation:
Planetary Impact Accountant should compare lifecycle water, energy, materials, reliability, and retrofit tradeoffs before Humanity Loop treats the technology as environmentally favorable.

## Cadence

The main hourly worker may claim at most one due Scout cell per eligible Scout-Mesh cycle. Do not burn compute on every cell every hour.

Suggested operating cadence:
- inspect one due cell at least every 6 hours when higher-priority core-readiness/outcome work does not displace it;
- each cell defaults to a 24-hour cadence;
- no signal is required from a scan;
- "nothing sufficiently useful/novel found" is an acceptable outcome.

## Success metric

Measure:
- signals verified vs rejected;
- novelty/usefulness distribution;
- duplication rate;
- fraction escalated into useful work;
- external outcomes eventually attributable to Scout-discovered opportunities;
- false-positive / dead-end rate.

The Scout Mesh should be expanded only when marginal cells produce enough verified useful signal to justify their research and compute cost.
