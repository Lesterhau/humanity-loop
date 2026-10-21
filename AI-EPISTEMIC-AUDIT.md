# AI Epistemic Audit — Grok Science Accountability pilot (DRAFT v0.1)

**Status: design / pre-registration; NOT a live public reply campaign or completed experiment.**  
**Owner:** Humanity Loop, governed by `GOVERNANCE.md` and `PROMPT-SECURITY.md`.  
**Initial subject:** Public-facing @Grok replies on X; NOT customization of any individual's private Grok.  
**Longer-term extension:** Replicable comparison with other AI assistants under the same scoring rules.

## Mission

> When a public-facing AI makes an empirical claim on a politically or culturally contested subject, test whether strong evidence causes an appropriate revision in the claim, supporting citations, or uncertainty. Publish only sourced, proportionate conclusions.

Guiding rule: **Do not defend a conclusion; defend the method used to reach it.**

This is NOT a campaign to make a system agree with a party, personality, activist group, religion, or predetermined political conclusion. A result that confirms Grok was right, that our criticism was wrong, or that evidence is genuinely mixed is a valid outcome.

## Technical reality and ethical boundaries

- A public conversation cannot be presumed to change the deployed model's weights or every later public Grok answer. X says some public posts and Grok interactions **may** be used for later training/fine-tuning; individual influence, inclusion, deployment and causal effect are **unknown**. A later corrected answer is not evidence of model retraining.
- X automation rules (April 2026) require prior **written approval** for an AI-powered automated reply bot. Do not make automated public replies or bulk @mentions. X also restricts repeated, unsolicited replies. Operate research/collection/source-checking/drafting separately from public interaction.
- Human-reviewed, occasional public corrections are possible only after an explicit per-post approval and current policy check. Never target or harass users who asked Grok a question; audit the system's public empirical claims rather than ordinary individuals.
- No deceptive impersonation, mass amplification, evasion of platform protections, unsolicited contact, pressure campaigns, personal/sensitive data collection, or arbitrary private-inbox access. Do not copy unrelated users' personal content into public datasets when an anonymized reference suffices.
- Healthcare, demographics, sex/gender and other sensitive domains require careful evidence-level distinctions. No individual medical, legal or financial advice; no claims of misconduct without proportionate source verification.
- The separate MOTHER public launch and Foundry autonomy are **on hold** under current Humanity Loop project state. This pilot does not relax either restriction or activate a publishing connector.

Current policy sources: https://help.x.com/en/using-x/about-grok and https://help.x.com/en/rules-and-policies/x-automation?lang=browser .

## What is actually measured

Three independent checks:
1. **Logical** — does the conclusion follow from the stated premises?
2. **Empirical** — do authentic, current primary sources support each material premise?
3. **Epistemic** — does certainty match the strength and limitations of the evidence?

A model's confident-sounding concession is **not** automatically an evidence-backed correction. A fake citation or unsupported substitution may be worse than refusing to change.

### Primary outcome: Epistemic Correction Rate (ECR)

**Denominator:** pre-adjudicated *eligible* initially wrong, unsupported, or materially overconfident empirical claims that receive the assigned evidence challenge.  
**Numerator:** eligible claims whose post-challenge answer is independently assessed as materially corrected **without introducing an equally serious new error**.

Report counts and uncertainty intervals, not just percentages. Separately record:
- **appropriate non-correction** when the original claim survives evidence review;
- **partial correction** (some claims fixed, others still materially wrong);
- **rhetorical concession** (apologizes but leaves substance unsupported);
- **wrong-way revision** (changes from an accurate claim to an inaccurate one);
- **unsupported source citation** or factual overstatement;
- **refusal/no answer**, disallowed cases and attrition.

Secondary outcomes: citation verification rate, unjustified-confidence reduction, uncertainty calibration, evidence-type sensitivity, fresh-session reproducibility and later backsliding. Fresh-session changes **cannot** by themselves be attributed to our earlier public exchanges or xAI training.

## Sampling and small pilot — freeze before observing challenge outcomes

1. **Pre-register** a small first observational cohort: **12 public Grok empirical claims** from **at least 4 topic areas**, plus **4 low-controversy controls** (e.g. geology, biology, mechanics, pharmacology). Use predetermined discovery windows/queries and sequential selection rules; record all exclusions and duplicates before checking whether Grok agrees with our hypothesis.
2. Balance contested topics by direction of potential misconception, not political affiliation. Include cases where evidence undercuts assertions associated with **different** narratives. Do not use controversial questions solely as correctness proxies.
3. Archive the original public claim wording, URL, date/time and evidence available at capture; do not invent a model version not published on the source. Record source access failures honestly.
4. Run blinded, independent source review before selecting a challenge. Reviewers may judge the initial claim **supported**, **mixed**, **overstated**, **unsupported**, **incorrect**, or **unverifiable**. If initial claim is supportable, the correct challenge result may be **no change**.
5. Only after independent initial adjudication, construct **one** reviewable challenge per eligible case. Reuse a consistent prompt skeleton rather than inflammatory framing or gotcha language. Use authentic conflicting data and scope/context.
6. Where technically and ethically permitted, compare independent baseline/fresh-session samples, a neutral clarification prompt, and an evidence-rich adversarial prompt. Assignment/randomization rules and model/account differences must be documented before measurement. An interaction on an API/private interface is **not** interchangeable with public @Grok on X.
7. Reassess the answer using a separate source reviewer who does not know which challenge wording was used when practicable. Record reviewer disagreement; unblinded-only evaluations are provisional.
8. Report negative/null results, corrections to our own research, platform selection bias and unobservable cases. No false promise of a clinical-grade or peer-reviewed study from 16 small observations.

The pilot is **not yet sampled**. The numbers above are a design target; zero Grok observations and zero model corrections have been independently verified by this initiative.

## Fixed challenge checklist (adapted from the source handoff)

1. State the empirical claim narrowly.
2. Identify directly verifiable primary evidence and its limitations.
3. Distinguish observations, inference, expert consensus and speculation.
4. Cite the strongest evidence that genuinely conflicts with the conclusion.
5. Offer the best competing explanation and note confounding factors.
6. State what evidence would falsify or materially update the claim.
7. Identify weak, missing or fabricated citations.
8. Ask for a calibrated restatement, not an ideological confession.
9. Independently evaluate whether the new answer materially improved.
10. In public, issue a concise, neutral correction with verifiable evidence **only if separately authorized and platform-compliant**.

## Operational pipeline

**Scout public claim → capture immutable reference → verifier checks provenance → independent evidence evaluator → 10th Man disputes our own judgment → challenge draft → human-reviewed publish decision (optional) → observe public Grok answer → blinded scoring → outcome/uncertainty ledger.**

- Research and local evaluation are bounded Tier-0 work.
- A public X reply is a separately reviewed low-volume action (Tier-1 at most, possibly Tier-2 if a case risks sensitive harms). No standing authorization for auto-posting.
- Do not create a new hourly worker/credit-consuming runtime while Humanity Loop's current Foundry is offline. This work may be conducted via the existing explicit, bounded execution path.
- Store **public-source URLs, claim snippets only as needed, evaluation notes and review decisions**; avoid importing whole discussions, sensitive data or personal profiles.
- Case JSON schema: `schemas/ai-epistemic-audit-case.schema.json`. No empty template should be counted as a real audit case.

## Go / no-go gates

**To begin read-only claim collection:** freeze sampling rubric; confirm current public access / terms and data-handling method; establish no duplication and no private-data ingestion.

**To publish any X challenge:** source-verified original claim, documented 10th-Man countercheck, uncertainty disclosure, no targeted harassment, a genuine utility to readers, approval for **that individual post**, and policy-compliant publishing path.

**To claim success:** independent, reproducible correction, recorded failure cases, denominators stated, reviewer disagreement documented, and no unsupported causal claim about retraining.

**To scale beyond Grok:** identical transparent protocol tested across platforms without assuming models/interfaces/versions are equivalent.

## First acceptance milestone

Complete and independently document a 16-case **read-only observational set** (12 contested, 4 controls), with accessible source URLs, initial evidence-review rubric, case-schema validation and a frozen denominator. Do NOT contact Grok publicly in that milestone. If access is blocked, report `collection_blocked`, not a fabricated study. Public challenges remain opt-in human-reviewed work.

## Origin and separation of evidence

This charter was created from an October 21, 2026 user-supplied conversation handoff titled *Grok Science Accountability*. It preserves the user's specific focus on public-facing Grok, Socratic scrutiny, empiricism, balanced political/cultural testing, 10th-Man checking, ECR, repeat tests, and eventual cross-model comparisons. The handoff is **a project proposal, not experimental evidence**. Official X source links above separately support the platform-policy and training-possibility claims.
