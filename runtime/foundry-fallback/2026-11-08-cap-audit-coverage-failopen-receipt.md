# NWS CAP audit — bounded coverage and fail-open response-shape regression

**Observed:** 2026-11-08 UTC. **Scope:** one read-only public-safety data-integrity build/verification step by the original Humanity Loop hourly coordinator. Single-model role-separated fallback, **not** eight independent models. No external agency outreach, NWS alert mutation, production detector modification, live alert API request, AppDeploy AI, deployment, or spending.

## Primary-source and project evidence

- [NWS official API documentation](https://www.weather.gov/documentation/services-web-api): the NWS alerts API is an official source of active watches/warnings/advisories; it is a public, rate-limited service. The documentation does not guarantee that Humanity Loop's client samples every alert.
- [Current Humanity Loop CAP audit source](https://github.com/Lesterhau/humanity-loop/blob/main/scripts/cap_daily_audit.py), blob `ffa41d4d6461ee2451b404297699d3bce056b2fd`: `fetch_active_alerts()` obtains the JSON `features` array, then returns only `features[:MAX_ALERTS]` with `MAX_ALERTS=250`. Missing or null `features` becomes `[]`; non-object records are filtered out without a count. `build_report()` reports `alertsChecked=len(features)`, without total source-record count, truncated/partial-coverage flag, or invalid-record count.
- [November 8 canonical CAP receipt](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/cap-daily-audit/latest.json), observed run `2026-11-08T19:52:05.822130Z`: `alertsChecked=250`, `findingsCount=12`. **Exactly 250 checked does not establish the live upstream feed contained only 250 records.** The upstream live count was not independently measured here.

## Distinct executable artifact and observed result

[New offline regression characterization](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/foundry-fallback/test_2026-11-08-cap-audit-completeness.py), blob `a097941e22f2b159f92ad951552b8c84a8f1c066`, independently read back after commit `ced88f8a61ccf55bf80526d9a952d9df75b234b6`.

Five tests characterize actual source-level behaviors:
1. A **synthetic** response containing 251 valid features returns only 250; the last is silently omitted.
2. `features: null` is treated as a successful empty result.
3. An absent `features` key is treated as a successful empty result.
4. Non-object feature entries are dropped without recording their count.
5. A non-list `features` value correctly raises a visible error.

**Local result:** 5/5 PASS, 0.003 s, against a local exact-function excerpt reconstructed from the GitHub-fetched production function. The new committed test imports the actual `scripts/cap_daily_audit.py` when run from the repository. **It has not yet been executed in the repository's own CI/environment**, and the local excerpt is not a complete checkout. No actual NWS alert loss or public harm is established.

## Proposed narrow, reversible correction (NOT deployed)

- Preserve a `sourceRecordsReturned` count before the cap and `alertsChecked` afterward; mark `coverageStatus=partial` and `recordsNotInspected` whenever the source array exceeds the chosen limit. Never label a partial scan complete.
- Treat missing/null `features` as invalid response shape unless explicitly supported by the API contract; fail visibly, rather than producing a misleading zero-alert success.
- Count invalid feature records and fail visibly or mark partial, rather than silently discarding them.
- Check the NWS API's actual paging/response behavior and rate limits before designing any full-coverage fetch; avoid unbounded requests. Preserve prior output schema consumers and use a reviewed, rollback-ready change. Add tests for source error and over-limit findings.
- Keep existing scheduled CAP detector and native CAP app unchanged until a separately reviewed patch, successful CI, and coverage comparison. No shutdown or escalation to NWS is justified by this synthetic test alone.

## Eight-role review (one model, not independent validation)

1. **Scout:** Prioritize emergency-message completeness over another cosmetic site audit.
2. **Verifier:** Exact production source and Nov 8 receipt inspected; NWS is the authoritative data provider. Live upstream cardinality remains unknown.
3. **PM:** Produce one bounded, reproducible regression artifact; no production mutation.
4. **Builder:** Wrote and read back a standalone test module; local exact-function characterization 5/5 PASS.
5. **10th Man:** A deliberate 250-record sample is not inherently wrong; the defect is failing to disclose sample coverage. Real API response size and paging must be verified before any all-alert claim.
6. **Safety:** Synthetic inputs only; no alerts, devices, user data, agency systems, AppDeploy or deployed jobs touched.
7. **Revision:** Recommend explicit partial/fail-visible status rather than an unbounded live API crawl or automatic scheduler change.
8. **Outcome:** Confirmed local completeness-reporting weakness and reproducible test artifact; **not** an NWS defect, missed warning, upstream acceptance, agency correction, or beneficiary impact.

**Next unchecked step:** Run the committed test against the actual repository module in a normal isolated checkout/CI, then prepare a small reviewed detector patch that emits explicit partial/incomplete coverage without increasing NWS request frequency. Keep issue #13 open. **Advisory inbox:** no private Claude/GPT/Gemini files read; no new commit metadata checked.
