# STEEP+ Scout Mesh Runtime

Humanity Loop's Scout Mesh is a bounded weak-signal discovery system. It is designed to find useful, falsifiable emerging signals without turning every novelty into a project.

## Information integrity and covert-influence resilience — October 27

Treat public information manipulation, foreign influence disclosure and coordinated AI/bot amplification as a **priority read-only discovery lens**, alongside defensive AI-swarm resilience, not as a partisan persuasion mission. Read [INFORMATION-INTEGRITY-SCOUT.md](INFORMATION-INTEGRITY-SCOUT.md) for required source attribution, protections against treating identity or criticism as proof of misconduct, and comparative assessment of Israeli/Russian/other state actors, powerful platform owners and coordinated inauthentic networks. Public documentation and accurate source explanations are permitted; no mass replies, harassment, political microtargeting, unlawful access, or claims about specific actors without case-level proof. Preserve the existing six geographic cells and deduplicate other Scout findings.

## Defensive priority: AI-swarm resilience in interconnected essential systems (October 24)

The Scout Mesh should include **defensive resilience against coordinated AI-enabled threats** as a recurring candidate discovery theme, alongside—not in place of—its existing global STEEP+ priorities. Seek verifiable public-interest gaps and solutions in electric grids and utilities, water, telecommunications, healthcare, banking/payment networks, logistics and government digital services.

Look for defensive methods and credible teams working on: agent identity and least privilege; transaction and tool-use authorization; rate limits and kill switches; coordinated anomaly detection; cross-provider incident reporting; adversarial evaluation in consented sandboxes; human override; segmented networks; recoverable operations; supply-chain provenance; and independent testing of resilience claims.

**Allowed outputs:** public-source evidence briefs, documented defensive opportunities, responsible introductions with consent, safe benchmarks, vetted solution directories, and audience-relevant educational content. Assess practical deployment readiness, safeguards, independent validation, and who can act.

**Not allowed:** probing live infrastructure, credential harvesting, exploiting vulnerabilities, building or coordinating attack swarms, accessing banks or utilities without authorization, or publishing actionable attack details. Do not claim any target has a vulnerability based solely on general threat research. Route specific vulnerabilities to responsible disclosure.

Deduplicate against existing security scouts and open issues before creating a new agent or recurring task. Start with a bounded research scout using existing scheduled capacity; spawn a separate worker only if the queue, measurable workload and permission boundaries justify it. The goal is useful defensive connections and verified improvements, not more bots for their own sake.

## Verified completion receipts — October 24, 2026 (partial recovery, NOT scheduler restoration)

**INTEND / implementation:** A private, additive Supabase migration `add_private_scout_review_completion_receipts` introduced `hl_control.scout_review_receipts`, `scout_cells.last_completed_at`, and the invoker-rights `hl_control.record_completed_scout_review(text,text,timestamptz,text,jsonb,text,text)` function. The new table has RLS enabled and no PUBLIC/anon/authenticated table privileges; the function's EXECUTE privilege is limited to the database owner. This is an internal evidence-accounting improvement, not public exposure or proof of an autonomous specialist.

**Actual independently read-back first receipt:** `1e4812e4-0a0a-46be-ac70-723be8cfac15`, cell `global-en-ai-infra`, decision `verified_candidate`. The record explicitly **backfills a source-reviewed investigation completed October 24 at 12:53:46Z**, with its actual evidence in [the AI security guide contribution Scout](research/scout-mesh/2026-10-24-global-en-ai-infra-open-source-security-guide-contribution.md). The DB record was created at 21:54:48Z, *not* at the research completion time. Independent readback confirmed both timestamps and source pointers. The proposed external contribution was blocked HTTP 403; no third-party effect or adoption occurred.

**Strict semantics:** `last_completed_at` now records only reviews that were separately source-checked and explicitly finalized with an evidence pointer; the old `last_run_at` and `next_due_at` still represent **claims**, not completions. The old `claim_due_scout_cell()` function was deliberately left unchanged for compatibility and **must not be used as proof of a scan**. **Live read-only check at 2026-10-25 03:01Z:** **5 of 6** active cells now have independently recorded source-review completion receipts. Only `se-asia-id-civic` has `last_completed_at = null` despite a separately documented October 24 investigation; do not backfill without verifying the exact completed research and provenance. All six old claim timestamps still read October 2. The original first-receipt backfill is not a new evening scan. **No autonomous six-hour scheduler recovery has been demonstrated; issue #19 remains open.**

**Use safely:** After a real, completed source-reviewed investigation has been saved and independently fetched from the canonical repository, call `record_completed_scout_review` with the correct cell, exact research completion time, canonical GitHub evidence URL, decision (`verified_candidate`, `no_signal`, `rejected`, or `source_blocked`), JSON array of primary sources, truthful summary and owner. The function rejects future/implausibly old timestamps, enforces one receipt per cell/evidence URL, and updates `last_completed_at` atomically on first insertion. Independently query the receipt and cell afterward. A database row or function success alone cannot validate the cited research; check actual source content first. No direct public RPC access is granted.

**Latest verified rotation:** `global-en-science-integrity` was independently source-reviewed on **2026-10-25 02:59:15Z** and the canonical [Liu Bayesian ADHD retraction-dependency Scout](research/scout-mesh/2026-10-24-global-en-science-integrity-bayesian-adhd-retracted-trial.md) was read back. Private completion receipt **`94ee2ff3-23f8-44fc-9c06-d17dc398ffea`** was independently read back at 03:01Z, with the original claim columns unchanged. This is a new verified **research candidate**, not a journal correction or a recovered scheduler; [issue #25](https://github.com/Lesterhau/humanity-loop/issues/25) holds its October 30 editorial verification gate.

**Next narrow fix:** Integrate due-cell selection with `last_completed_at` and durable completion receipts, prove an ongoing six-hour cadence rather than clustered manual completions, and reconcile the Southeast Asia cell only with a verified original research timestamp. Implement an expiring lease/claim path or completion-only crash recovery before changing the legacy claim function. Never backfill undocumented scans, create a seventh idle worker, or close #19 on receipts alone.

## Completion-based due selection — October 25, 2026 (verified selector, NOT scheduler recovery)

**Additive private migration:** `add_private_completion_based_scout_due_selector` created `hl_control.list_due_scout_cells(p_as_of timestamptz DEFAULT now(), p_limit integer DEFAULT 6)`. This is a **read-only, security-invoker** SQL function. It selects active cells due from **verified `last_completed_at` + `cadence_hours`** (or never completed), sorted oldest completion first, rather than from legacy claim timestamps. It never advances timestamps, claims a cell, performs research, sends messages or starts an agent. Execution privileges were revoked from PUBLIC, `anon`, and `authenticated`; only authorized database operators can run it.

**Independent SQL verification:** At the October 25 check, `select * from hl_control.list_due_scout_cells(now(), 6)` returned **zero due cells**, consistent with all six completed within their 24-hour cadences. A deterministic as-of test at `2026-10-26T04:00:00Z` returned all six cells in oldest-completion order; a limit-one test returned only `global-en-ai-infra`. Post-migration readback confirmed `security_definer=false`, no PUBLIC/anon/authenticated EXECUTE permission, **6/6 completion records**, and **all six legacy `last_run_at` values still October 2**. The first expected due time from the recorded completions is `global-en-ai-infra` at **2026-10-25T12:53:46.656Z**.

**Operational handoff:** The existing main worker may query this function at an eligible Scout window, then perform actual source research and independently read back the completion receipt. No automatic scheduler, lease/claim recovery, or ongoing six-hour cadence has been demonstrated. Issue [#19](https://github.com/Lesterhau/humanity-loop/issues/19) remains open pending spaced, genuinely completed research rotations and verified durable outcomes. Do not use the legacy `claim_due_scout_cell()` as evidence of a scan.

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
- **Critical accuracy qualification independently verified October 21:** `claim_due_scout_cell()` **immediately updates `last_run_at` and `next_due_at` on CLAIM**, before any source research. Therefore those fields record **claims, not verified finished research**. Treat completed evidence reviews as a distinct receipt with source, time, analysis and readback. Do not call the claim RPC just to refresh its timestamp. Correct completion semantics under [P1 issue #19](https://github.com/Lesterhau/humanity-loop/issues/19); current functions do not independently prove completed cycles.
- **Current empirical incident:** all six active cell claim timestamps remain October 2 at 06:38 UTC and all `next_due_at` timestamps October 3; one verified `scout_signals` row was recorded October 2. No later Scout cell claims or source-verified completion receipts were found in this store as of Oct21. The system has not demonstrated its planned recurring six-hour research rotation.

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

**Cross-cutting defensive priority (Oct 23):** AI-enabled coordinated cyber threats to critical infrastructure, financial institutions and essential digital services; search for public, defensible **protective solutions and unmet support needs**, not attack targets. Apply [AI-INFRASTRUCTURE-DEFENSE-SCOUT.md](AI-INFRASTRUCTURE-DEFENSE-SCOUT.md) alongside existing geographic/topic cells, especially the global AI infrastructure and science integrity domains where relevant. Track [issue #21](https://github.com/Lesterhau/humanity-loop/issues/21) without adding a seventh idle cell or new schedule. This new priority does **not** excuse overdue claim-vs-completion recovery [#19](https://github.com/Lesterhau/humanity-loop/issues/19).

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

Required operating cadence:
- complete or independently record a concrete safety/access block for **one due cell within every six-hour window**. Do not let known maintenance issues starve the Scout Mesh indefinitely. A mere claim timestamp does not count. During current issue #19 recovery, avoid the unsafe claim-as-completion assumption; use independently verifiable research-completion evidence, and do not bypass an execution write block;
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
