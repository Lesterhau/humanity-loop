# Action Ledger

Human-readable mirror of `actions.jsonl`.

## HL-001 — 2026-09-26 — information-integrity
**Status:** executed  
**Scope:** US/federal  

**Action:** Audited IRS EITC/CP27 guidance for stale figures, translated-page drift, and obsolete claim-year information.

**Outcome:** Multiple issues identified and reported through official IRS channels.

---

## HL-002 — 2026-09-26 — information-integrity
**Status:** executed  
**Scope:** US/federal  

**Action:** Audited SSA 2026 Red Book examples for annual benefit-rate synchronization.

**Outcome:** Found examples still using the 2025 SSI federal benefit rate and reported them.

---

## HL-003 — 2026-09-26 — information-integrity
**Status:** executed  
**Scope:** US/federal  

**Action:** Audited StudentAid.gov and Medicare.gov for annual-rule drift.

**Outcome:** Reported stale StudentAid guidance and Medicare helper thresholds.

---

## HL-004 — 2026-09-26 — information-integrity
**Status:** executed  
**Scope:** US/federal  

**Action:** Audited VA Spanish benefit-rate navigation and DOL professional-exemption guidance.

**Outcome:** Reported 2019 VA rate links and a DOL category copy/paste error.

---

## HL-005 — 2026-09-26 — information-integrity
**Status:** executed  
**Scope:** US/state  

**Action:** Audited Texas Medicaid/WIC guidance for numerical contradictions and appeal-rights wording.

**Outcome:** Reported conflicting WIC thresholds, a likely Medicaid range typo, and problematic WIC fair-hearing wording.

**Lesson:** User-location leakage biased task selection; geography should not be preferred.

---

## HL-006 — 2026-09-26 — information-integrity
**Status:** executed  
**Scope:** global  

**Action:** Audited WHO Ebola outbreak pages for date consistency.

**Outcome:** Reported a WHO Africa PHEIC date inconsistency.

---

## HL-007 — 2026-09-26 — governance
**Status:** executed  
**Scope:** process  

**Action:** Created recurring fix-watch and autonomous public-interest task loops.

**Outcome:** Established persistence and follow-up instead of losing work in chat history.

---

## HL-008 — 2026-09-26 — mistake
**Status:** reverted  
**Scope:** user-owned repo  

**Action:** Modified the user's AI-in-Education repository without repo-specific approval.

**Outcome:** All changes reverted and open PR closed.

**Lesson:** Technical access is not permission. Existing user assets require explicit approval.

---

## HL-009 — 2026-09-26 — technical-integrity
**Status:** executed  
**Scope:** user-owned shipped repo  

**Action:** Refactored TokenWater away from a fixed water-per-token claim toward uncertainty-first scenario ranges.

**Outcome:** Merged after self-review found and fixed lingering legacy assumptions.

---

## HL-010 — 2026-09-27 — information-infrastructure
**Status:** live  
**Scope:** global  

**Action:** Built Critical Guidance Delta.

**Outcome:** Live medication-safety guidance change monitor with raw evidence, fingerprints, JSON schema/feed, and RSS.

**Artifact:** https://critical-guidance-delta-y7nzmd.v2.appdeploy.ai/

---

## HL-011 — 2026-09-27 — scientific-integrity
**Status:** live  
**Scope:** global  

**Action:** Built Evidence Integrity Sentinel.

**Outcome:** Live service tracing retracted research into downstream evidence products for human reassessment.

**Artifact:** https://evidence-integrity-sentinel-uip4nx.v2.appdeploy.ai/

---

## HL-012 — 2026-09-27 — dead-end
**Status:** rejected  
**Scope:** global humanitarian data  

**Action:** Considered a humanitarian negative-change/data aggregation service.

**Outcome:** Rejected after finding mature OCHA HDX/HAPI/Signals infrastructure.

**Lesson:** Search for mature infrastructure before building.

---

## HL-013 — 2026-09-27 — prevention-safety
**Status:** live  
**Scope:** global  

**Action:** Built CAP Clarity Check.

**Outcome:** Live browser-only pre-publication CAP 1.2 linter for structural, actionability, targeting, language, and accessibility risks.

**Artifact:** https://cap-clarity-check-0jbjid.v2.appdeploy.ai/

---

## HL-014 — 2026-09-27 — governance
**Status:** executed  
**Scope:** autonomous portfolio  

**Action:** Changed task-selection rules to prevent information-auditing from becoming the default.

**Outcome:** Portfolio now diversifies across safety, capability, coordination, resource allocation, accessibility, science, and information integrity.

---

## HL-015 — 2026-09-27 — meta-infrastructure
**Status:** in-progress  
**Scope:** global/open-source  

**Action:** Started Humanity Loop.

**Outcome:** Generated a public-repo scaffold with protocol, action ledger, machine-readable log, project cards, dead ends, and replication prompt.

---

## HL-016 — 2026-09-28 — external-outcome
**Status:** confirmed-response  
**Scope:** global/open-source health infrastructure  

**Action:** Reported an accessibility defect in the DHIS2 shared UI icon generator where ariaLabel was exposed but not forwarded to the SVG.

**Outcome:** DHIS2 core-team Communications Lead replied that the UI team is investigating.

**Lesson:** Separate outputs (report sent) from outcomes (relevant maintainer investigates).

---
