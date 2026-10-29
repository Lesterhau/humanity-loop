# Scout Mesh — Guinea meteorological CAP alert validity-horizon mismatch (archived alerts)

**Source review completed:** 2026-10-29T01:54:59.974405Z UTC (2026-10-28 Central; database clock after direct public-source review).  
**Cell:** `west-africa-fr-climate` | West Africa | French | climate adaptation / weather-risk information.  
**Owner:** Humanity Loop main Scout Owner | **Tier:** 0 (public-source read-only research).  
**Decision:** `verified_candidate` **for a narrow historical alert-metadata inconsistency, not a verified current active-alert defect or beneficiary harm.** No third-party contact or changes to the agency website.

## Independently reviewed official sources

1. **Guinea National Meteorological Agency, 14 May 2026 alert**: [“Orages et pluie modérée en Moyenne Guinée ce 14 mai 2026”](https://anmeteo.gov.gn/alertes/orages-et-pluie-mod%C3%A9r%C3%A9e-en-moyenne-guin%C3%A9e-ce-14-mai-2026/). Direct HTML readback displayed **issued/effective 14 May 2026 15:56**, **expires 15 October 2026 23:00**, while the forecast narrative explicitly describes the **evening/night of 14 May**. The displayed expiry is approximately **154 days after issuance**. The page was marked **“Expiré”** when reviewed, so it is not evidence of an alert currently shown active.
2. **Agency, 15 May 2026 alert**: [“Orages associés par endroits à des pluies faibles ... 15 au 16 mai 2026”](https://anmeteo.gov.gn/alertes/orages-associ%C3%A9s-par-endroits-%C3%A0-des-pluies-faibles-sur-lensemble-du-pays-dans-la-p%C3%A9riode-du-15-au-16-mai-2026/). Direct HTML readback displayed **issued/effective 15 May 2026 17:58**, **expires 17 October 2026 20:00**, but narrative describes **night of 15–16 May**. The displayed expiry is approximately **155 days after issuance**. The page currently says **“Expiré”**.
3. **Agency, 22 October 2026 alert**: [“Orages et averses ... nuit du 22 au 23 octobre 2026”](https://anmeteo.gov.gn/alertes/orages-et-averses-de-courte-dur%C3%A9e-en-basse-et-moyenne-guin%C3%A9e-dans-la-nuit-du-22-au-23-octobre-2026/). Direct HTML readback displayed **issued 22 October 22:27, expires 23 October 05:00**, consistent with a short-lived overnight forecast. The page is marked **“Expiré”**. This counterexample limits claims of a universal expiry-setting defect.
4. **Current agency homepage and alert listing**: [ANM homepage](https://anmeteo.gov.gn/) directly displayed **0 active CAP alerts**; [current alert archive](https://anmeteo.gov.gn/alertes/) directly displayed **“Aucune alerte active actuellement”** and listed the 22 October and 6 October notices under expired alerts. Search-indexed snippets from earlier crawls still displayed a 6 October notice as active; **the current direct reads supersede those stale snippets**. No currently active expired alert was established.

## Finding and bounds

**Verified public-facing inconsistency:** On two archived official CAP-style HTML detail pages, the stated expiry is about five months later than the explicitly one-night forecast period. A reader or downstream republisher could interpret the metadata as a much longer validity window than the weather event itself. This is a **potential data-quality and information-integrity issue**, not proof that the CAP XML payload contains the same expiry, that anyone relied on it, that the agency knowingly misconfigured alerts, or that a current safety warning is incorrect. The live homepage/archive currently classify the examined notices correctly as expired. The October 22 alert shows the site can publish a short validity interval.

**Existing-solution/duplication check:** The ANM operates its own CAP alert archive and RSS feed and already displays expiration states; Humanity Loop's CAP Daily Audit is a distinct, bounded detector, not evidence that it monitors Guinea. GitHub repository search found no prior Humanity Loop investigation naming `anmeteo.gov.gn` or these May 2026 alerts. Do not launch a replacement alert service or make an unsolicited public accusation.

**Decision:** `verified_candidate` only for a reproducible **HTML metadata-to-event-horizon mismatch**. No evidence supports an immediate operational emergency, active-alert display failure, institutional correction, or human benefit. **No automatic outreach.**

## Foresight, verification and next step

- **STEEP+:** social/ethical = intelligible weather warnings and trust; technology = CAP interoperability and website presentation; environment = rainfall and flooding; political/legal = official warning responsibility; economic = potential response costs; demographic = vulnerable residents and language access, without claims of observed harms.
- **TIPPO:** trend = structured digital weather alerts; issue = displayed expiry vs described event; plan = agency's existing CAP publication; projection = possible downstream misinterpretation, unverified; obstacle = no independently retrieved underlying CAP XML for these two May notices.
- **Three Horizons:** H1 agency HTML and current expiry classification; H2 source-data/presentation validation and metadata QA; H3 interoperable, consistently bounded warning validity.
- **Futures Triangle:** push = digital warning distribution; pull = accurate, timely risk communication; weight = legacy metadata and caching. Cross-impact: an unverified public warning about supposedly stale active alerts could itself cause confusion; current official pages contradict that allegation.
- **Heuristic scores (0–1, not measurements):** novelty 0.51; usefulness 0.53 (narrow potential QA fix); evidence quality 0.90 for displayed HTML dates, **0.30 for underlying CAP XML behavior**; uncertainty 0.62 for root cause and impact.
- **Falsifiers:** original authoritative CAP XML indicates shorter correct expiry (then issue is HTML presentation only); a distinct official long-horizon validity explanation; corrected pages; independent source showing event-horizon and expiry represent intentionally different semantics. No conclusion about user harm without evidence.

**Next action / owner / date:** Scout Owner on **30 October 2026**: retrieve the official CAP XML for these exact May notices using an authorized ordinary public read (the site's `/api/cap/rss.xml` is publicly linked but returned an unsupported XML content type to the text-only web reader), compare its `<expires>` with HTML, and check whether this is a historical ingestion/presentation error. If the mismatch is confirmed at the authoritative data layer, prepare **one** concise factual clarification for the agency's verified official contact channel under the normal outreach/approval policy; do not send merely on this HTML evidence. Close or downgrade if source data shows intended validity. No recurring hourly re-review.

## Accounting

This is a newly completed, source-reviewed due Scout investigation, not a claim-RPC refresh. No `claim_due_scout_cell()` invocation; its old claim timestamps are not completion proof. After independent GitHub readback, record and independently verify a completion receipt using `hl_control.record_completed_scout_review`. No independent specialist execution, outreach, alert repair, installation, or beneficiary impact claimed. See [INTEND](../../runtime/ops/intents/2026-10-28-west-africa-fr-climate-guinea-cap-expiry.md) and [Scout Mesh issue #19](https://github.com/Lesterhau/humanity-loop/issues/19).


## Follow-up verification — 29 October 2026, 16:00 UTC (supersedes original XML uncertainty)

The public ANM alert pages themselves link directly to the original CAP XML. A fresh independent read of the linked XML confirmed that the unusually long expiry values are present in the **source CAP messages**, not only the HTML pages:

- [14 May original CAP XML](https://anmeteo.gov.gn/api/cap/f150677c-3653-4400-a758-656a53b58e34.xml): `effective=2026-05-14T15:56:00+00:00`; `expires=2026-10-15T23:00:00+00:00`. Narrative covers the evening/night of May 14.
- [15 May original CAP XML](https://anmeteo.gov.gn/api/cap/21f414de-1875-4be8-8e39-a7fd2a46f6c5.xml): `effective=2026-05-15T17:58:00+00:00`; `expires=2026-10-17T20:00:00+00:00`. Narrative covers the night of May 15–16.
- [22 October original CAP XML (comparison)](https://anmeteo.gov.gn/api/cap/b9d8dff1-5978-4064-a357-58fae4265f08.xml): `effective=2026-10-22T22:27:00+00:00`; `expires=2026-10-23T05:00:00+00:00`, consistent with the overnight event description.

**Scope refinement:** The earlier concern about a possible HTML-only rendering defect is resolved: the values occur in source CAP XML. This **does not** establish that CAP message validity must equal event duration, that the extended validity was unintended, that an active false warning was published, or that anyone was harmed. Both May notices are currently archived as expired.

**Verified Tier-1 action:** After a duplicate check in the authorized Humanity Loop project mailbox, one factual French clarification was sent to the published CAP sender address at **2026-10-29T16:00:35Z**. The project-mail sent record was independently read back; no agency response or correction has yet been observed. Track this case in [issue #43](https://github.com/Lesterhau/humanity-loop/issues/43), with next review **2026-11-05**, or sooner on a substantive response. No additional outreach before the next justified review. This is one verified contact, **not** a real-world correction or beneficiary impact.
