# Foundry Runtime and Fallback

This file defines how Humanity Loop keeps the bounded Foundry control spine available when one execution provider is unavailable.

## Goal

Preserve the Foundry function without pretending that provider-specific model execution is vendor-neutral.

The control spine remains:

Scout → Verifier → Project Manager → Builder → 10th Man → Safety Governor → Revision → Outcome Tracker.

Specialists are activated only when the task needs them.

## Runtime modes

### Mode A — independent provider worker

Use the deployed Foundry Alpha worker when its scheduler is healthy and a recent run proves it is executing.

Current AppDeploy surface:
https://humanity-loop-foundry-alpha-0wls2s.v2.appdeploy.ai/

A reachable UI or healthcheck does **not** prove the worker scheduler is active.

### Mode B — main-worker fallback

If the independent Foundry scheduler is disabled, stale, or otherwise unavailable, the canonical Humanity Loop hourly worker may execute **at most one** bounded Foundry cycle during that hour.

Fallback is allowed only when:
- the independent worker is verified inactive/stale;
- no equivalent Foundry cycle is already in progress;
- higher-priority pending external failures or time-sensitive safety work do not require the cycle instead;
- a useful, non-duplicative Tier-0 or otherwise authorized task exists.

Do not generate a fake task merely to keep the Foundry busy.

## Single-active-scheduler rule

Never run Mode A and Mode B for the same cycle.

Before fallback:
1. check independent Foundry cron/last-run state;
2. check recent canonical run receipts;
3. claim one fallback cycle;
4. execute;
5. persist the result;
6. release the claim.

If the independent worker resumes, fallback yields on the next cycle after verification.

## Role separation

A fallback cycle may use one underlying model, but roles must remain logically separated.

Each role receives only the context needed for its job:

- **Scout:** problem/opportunity, affected people, why now, smallest useful deliverable, evidence needed, duplication risk.
- **Verifier:** PROCEED/REJECT, unsupported claims, duplication, evidence gates, narrow safe scope.
- **Project Manager:** one-cycle plan, acceptance criteria, dependencies, external-verification needs.
- **Builder:** actual deliverable or concrete external action, not another plan.
- **10th Man:** fatal flaws, manageable risks, unknowns, "If this wins, who loses?", mitigations.
- **Safety Governor:** GO/HOLD with minimum safeguards under `GOVERNANCE.md`.
- **Revision:** incorporate dissent/safety without scope bloat.
- **Outcome Tracker:** success evidence, next review, stale threshold, escalation, closure/falsification.

Generation and validation must not be collapsed into one unexamined judgment.

## Persistence

Fallback cycles are institutional work, not chat memory.

For each meaningful cycle, preserve a compact machine-readable or Markdown receipt under:

`runtime/foundry-fallback/`

Minimum fields:
- run ID;
- started/completed timestamps;
- scheduler mode = `main-worker-fallback`;
- candidate;
- verification verdict;
- plan;
- artifact/action reference;
- dissent;
- safety decision;
- outcome plan;
- status = completed | held | failed;
- evidence/provenance links where applicable.

Meaningful external actions also update `ACTION-LEDGER.md` / `actions.jsonl` as required.

## Permissions and limits

Fallback does not expand authority.

- Default to Tier-0 reversible work.
- Tier-1 external actions still follow `OPERATIONS.md`.
- Tier-2 still requires human/qualified oversight.
- Tier-3 remains prohibited/specialist-controlled.
- No unrestricted recursive spawning.
- No autonomous financial/legal commitments.
- No unauthorized personal-account use.
- No political persuasion.
- No harassment, intrusion, deception, or coercion.
- No unbounded compute loops.

A child/specialist role never inherits more authority than the parent cycle.

## Provider-neutrality requirement

The fallback is continuity, not the final architecture.

Longer term, separate:
1. deterministic queue/lease/checkpoint state;
2. provider adapters for model calls;
3. tool/action adapters;
4. evidence and safety gates;
5. durable run/event storage.

A provider adapter should be replaceable without changing mission, role definitions, permissions, or outcome criteria.

## Recovery criterion

The independent Foundry blocker is fully resolved only when either:
- its original scheduler is reliably restored; or
- a replacement independent runtime has been live-validated with bounded cost, secrets discipline, checkpoint/retry behavior, role permissions, safety gates, and no duplicate scheduler.

Until then, Mode B keeps the Foundry function alive but should be described as a fallback, not as an independent multi-agent fleet.
