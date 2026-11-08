# NWS CAP audit — fail-visible coverage candidate (review-only)

**Date:** 2026-11-08 UTC. **Run:** HL-20261108-CAP-FAILVISIBLE-01. **Mode:** original hourly coordinator, single-model role-separated offline fallback; **not** eight independent LLMs. **Tier:** 0 (public-source evidence and isolated local tests). **Status:** completed as a review-only artifact, NOT deployed or accepted in production.

## External public-interest rationale and primary evidence

The U.S. National Weather Service operates the official alerts API for watches, warnings, advisories and other CAP messages. Its [Alerts Web Service guidance](https://www.weather.gov/documentation/services-web-alerts) describes API access, rate limits, and machine-readable alert distribution. This work improves the honesty of Humanity Loop's independent inspection of that public emergency-information feed; it does **not** identify an error in NWS warnings or prove missed alerts.

Exact repository source inspected via authenticated GitHub connector:
- [scripts/cap_daily_audit.py](https://github.com/Lesterhau/humanity-loop/blob/main/scripts/cap_daily_audit.py), blob `ffa41d4d6461ee2451b404297699d3bce056b2fd`.
- [scripts/test_cap_daily_audit.py](https://github.com/Lesterhau/humanity-loop/blob/main/scripts/test_cap_daily_audit.py), blob `b85e2443f270912f68af8fab05580ec144c69b79`.
- [Previous characterization](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/foundry-fallback/2026-11-08-cap-audit-coverage-failopen-receipt.md) and [issue #13](https://github.com/Lesterhau/humanity-loop/issues/13).
- The [2026-11-08 19:52:05Z CAP receipt](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/cap-daily-audit/latest.json) says `alertsChecked=250`, `findingsCount=12`. It does not reveal the upstream feed's actual returned cardinality.

## Concrete, reproducible build

- [Proposed unified diff, NOT applied to production](2026-11-08-cap-audit-failvisible-candidate.patch), Git blob `9e15ff0a6bc7621638d4b1cad1a5490601f799c2`.
- [13 new synthetic regression tests](test_2026-11-08-cap-audit-failvisible-candidate.py), Git blob `272c37bfa1a2ca0d15354056441bf6493a6c2150`.

Local isolated verification used exact copies of both GitHub production files; their locally computed Git blob SHAs matched the two source SHAs above. The unified diff was checked with `git apply --check`, applied to a separate copy, and the patched-file SHA matched the directly edited candidate. Tests then ran against the **complete reconstructed original module plus candidate patch**, not merely an extracted fetch function.

**Observed tests:** existing upstream-local suite **8/8 PASS**, new candidate tests **13/13 PASS**, 21/21 combined. The prior 5/5 characterization was separately reproduced against the exact original module. No network was available to the isolated test container, and no live NWS API requests were made.

The candidate keeps the old list-returning fetch signature for callers but makes the scheduled `main()` use a coverage-aware fetch. It adds `sourceRecordsReturned`, `recordsNotInspected`, `recordsBeyondLimit`, `invalidSourceRecords`, `hasNextPage`, and `coverageStatus` to the durable JSON. Missing/null `features` now raises instead of silently reporting zero alerts. A 251-record response reports **partial** coverage; malformed records and explicit `pagination.next` are also disclosed. It preserves the 250-alert inspection cap and does not add requests. It separately counts findings omitted by the 400-finding limit. Existing `schemaVersion=1`, `alertsChecked`, `findingsCount`, `bySeverity` and `findings` remain present. Partial runs print a GitHub Actions warning while returning success so the existing workflow can still commit a durable partial receipt.

**Reproduction from repo root, in a temporary checkout only:**

```bash
git apply --check runtime/foundry-fallback/2026-11-08-cap-audit-failvisible-candidate.patch
git apply runtime/foundry-fallback/2026-11-08-cap-audit-failvisible-candidate.patch
PYTHONPATH=scripts python -m unittest -v scripts/test_cap_daily_audit.py
python -m unittest -v runtime/foundry-fallback/test_2026-11-08-cap-audit-failvisible-candidate.py
```

Do **not** apply this to production without review and authorization.

## Eight-role control sequence (one model, no independent multi-agent verification)

1. **Scout:** Emergency-alert audit completeness is more material than another superficial site check.
2. **Verifier:** Exact source and existing tests SHA-matched; NWS is the primary source. No live alert loss established.
3. **Project Manager:** Preserve existing source request frequency, output schema and test-message handling; expose coverage uncertainty.
4. **Builder:** Produced a directly applicable 106-line review-only diff plus 13 executable tests; tested with complete module.
5. **10th Man:** `response_complete` means complete *for this response*, not the whole national feed. Unrecognized pagination formats or downstream consumers may remain; GitHub workflow success can still coexist with a `partial` receipt. These require separate integration review.
6. **Safety Governor:** GO for offline proposal only; HOLD for live detector modification, upstream agency escalation, extra NWS requests or cron changes.
7. **Revision:** Keep bounded fetch, fail visibly on invalid response shape, preserve old fields and add explicit partial counters; no automatic pagination or silent full-coverage claims.
8. **Outcome Tracker:** Artifact and local tests verified; production effect, real-world alert count, downstream schema compatibility and any public-benefit outcome **unverified**.

## Next unchecked acceptance gates

Review this diff against current head and all consumers of CAP JSON, including workflow receipt verification, UI and alert count labels. Test synthetic partial cases in the actual GitHub Actions workflow on a non-production branch, ensuring partial receipts persist and surface a visible warning; validate any NWS pagination contract without increasing rate. Only after review and separate authorized release should production `scripts/cap_daily_audit.py` be changed. Keep existing native CAP and GitHub schedules unchanged; #13 remains open.

**Spend and external effects:** 0 AppDeploy model calls, 0 deployments, 0 new schedulers, 0 NWS HTTP requests, 0 external outreach, 0 real users or agency outcomes. Advisory inbox: no private Claude/GPT/Gemini files read; no new commit metadata verified.
