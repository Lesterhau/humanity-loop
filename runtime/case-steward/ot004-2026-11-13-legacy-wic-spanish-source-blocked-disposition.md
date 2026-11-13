# OT-004 — Texas WIC Spanish legacy income page: November 13 source-blocked disposition

**Review date:** 2026-11-13 UTC. **Case owner:** Humanity Loop original hourly coordinator, Case Steward lane. **Institution:** Texas Health and Human Services / Texas WIC. **Disposition:** close the repetitive routine source-check lane as **blocked / not independently resolved**; retain one optional consented ordinary-browser observation in [issue #46](https://github.com/Lesterhau/humanity-loop/issues/46). **No new agency contact or publication.**

## Primary-source observations

1. [Current official Spanish application page](https://www.texaswic.org/es/solicita-beneficios), freshly retrieved by public web reader on November 13 (reader reports crawl on November 12), displays **2026–27 gross monthly ceilings $2,461 for household size 1 and $3,337 for size 2**; household sizes 3–6 are $4,212, $5,088, $5,964, $6,839. It offers online and telephone application routes and was last updated November 5, 2026 according to its footer.
2. [Current official English application page](https://www.texaswic.org/apply), retrieved in the same review, shows matching amounts.
3. [USDA's 2026–27 WIC income eligibility notice](https://www.fna.usda.gov/wic/fr-042926), published April 29, 2026 and effective July 1, 2026–June 30, 2027, independently lists the same maximum 185%-poverty monthly figures for the contiguous states.
4. **Exact legacy entry point:** https://www.texaswic.org/es/solicita-beneficios-de-wic/como-iniciar-tu-participacion-en-wic . A fresh direct public web-reader open on November 13 returned **HTTP 403**. This is a limitation of that access route; it does not prove ordinary visitors see a 403, nor that the page is corrected, redirected or retired. Search engine retrieval of the legacy URL produced an indexed copy marked crawled **last month**, still showing the superseded **$2,322 (size 1) / $3,152 (size 2)** figures. That older crawl does **not** prove those amounts are currently visible to normal users.
5. The current Spanish application page contains a current application link and current income figures; no direct link to the legacy path was observed in the retrieved current-page text. This does not rule out external referrals or other site links.

## Decision and safe action

The main application route is verified current and usable in the public reader. The narrower question—whether a real visitor can still see outdated thresholds at the exact legacy URL—remains **unverified after repeated 403s**. Continuing the same automated fetch every few days has low expected value. Close **routine hourly/periodic rechecks** of this URL as *source-blocked*, **not** as an agency correction or confirmed defect; do not count a new win, reported correction or beneficiary outcome. Preserve the one-shot external volunteer test in #46 (public ordinary browser only, exact URL, UTC timestamp, visible page/redirect/status, redacted evidence, consent and independent review). Reopen OT-004 only on a genuine human browser observation, agency confirmation, or materially changed public-source access; otherwise select a different due case.

**Safe applicant-facing draft (UNSENT):** “Para consultar los requisitos de ingresos vigentes de WIC en Texas, use la página oficial de solicitud: https://www.texaswic.org/es/solicita-beneficios . La elegibilidad final se determina mediante el programa WIC; las cifras de páginas archivadas o antiguas pueden no estar actualizadas.”

## Accounting

- External action: one bounded primary-source re-verification and case disposition; **not** an agency repair, external contact, accepted volunteer submission, completed Scout Mesh cell or direct beneficiary impact.
- No form submission, social publication, external outreach, Foundry/AppDeploy model use, deployment, production mutation, payment or schedule change.
- Next unchecked independent step: #46 one-time normal-user browser observation if a consenting contributor is available; otherwise no recurring recheck of this exact 403 source.
