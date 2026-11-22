# Humanity Loop Mission Control — END STATE AND CRITICAL PATH
**Owner directive adopted 2026-11-21 (America/Chicago); updated November 22 after the IRS source-audit reconciliation.**

**CURRENT GATE: G2, repeatable zero-new-cash, founder-independent case execution.** G1's fourth historically verified external publication correction is now [WIN-004](WIN-LEDGER.md): the September 18 IRS 2025 EITC multilingual threshold report preceded official six-language corrections independently checked November 7 and again November 22. **No IRS causal acknowledgment**, no newly observed November 22 edit, no actual taxpayer usage. The other OT-005 issues remain unresolved. This is a retroactively recognized fourth recorded correction, not a claim that today's review made the IRS act.

**This is the ONE operational priority framework.** The authoritative machine-readable gate state is [ops/mission-control.json](ops/mission-control.json); the independent outcome record remains [WIN-LEDGER.md](WIN-LEDGER.md). The hourly coordinator must not replace actual evidence with optimistic status narration.

## End state (a TARGET, not a current capability)

Humanity Loop is a **worldwide, permissioned, accountable AI public-benefit operation** that, without the founder having to operate every task, repeatedly identifies a tractable public-interest problem, independently checks official evidence, takes a bounded authorized action, independently confirms an actual external correction or useful adoption, and shares a reproducible public record with the responsible institution properly credited. Keep it viable on zero new cash while the project establishes a sustainable funding model; external volunteers and paid inference are **not dependencies**.

**Proposed ultimate acceptance window:** four independently verified external outcomes per rolling 28 days, at least three distinct regions and three reviewed languages, 30 consecutive days of operation without founder-specific manual steps for ordinary Tier-0 work, **zero** unapproved spending and consequential actions, tested privacy/delete/stop controls and qualified oversight. These are operating targets, *not a promise, current count, or service-level agreement*.

**Units that matter:**
- External correction/real adoption = source-backed, independently verifiable outside change with date, provenance, and attribution caveat. The source-of-truth win ledger currently contains **four** (`WIN-001/002/003/004`) historically verified U.S. public-source changes, including one low-causal-attribution IRS correction. Four historical records are **not** four in the required rolling 28-day window. Public readership or beneficiary usage is not known.
- Report sent, accepted by an inbox provider, reply received, unverified source claim, CI test, model run, public issue, website build, or volunteer response = useful **intermediate evidence**, never a win.
- Independently registered non-owner nodes = a separate scale metric; the core outcome pipeline must function even if this number remains zero.

## Reverse-engineered release gates

| Gate | Achievable condition | Concrete test | Current truth |
| --- | --- | --- | --- |
| **G1** Fourth verified correction | One more externally implemented fix independently checked and entered in WIN-LEDGER | September original report, independent November 7 and 22 official source comparisons, [adjudication](runtime/case-steward/ot005-2026-11-22-irs-outcome-adjudication.md) | **ACHIEVED:** retrospective WIN-004 IRS 2025 translated-guidance correction. Causation unproven. |
| **G2** Repeatable low-cost founder-independent case cycle | Two distinct cases progressed through evidenced discovery, bounded authorized action, and independently checked final disposition, including a case not manually operated at every step | Two distinct end-to-end case receipts, recorded source/agency outcomes and zero new paid API charges | **ACTIVE:** OT-003 and OT-013 are the two WIP cycles, both awaiting external publication / source change. **0 cycles accepted under this new gate.** |
| **G3** Portable governed Foundry | One **real** model-produced public-safe artifact under bounded lease, source review, provider cost stop, negative auth/failure tests and zero duplicate schedulers | Verifiable model outputs, reviewer decision, canonical leases, budget tests | Pending G2; local Ollama is optional, not mandatory to continue case work |
| **G4** Cross-border replication | Verified outcomes in at least two countries; locally appropriate sources, languages and reviewer checks | Official before/after, independent evidence and jurisdiction competence | Pending G3; Pakistan is a case being worked, not a win |
| **G5** Sustainable global service | Meets end-state 28-day metrics plus privacy/retention, abuse, accessible multilingual intake, review capacity and operating budget | Rolling evidence audit, not an architecture diagram | Pending G4 |

We do not treat **100 or 1,000 agent registrations** as the goal. Additional contributors are optional capacity once they can be permissioned and reviewed safely. The system must succeed with *zero* independent volunteer nodes as an initial condition.

## Parallel development policy — G2 operations, G3/G4 engineering, G5 safeguards

**Release gates remain sequential, engineering does not.** We preserve exactly one active accepted-release gate (currently G2). While actual G2 public-source/agency changes await their defined dates or substantive replies, execute one demonstrably testable engineering task for G3 or G4 **without opening another external case** or requiring recruited volunteers, laptop time, new hosting or paid inference.

The [machine-checked milestone state](ops/mission-control.json) now holds separate `development` fields for G3, G4 and G5. Its selector exposes `parallel_readiness` separately from `active_gate`; the validator rejects any attempt to mark later gates `achieved` before prerequisites. Readiness artifacts are **not accepted public benefit**.

- **G3, engineering IN PROGRESS:** [source-evidence validator](scripts/foundry_source_evidence.py) + [Foundry Lite](scripts/foundry_lite.py) accept a bounded, manually provided, task-matched official-source candidate packet. They can produce a source-specific checklist for an independent reviewer or pass the *untrusted* packet to the local eight-role drafting workflow. They do **not** fetch live URLs, grant source verification, publish, lease canonical tasks, start models automatically or spend paid credits. A genuine eight-stage local model result, independent reviewer, robust lease and provider hard budget stop are still missing. The actual 1B laptop test held safely at stage 2.
- **G4, engineering IN PROGRESS:** the same validator and CI execute source-candidate examples from **Texas WIC (US, English/Spanish)** and **LUMS climate atlas (Pakistan, English)**. The arithmetic checker independently establishes that 84/117 rounds to **71.8%**, which is inconsistent with a claimed 81.6%, while making **no claim about whether 103 or 117 is the correct underlying dataset cohort**. The U.S. bilingual test flags qualified Spanish review as required. These are flagged `fixture_only`; they are not completed new source checks, external outcomes, approved translations, or proof of international operational readiness. [US fixture](foundry-lite/fixtures/ot003-us-bilingual-source-candidate.json) · [PK fixture](foundry-lite/fixtures/ot013-pk-climate-source-candidate.json).
- **G5, scoped:** Hold the end-state service requirements: region/language-qualified review, 28-day externally verified throughput, 30 founder-independent operating days, audited spending, privacy deletion/revocation ([issue #96](https://github.com/Lesterhau/humanity-loop/issues/96)), branch protection ([issue #68](https://github.com/Lesterhau/humanity-loop/issues/68)), and incident recovery. These are **not met**.

**Per-run operating rule:** Priority 1, respond to safety incidents and genuinely new time-sensitive outside evidence; priority 2, move due G2 case work one legitimate step forward; priority 3, when G2 is genuinely blocked waiting on others, complete one preselected G3/G4 **executable** test or gate-blocker repair with a verified result. Do not claim that additional test files or documents alone establish model execution, two-country public outcomes or a sustainable worldwide system.

## WIP = 2. November 22 active case cycles

1. **OT-003 (U.S., English + Spanish).** A Texas WIC fair-hearing PDF still misleadingly implies HHSC assigns an appellant a lawyer. HHSC confirmed the lawyer represents the *agency* and said on November 2 it would remove the sentence. On November 21 the live PDF image still showed both old language variants. A single factual update/request for publication status was sent in the authorized existing thread and **independently read back** at **2026-11-22T04:46:50 UTC**. **Next:** check original PDF for a visibly corrected bilingual version on/after **November 30 UTC** or sooner only after a substantive agency response. No extra routine email. A revised document must actually be retrieved and compared before any **additional** win is considered.
2. **OT-013 (Pakistan, English).** LUMS CITY climate atlas public summary still says 103 schools in one place and 117 elsewhere, with 84/117 incorrectly shown as 81.6%; the listed top-five events include three 2025 dates while prose says four. The original public page was source-checked November 21; one proportional factual follow-up was sent to the previously used institutional contact and **independently read back** at **2026-11-22T04:47:53 UTC**. **Next:** recheck exact original public copy on/after **December 2 UTC** or after a substantive reply. No further routine outbound correspondence. The underlying research dataset was **not audited**.

See [the exact read-only next-action selector](scripts/mission_control.py) and [the private-mail-safe action receipt](runtime/mission/2026-11-21-first-outcome-sprint.md).

## Decision rule for EVERY worker cycle

Run or inspect the no-network selector:
```bash
python3 scripts/mission_control.py
```
The output is an **offline decision aid**, not a live external-source scan, a scheduled job, a true cost meter or an autonomous legal/medical/publication authorization.

1. Continue one overdue material incident or genuine urgent outside consent/response first; inspect before answering; don't impersonate a participant.
2. If a **focus case** is due, perform exactly one fresh primary-source read and move it only one legitimate step closer to independent external outcome. Every material action needs INTEND → EXECUTE → independent VERIFY → COMMIT, not merely a self-reported note.
3. If both focus cases are awaiting publication, **do not repeatedly email recipients or generate status updates**. Preserve the next dated checks and inspect substantive replies if available. For active **G2**, test one specific documented end-to-end case-cycle blocker using existing authorized tools and evidence without opening a third WIP case. Replace a focus case only if independently source-backed evidence clearly justifies displacing it. Otherwise report `no_new_evidence`; no simulated case completion.
4. Only count a win when there is **an actual outside change** observed in authoritative sources, cross-checked under [REVIEWER-RUNBOOK.md](REVIEWER-RUNBOOK.md), and correctly recorded in WIN-LEDGER. The repo's offline selector rejects mismatched ledger counts or claimed achieved gates without proof.
5. Use Claude, Gemini, DeepSeek, Perplexity or Ollama **as optional analysis/review tools when accessible within existing approved allowances**. Multiple copies of one model are NOT independent verification. External volunteers are optional; **never** wait for Facebook responses to keep working.
6. Escalate only where owner authentication, spending, irreversible/consequential external actions, private data, platform restrictions or actual legal/medical expertise require human authority. Explicit current broad authorization to conduct bounded project work removes repeated conversational permission-seeking, but never silently removes governance, consent, security, privacy or external-account restrictions.

## What is explicitly out of the critical path

Unlimited scout notes, repeated same-page no-change checks, speculative multi-agent role counts, new cron workers, cloud billing accounts, hosted GPU purchasing, unreviewed AI outreach, endless status PRs, crowdfunding or volunteer recruiting **are not milestones**. Fix these only when a dated deficiency is causally blocking the active gate, and prove that the repair enables a previously blocked test.

## Accountability and correction

- A failed or blocked attempt must report its precise observed failure and next *conditional* check. A self-issued receipt is not an outcome.
- G1 was closed by a conservative **retrospective** adjudication of a previously verified IRS correction; [WIN-004](WIN-LEDGER.md) and the source proof are in the same reviewed PR as the mission-control update. **The next increase to five wins** requires a distinct, newly evidenced outside change and updated ledger/mission state; existing IRS six translated pages never count as six separate wins. The mission gate rejects mismatched historical counts but cannot itself fact-check an external website.
- The existing hourly coordinator remains the **only** Humanity Loop ChatGPT scheduled worker. Foundry AppDeploy remains paused, the 350-credit reserve stays protected, and no extra recurring job is authorized here. Existing security issue #68 (unprotected GitHub main), retention issue #96 and Foundry acceptance issues #14/#16 remain open.
- International ambition requires regionally relevant evidence, human agency and qualified review; U.S.-only corrections cannot be misrepresented as worldwide demonstrated impact.

**Operating constraint:** There is no promise of autonomous future work from this chat alone. The existing separately enabled hourly coordinator can use the repo's current gate and source documents on its scheduled invocations. Check actual run receipts before claiming it executed these new instructions.
