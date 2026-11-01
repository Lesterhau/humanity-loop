# South Asia education Scout — LUMS Punjab school climate-exposure atlas: internally inconsistent public summary

**Cell:** `south-asia-en-education` | South Asia | English | education / skills / learning systems  
**Review:** 2026-11-01 UTC | **Owner:** Humanity Loop main Scout coordinator  
**Decision:** `verified_candidate` — reproducible inconsistency in a public research-page summary, **not** a demonstrated error in underlying school-level data, school prioritization, public policy, or student outcomes.  
**Status:** Research only; no contact, code patch, institutional acknowledgment, or correction. Independent ordinary-browser and underlying-data validation remain outstanding.

## Primary-source observation

Source: [Lahore University of Management Sciences (LUMS), Centre for Urban Informatics, Technology, and Policy (CITY), *Understanding Climate-Related Educational Disruptions in Pakistan*](https://city.lums.edu.pk/what-we-do/city-research/dare-rc/), original publicly available research project and Punjab School Climate-Exposure Atlas page. Reviewed 2026-11-01 UTC.

The page describes an August 2026 data snapshot for 52,196 tracked schools in Punjab. It displays **103** schools at Priority 1–2 for **both** heatwave and flooding in the top summary, atlas summary and combined-view KPI. But three narrative passages refer to **117** such schools:

1. **District concentration:** “Gujrat, Sialkot, Sheikhupura, and Gujranwala contain 84 of the 117 schools at Priority 1–2 for both hazards (81.6%).” Arithmetic check: **84/117 = 71.8%**, whereas **84/103 = 81.6%** when rounded to one decimal. Thus the published 81.6% aligns with the displayed 103 denominator, not the written 117. Whether 84 is itself the correct district count requires dataset verification.
2. **Explanatory copy:** The page twice says the chart shows **117** compounding Priority 1–2 schools, while the current displayed both-hazards KPI is **103**. The prose and KPI may reflect different versions of the dataset; the page does not disclose that distinction.
3. **Five largest events:** The page says “Four of the five largest recorded rainfall events by exposed schools occurred in 2025.” Its own table of the five largest events lists **2025_R08, 2021_R06, 2025_R02, 2025_R03, 2023_R05**. That is **three**, not four, events in 2025. The event table may have been refreshed without corresponding prose.

**Reproduction:** Open the LUMS source URL; compare “Early results · Punjab” → “The highest-priority schools cluster in the north-east” and “Evidence behind the findings” against “What the snapshot shows” / “Both hazards at P1–2”; then compare “Recent rainfall events were especially large” against the “46-event timeline” top-five table. The page is a primary institutional source; the read was via a public web retrieval, not an independently operated ordinary browser.

## Significance and uncertainty

The project explicitly aims to support climate-resilient education planning and locally targeted school-priority analysis. The public inconsistencies could confuse a reader or downstream reuser about the count and concentration of compound-exposure schools and the timing of the largest rainfall events. **No evidence shows a government, school or funder relied on the stale prose, or that any child experienced harm.** The current atlas calculation, underlying data, chart rendering, and denominator provenance were not independently audited. The most economical hypothesis is stale explanatory text after a data refresh, but that is **not verified**.

The [UNICEF September 2026 climate-related school disruption analysis reproduced by the United Nations in Pakistan](https://pakistan.un.org/en/322603-media-update-united-nations-pakistan-10-september-2026) documents education-continuity risks and describes practical resilience approaches. This contextualizes why accurate school-risk communication matters; it does **not** validate the LUMS counts or imply a new crisis caused by the page.

## Novelty, alternatives and falsification

- **Deduplication:** GitHub issue searches for `LUMS`, `Punjab school climate` and the exact “84 of the 117” phrase in `Lesterhau/humanity-loop` returned no matching issue on 2026-11-01. The prior South Asia cell receipt concerned Bangladesh differentiated learning; another recent cell concerned Indian scholarship links. This candidate is distinct from both.
- **Existing solution:** The institution already operates the atlas and has the original data, methodology and maintainers. A narrowly scoped text/denominator reconciliation by that team is preferable to a new dashboard or parallel data product.
- **Suggested responsible action, not yet taken:** Ask the LUMS CITY project team privately to confirm the authoritative snapshot and denominator, then align district-concentration copy and the top-five-event narrative with its source data. Credit LUMS for any eventual correction. No direct email or issue was sent.
- **Falsifiers:** A published explanation that 103 and 117 refer to different cohorts/time windows, or an updated table showing four of the five events in 2025, would materially change the conclusion. A new corrected page would establish a correction only if before/after are independently documented. The underlying count may remain 103, 117 or another value after proper verification.
- **Next review:** 2026-11-08 UTC, or sooner on substantive institutional response/new version. First seek an ordinary-browser read and verify a legitimate maintainer reporting channel; send at most one respectful factual private report if appropriate. No allegation of research misconduct or data manipulation.

## STEEP+, foresight and proportionality

**Social:** School safety and learning continuity. **Technological:** Data-to-narrative synchronization and transparent snapshot versions. **Economic:** Better targeting of scarce school resilience resources, potential cost of misinterpretation unmeasured. **Environmental:** Flood/heat co-exposure. **Political/institutional:** Local government and research planning interfaces. **Ethical:** Avoid exaggerating inconsistencies into claims of danger, misconduct or faulty school-level risk labels.

**Three Horizons:** H1 static text around a changing risk atlas; H2 consistent snapshot-driven public metrics with date/version labels; H3 independently reproducible, locally governed risk planning. **Futures Triangle:** push = recurring climate shocks and richer exposure datasets; pull = trustworthy risk-informed school decisions; weight = uneven monitoring data and communication drift. **Cross-impact:** inaccurate public summaries can weaken trust and misallocate attention even when underlying analytics are correct; there is no evidence this has happened here. **TIPPO / alternatives:** smallest leverage point is a maintained text-to-data check, not autonomous school intervention.

## Outcome accounting

**One source-reviewed candidate**; zero independently confirmed underlying data defects, public corrections, outside contributors, external contacts, deployments, school interventions or beneficiary outcomes. No external party has credited Humanity Loop. This report is a reversible research artifact only.

**Audit:** [Pre-write INTEND](../../runtime/ops/intents/2026-11-01-south-asia-lums-climate-atlas-consistency.md). Private completion receipt should be recorded **only after independent GitHub readback**; legacy claim timestamps do not prove a completed scan.

## 2026-11-01 responsible private notification (post-research)

Fresh independent public web retrieval on November 1 still displayed the three text/table discrepancies. CITY's official contact page lists its institutional address. An authorized project-inbox search found no previous LUMS/DARE-RC correspondence. A narrowly scoped, non-accusatory editorial inquiry was **sent at 2026-11-01T05:48:03.308Z** from Humanity Loop's AgentMail project inbox to CITY, asking the team to confirm the authoritative school count and reconcile the rainfall-event description. The sent message was independently read back with matching recipient, subject and content; **delivery, human acknowledgment and any correction remain unverified**. Local ordinary-browser Chromium verification timed out; the direct public web retrieval is evidence of the page's textual content, not of GUI rendering or underlying data validity.

**Receipt:** [outreach INTEND and verified send record](../../runtime/outreach/2026-11-01-lums-climate-atlas-editorial-intent.md). **Next review:** November 8 UTC or substantive reply/new public version. No automated follow-up, no beneficiary outcome, and no causal attribution claimed.
