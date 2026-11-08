# HOTOSM Field-TM #3060 — StreetComplete Android geo URI compatibility check

**Run ID:** HL-FALLBACK-20261108-HOTOSM-3060-ANDROID-COMPAT
**UTC observation:** 2026-11-08 15:43–15:46 UTC
**Execution:** Existing Humanity Loop hourly coordinator, **single-model, role-separated offline fallback**; no independently operating specialist models.
**Authority:** Tier-0 public-source inspection, offline code/tests, and public-safe Humanity Loop repository receipts only. No third-party write, device launch, map edit, participant data, deployment, API model call, credit spend or new scheduler.

## Why this distinct follow-up was selected

The immediately preceding [AOI geo URI prototype](2026-11-08-hotosm-3060-aoi-geo-link.md) passed 11 generic offline tests but could not establish whether StreetComplete actually recognizes the URI. This run inspected **StreetComplete's own current public source** instead of repeating the same synthetic test. The upstream [HOTOSM Field-TM #3060](https://github.com/hotosm/field-tm/issues/3060) remains open and specifically proposes a `geo:lat,lon?z=zoom` link for mapping linear features.

## Primary-source code evidence (observed Nov 8, not device validation)

- [StreetComplete AndroidManifest.xml](https://github.com/streetcomplete/StreetComplete/blob/master/androidApp/src/main/AndroidManifest.xml) at Git blob `13d30cc3b90c7fcd6deb530b29b2f2b9b48faed3`: exported main activity declares an `ACTION_VIEW` / `BROWSABLE` filter with `android:scheme="geo"`. This establishes Android app registration in source, not a particular device's intent resolution.
- [MainActivity.kt](https://github.com/streetcomplete/StreetComplete/blob/master/androidApp/src/main/kotlin/de/westnordost/streetcomplete/screens/main/MainActivity.kt), blob `740492da129ca5c556b7785a9859b5b4cad98f4c`: passes VIEW intent URI into the app view model.
- [GeoUri.kt](https://github.com/streetcomplete/StreetComplete/blob/master/app/src/commonMain/kotlin/de/westnordost/streetcomplete/util/GeoUri.kt), blob `0b7e6024457483e9c866f75687d7db8f90de7fcc`: `parseGeoUri` recognizes `geo:latitude,longitude?z=zoom` and checks coordinate ranges.
- [MainNavViewModel.kt](https://github.com/streetcomplete/StreetComplete/blob/master/app/src/commonMain/kotlin/de/westnordost/streetcomplete/screens/MainNavViewModel.kt), blob `ca5802c8d5db30a1561f2e076dcb38502d03ac90`: `setUri` uses the parsed location, **but substitutes zoom 18 if the requested zoom is absent or below 14**. This is a material incompatibility with treating the earlier helper's generic 1–20 zoom range as faithfully applied by StreetComplete.
- [Android platform geo-intent documentation](https://android.googlesource.com/platform/frameworks/base/+/8085477fb98eab36bbc8c3e9add76f398235b469/docs/html/guide/components/intents-common.jd) independently documents the general `geo:lat,lon?z=zoom` convention.

## Offline actual-upstream-parser test

For verification only, compiled the current upstream `GeoUri.kt` source in an **isolated local Kotlin/JVM harness** with a minimal local format shim. Upstream GPL-3.0 source was **not copied into the public Humanity Loop repository**. The test inputs and observed results:

| URI suffix | Parsed? | App's effective zoom per MainNav source |
|---|---|---|
| `21.000000,11.000000?z=13` | yes | **18**, not 13 |
| `0.000000,-180.000000?z=8` | yes | **18**, not 8 |
| `38.000000,-121.000000?z=10` | yes | **18**, not 10 |
| `21.000000,11.000000?z=15` | yes | 15 |
| `21.000000,11.000000?z=18` | yes | 18 |
| `21.000000,11.000000?z=20` | yes | 20 |

This verifies the parser's behavior for these inputs and the separate source-defined camera-zoom decision. It is **not** an Android instrumentation test or proof that an installed app opens from a web browser.

## Eight-role decision record (one model, not independent agents)

1. **Scout:** Field-TM #3060 has a concrete map-survey workflow gap; the preceding helper's unverified Android behavior is the next highest-value uncertainty.
2. **Verifier — PROCEED:** Upstream manifest, parser, intent handler and camera code establish a supported source-level path and a previously unknown zoom override. No duplicate existing Humanity Loop compatibility artifact was found in the prior receipt.
3. **PM:** Produce a safe opt-in Android-specific wrapper for local AOI GeoJSON, retaining the generic helper but rejecting misleading requested zooms below 14; test no network or map writes.
4. **Builder — COMPLETE:** [Original wrapper](2026-11-08-hotosm-streetcomplete-android-link.py) and [nine offline regression tests](test_2026-11-08-hotosm-streetcomplete-android-link.py). `python -m unittest -v runtime/foundry-fallback/test_2026-11-08-hotosm-streetcomplete-android-link.py`: **9/9 PASS**. `py_compile`: PASS. Uses existing [generic AOI helper](2026-11-08-hotosm-geo-intent.py); no third-party code bundled.
5. **10th Man — DISSENT:** This intentionally rejects z=1..13, so it cannot fit a large area in StreetComplete; forcing 14 may hide part of the AOI. The computed midpoint may be outside a concave or multipart AOI. Android may open another registered map app. iOS intent behavior and installed-version differences are not tested. The link does not encode the polygon or assign tasks.
6. **Safety — GO offline / HOLD upstream:** No device, personal location, external endpoint or OSM data is accessed. A Field-TM integration needs device testing, project AOI schema review, maintainer contribution rules, human approval and honest AI attribution.
7. **Revision:** Preserve the original generic helper unchanged. Add a clearly labeled StreetComplete-Android-only wrapper that fails closed on z<14 and invalid AOIs rather than silently implying the zoom is honored.
8. **Outcome:** Verified original code/tests and upstream source-level behavior only. **No accepted HOTOSM patch, field survey, participant, real-world impact or independent multi-LLM review.** Next: test the URI on an Android device with StreetComplete installed, inspect actual Field-TM AOI data and map viewport, then consider a small upstream integration with maintainer review.

## Reproduction

From the repository root, with Python 3.10+ and no external packages:

```sh
python -m unittest -v runtime/foundry-fallback/test_2026-11-08-hotosm-streetcomplete-android-link.py
python runtime/foundry-fallback/2026-11-08-hotosm-streetcomplete-android-link.py local-aoi.geojson --zoom 14
```

**Budget:** 0 AppDeploy model calls, 0 paid API, 0 deployments, 0 new schedules. The last queue-verified AppDeploy Free balance was 279.179185974 credits, below the 350 reserve; **not remeasured** here.

**Source/license discipline:** Upstream GPL-3.0 Kotlin was inspected and compiled locally for compatibility verification; only original Python wrapper/tests and factual analysis were published here. No source copying into an Apache-2.0 public artifact.
