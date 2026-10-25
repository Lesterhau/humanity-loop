# Humanity Loop Outcome Tracker

This file tracks external actions whose real-world outcome still needs verification.

Status vocabulary:
- **reported** — issue sent to responsible organization;
- **acknowledged** — recipient confirmed receipt;
- **claimed-resolved** — recipient says it is fixed, but independent verification is incomplete;
- **verified-resolved** — the public outcome was independently confirmed;
- **follow-up-sent** — factual follow-up sent after non-resolution or contradictory evidence;
- **closed-no-fix** — issue is no longer actionable or was rejected with a documented reason.

No item should remain indefinitely in a vague waiting state. Apply `OUTCOME-ESCALATION.md`.

## Active / recently resolved items

### OT-001 — Texas HHS Medicaid Buy-In earned-income premium typo
- Original report: 2026-09-25
- Agency: Texas Health and Human Services — Form and Handbook Unit
- Problem: Appendix XXXI showed an impossible 150%–185% FPL range beginning at “more than $41,995” instead of “more than $1,995.”
- Agency response: 2026-09-30 — “It was corrected.”
- Independent verification: **verified-resolved 2026-09-30**
- Evidence: live Appendix XXXI now shows “More than $1,995 up to and including $2,461.”
- Public source: https://fhb.hhs.texas.gov/handbooks/medicaid-elderly-people-disabilities-handbook/appendix-xxxi-budget-reference-chart
- Win ledger: WIN-001
- Follow-up: none unless regression is detected.

### OT-002 — VA Spanish “current rates” index points to 2019 tables
- Original report: 2026-09-25
- Agency: U.S. Department of Veterans Affairs / Veterans Benefits Administration
- Problem: Spanish “Tasas Actuales de Acceso” links labeled current resolve to legacy pages explicitly marked Effective 12/1/19.
- Agency responses:
  - 2026-09-28 Digital Media: will investigate and work to resolve.
  - 2026-09-28 Web Team: stated the link redirects to the latest rates and the page will eventually redirect to VA.gov.
- Independent verification: **unresolved 2026-09-30** — the Spanish index still links to pages visibly marked Effective 12/1/19 for compensation, DIC, and Parents DIC.
- Status: **follow-up-sent / public correction not yet verified**
- Initial follow-up: sent 2026-09-30 from MOTHER / Humanity Loop to DIGITALMEDIA.VBACO@va.gov and WEBADMIN.VBACO@va.gov.
- **2026-10-20 independent recheck:** Spanish index at https://www.benefits.va.gov/Benefits/espanol/compensation_rates-index.asp still labels Veteran-compensation and DIC links *Tasas Actuales* but their linked page headings show `Effective 12/1/19`. The Parents DIC link now redirects to the general `https://www.va.gov/pension/` page, not directly to its current Parents DIC rates. Modern VA.gov current-rate pages exist. Distinguish partial redirect progress from verified correction.
- **2026-10-20 one bounded material-evidence update sent:** From MOTHER / Humanity Loop to the same VBA Digital Media/WebAdmin contacts, expressly referencing the newly observed Parents DIC routing and giving the direct 2026 Veterans/Survivor/Parents DIC rate URLs. AgentMail thread `3d788187-c352-424a-a47b-686ee014a012`; sent Message-ID `<010001a15b9c2c7d-baeb7202-f9fa-4c63-b595-32ba1a9ae755-000000@email.amazonses.com>`, 2026-10-20T23:18:43.904Z; independent thread readback confirms two project messages total and **zero inbound replies** in that mailbox. See Undermind `/humanity-loop/operations/2026-10-20-execution-ot002-intent.md`.
- **Contact limit:** No further routine contact unless the agency responds or significant new facts justify proportionate escalation. Do not count either message as an outcome.
- Next independent public-link and reply review: **2026-10-27**, then record verified-resolved, bounded escalation, or closure with reason. Owner: Humanity Loop hourly worker/Outcome Tracker; human only if a material decision gate arises.

### OT-003 — Texas WIC fair-hearing PDF says HHS assigns a lawyer
- Original report: 2026-09-25
- Agency: Texas WIC / Texas Health and Human Services
- Problem: public English/Spanish handout says HHS will assign the appellant a lawyer.
- Agency response: 2026-09-28 acknowledgement only.
- Independent verification: **unresolved 2026-09-30** — public PDF still contains the attorney-assignment language.
- Status: **agency clarification received; public PDF unresolved**
- Follow-up: sent 2026-09-30 from MOTHER / Humanity Loop to WICGeneral@hhs.texas.gov and WICsupport@hhs.texas.gov.
- Public source: https://texaswic.cart.com/Shared/PDF-Downloads/13-06-12103.pdf
- **2026-10-23 verified recheck and internal escalation:** Original bilingual PDF still promises an HHS-assigned lawyer; HHSC general Fair and Fraud Hearings FAQ separately says appellant counsel is at the appellant's expense. This warrants program-specific clarification rather than a categorical legal conclusion. One neutral clarification/escalation sent to the HHSC Fair and Fraud Hearings Department (different responsible unit), independently read back in approved AgentMail thread `4a80f3d5-e07d-4646-88c8-a65404adbbb2`; an automated receipt was independently verified. A substantive HHSC Deputy Director response followed at 2026-10-23T20:26:07Z; no public PDF correction yet. Full public-safe intent/evidence/receipt: `runtime/case-steward/ot003-2026-10-23-escalation.md`.
- **2026-10-23 material HHSC response and verified reply:** M. Elizabeth Boyce, HHSC Appeals Division Deputy Director, confirmed that the HHSC-assigned lawyer represents the **agency**, not the appellant, and agreed that the bilingual handout's wording is misleading. She offered to identify the responsible publications contact. Humanity Loop replied once from its project AgentMail inbox accepting that referral offer; the two-message thread was independently read back. Exact internal correspondence IDs and safe evidence are preserved in `runtime/case-steward/ot003-2026-10-23-escalation.md`. **Do not claim a public correction, representation guarantee, or beneficiary impact.**
- **Case Steward owner and review:** Humanity Loop main worker until separate specialist actually verified; review on substantive HHSC response or **2026-11-06**, whichever comes first. Stale threshold **2026-11-13**; decide one proportional next step or close with reason. No more routine follow-ups to the same recipients. Closure requires corrected bilingual handout, official clarification, or documented closure decision.

### OT-004 — Texas WIC conflicting Spanish income limits
- Original report: 2026-09-25
- Agency: Texas WIC / Texas Health and Human Services
- Agency response: 2026-09-28 confirmed the current correct income limits and said the discrepancy could be quickly addressed.
- Status: **acknowledged / current main site corrected, legacy page not verifiable**
- **2026-10-20 independent finding:** The accessible Spanish WIC application page `https://www.texaswic.org/es/solicita-beneficios` and its English counterpart `https://www.texaswic.org/apply` both publish the current 2026–27 income limits, including 1-person gross monthly **$2,461** and 2-person **$3,337**, which match USDA's July 1, 2026 guidelines (`https://www.fna.usda.gov/wic/fr-042926`). Their current paths were fetched directly successfully.
- **Remaining uncertainty:** The older Spanish page `https://www.texaswic.org/es/solicita-beneficios-de-wic/como-iniciar-tu-participacion-en-wic` still appears in the search index with **2024** outdated 1-person **$2,322** and 2-person **$3,152** limits, but the direct live fetch returned HTTP **403 Forbidden**. A search-index snippet is NOT proof that ordinary users can presently see those old figures. Do not count this as verified-resolved or a current public exposure defect until independent human/browser navigation confirms the legacy-page behavior.
- Follow-up: no unverified new agency contact on this observation. Request a documented browser/user-visible navigation or agency confirmation of retirement/correction; recheck Oct 27 or on substantive agency reply.
- Next decision: mark verified-resolved only if the obsolete public entry point is inaccessible to normal users, redirects correctly, or has actually been updated; otherwise make one proportionate factual correction request under governance and outreach limits.

### OT-005 — IRS EITC / translated-page annual-update inconsistencies
- Original report: 2026-09-17/18
- Status: **reported**
- Personal Gmail scan through 2026-09-30 found no substantive agency response.
- Next step: verify live pages and follow `OUTCOME-ESCALATION.md` if stale.

### OT-006 — SSA 2026 Red Book examples using prior-year SSI rate
- Original report: 2026-09-17/18
- Status: **reported**
- Personal Gmail scan through 2026-09-30 found no substantive agency response.
- Next step: verify live pages and follow `OUTCOME-ESCALATION.md` if stale.

### OT-007 — StudentAid.gov aid-offer article annual-update drift
- Original report: 2026-09-18
- Status: **reported**
- Personal Gmail scan through 2026-09-30 found no substantive agency response.
- Next step: verify live page and follow `OUTCOME-ESCALATION.md` if stale.

### OT-008 — Medicare helper / Extra Help threshold drift
- Original report: 2026-09-19
- Status: **reported**
- Personal Gmail scan through 2026-09-30 found no substantive agency response.
- Next step: verify live tool/page and follow `OUTCOME-ESCALATION.md` if stale.

### OT-009 — DOL Fact Sheet #17D content error
- Original report: 2026-09-25
- Status: **reported**
- Personal Gmail scan through 2026-09-30 found no substantive agency response.
- Next step: verify live page and follow `OUTCOME-ESCALATION.md` if stale.

### OT-010 — Clarvia ASBL → NLnet funding connection
- Original Connector action: 2026-09-30
- External project: Clarvia ASBL / Clarvia Graph
- Verified need: grant funding plus technical maturity work including validation/testing/documentation and independent review.
- Matched resource: NLnet Foundation Open Internet Stack funding cycle; next published deadline noted by the Connector as 2026-11-03.
- Action: one targeted email sent from MOTHER / Humanity Loop to Clarvia's public contact address; send/read-after-send verification completed.
- Durable receipt: `runtime/connector/2026-09-30-clarvia-nlnet.json`
- Status: **closed — no verified connection outcome (2026-10-23)**
- Independent AgentMail inbox/thread verification: **2026-10-10 02:45:45Z** — exactly two outbound messages; no Clarvia reply. A single corrective follow-up was sent about NLnet's explicit AI-generated-project/proposal restrictions; Clarvia eligibility remains undetermined. Project inbox thread `84745782-8baa-4911-8d4c-a5576166e9b6`, follow-up message `<010001a123b3c16b-a86cd94c-97ef-40db-95bf-f456cde86b11-000000@email.amazonses.com>`.
- Follow-up receipt: Undermind `/humanity-loop/operations/2026-10-09-ot010-one-followup.md`; **one-follow-up limit EXHAUSTED; do not send another routine contact without material new evidence or recipient opt-in**.
- **2026-10-23 closure check:** Independently re-read project AgentMail thread `84745782-8baa-4911-8d4c-a5576166e9b6`: exactly two outbound messages, latest 2026-10-10, with no inbound recipient reply. The 2026-10-14 stale threshold has passed and the one-follow-up limit is exhausted. Close as **no independently verified downstream value**, not as proof the recipient did nothing. No further routine contact. Reopen only on a substantive unsolicited response or independently verifiable evidence of useful adoption.
- Stale threshold: **2026-10-14** (exceeded; proportionately closed 2026-10-23).
- Success/closure condition: Clarvia confirms the match was useful (for example, application/grant-path use, useful eligibility clarification, or another concrete resource connection) or independently verifiable downstream value is documented.
- Do not count the outbound email itself as a Connector win.

### OT-011 — GestureLabs/A3CP → GitHub Open Source Accessibility community
- Original Connector action: 2026-10-02
- External project: GestureLabs / Ability-Adaptive Augmentative Communication Platform (A3CP)
- Verified need: public project materials explicitly invite developers, researchers, pilot partners, supporters, and collaboration inquiries.
- Matched resource: GitHub's Open Source Accessibility community and the 2026 Open Source Accessibility Summit on 2026-10-19.
- Action: one targeted email sent from Ryan Lester | Humanity Loop to GestureLabs' public collaboration contact; read-after-send verification completed.
- Durable receipt: `runtime/connector/2026-10-02-gesturelabs-github-accessibility.json`
- Status: **closed — no verified connection outcome (2026-10-23)**
- Independent AgentMail inbox/thread verification: **2026-10-10 02:40:01Z** — exactly two outbound messages; no GestureLabs reply. One timely follow-up referenced the October 19 accessibility summit and standing GitHub Open Source Accessibility community. Project inbox thread `625a9116-2af2-47b1-a1b0-25c1e9e16b0b`, follow-up message `<010001a123ae80ca-5e4ab17e-dae2-4820-a451-d099cf99dc84-000000@email.amazonses.com>`.
- Follow-up receipt: Undermind `/humanity-loop/operations/2026-10-09-ot011-followup.md`; **one-follow-up limit EXHAUSTED; do not send another routine contact without material new evidence or recipient opt-in**.
- **2026-10-23 closure check:** Independently re-read project AgentMail thread `625a9116-2af2-47b1-a1b0-25c1e9e16b0b`: exactly two outbound messages, latest 2026-10-10, with no inbound recipient reply. The 2026-10-14 stale threshold has passed and the one-follow-up limit is exhausted. Close as **no independently verified downstream value**, not as proof the recipient did nothing. No further routine contact. Reopen only on a substantive unsolicited response or independently verifiable evidence of useful adoption.
- Stale threshold: **2026-10-14** (exceeded; proportionately closed 2026-10-23).
- Success/closure condition: GestureLabs confirms the community/event connection was useful or independently verifiable participation/collaboration attributable to the connection is documented.
- Do not count the outbound email itself as a Connector win.

### OT-012 — Indonesia: Batin Tikal complaint-link 404 and placeholder public-service page
- **Owner:** Humanity Loop Case Steward lane (main worker interim until independent handoff); institution: Kelurahan Batin Tikal / municipal website maintainer, Pangkalpinang.
- **Original verified finding:** 2026-10-25. Official homepage links `Layanan Pengaduan` to `/pengaduan`, independently returning HTTP 404; `Layanan Kelurahan` links to a page containing only placeholder service information. Generic government email and office address remain publicly listed. No claim all complaint channels are unavailable.
- **Existing institutional oversight:** Ombudsman RI independently reported missing published service standards and a dedicated complaint contact after its 2026-10-20 inspection. Ombudsman receives credit for its own inspection; Humanity Loop's distinct contribution is documenting two exact website observations and notifying the public contact.
- **Status:** **reported** (not acknowledged or resolved).
- **Action:** one neutral Indonesian-language factual report from MOTHER / Humanity Loop to the publicly listed `kel-batintikal@pangkalpinangkota.go.id`, sent **2026-10-25T18:25:01.972Z**. Project AgentMail Message-ID `<010001a1744f1920-d75e9e96-0187-4d4d-8b5f-8b128fa9b848-000000@email.amazonses.com>`, thread `4e6d76dc-cf2e-4d92-9dff-4a4c63b3b76a`. Independent `get_message` readback verified sender, recipient, subject, body and sent label. Recipient receipt/delivery, response and fix are not yet verified.
- **Public evidence:** https://github.com/Lesterhau/humanity-loop/blob/main/research/scout-mesh/2026-10-25-se-asia-id-civic-batin-tikal-complaint-route.md
- **Intent and send receipt:** https://github.com/Lesterhau/humanity-loop/blob/main/runtime/case-steward/ot012-2026-10-25-batin-tikal-intent.md
- **Next review:** **2026-11-01** or a substantive reply; **stale threshold:** 2026-11-08. At most one reasonable follow-up, no hourly recontact. If the address bounces or site is not the maintained official channel, identify the responsible municipal IT contact before any new outreach.
- **Next concrete action:** verify whether the exact advertised complaint URL and service page are corrected or a current official replacement is published; record before/after and actual access separately.
- **Closure:** verified-resolved with independently checked links, verified alternate official service channel, or documented closed-no-fix after proportionate escalation. **No beneficiary effect, correction or institution credit to Humanity Loop claimed yet.**

## Correspondence rule

For Humanity Loop government/public-agency correspondence going forward:
- default outbound sender: **MOTHER <mother.humanityloop@agentmail.to>**;
- do not use Ryan's personal email for new project outreach unless he explicitly requests it;
- Ryan's personal Gmail may be read only for replies to earlier Humanity Loop reports or when separately authorized;
- migrate active threads to MOTHER with a transparent continuity note rather than impersonating Ryan;
- independently verify any claimed correction before changing an item to `verified-resolved` or adding it to `WIN-LEDGER.md`.
