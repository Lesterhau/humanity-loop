# Humanity Loop Foundry-style fallback — HOTOSM Field-TM #3060 AOI geo-link prototype

**Date:** 2026-11-08 UTC
**Run ID:** HL-FALLBACK-20261108-HOTOSM-3060
**Mode:** existing Humanity Loop hourly coordinator, **single-model role-separated fallback**. This is **not** independently executed multi-LLM review, a running Foundry scheduler, or an accepted outside contribution.
**Permission:** Tier-0, public source/code read and isolated offline Python prototype only. No live map edits, third-party repository changes, outside contact, device app launch, new worker, model API, AppDeploy deployment, paid operation, or production mutation.

## Source and nonduplication
- Original upstream public-interest need: [Humanitarian OpenStreetMap Team Field-TM issue #3060](https://github.com/hotosm/field-tm/issues/3060), **open** on the November 8 readback. It asks for alternative workflows for mapping roads/other linear features, including a possible `geo:lat,lon?z=zoom` link to StreetComplete. The only fetched issue comment was an automated Linear link, not a fix/acceptance report.
- [Field-TM AGENTS.md](https://github.com/hotosm/field-tm/blob/dev/AGENTS.md) and [CONTRIBUTING.md](https://github.com/hotosm/field-tm/blob/dev/CONTRIBUTING.md) require tests, human responsibility, honest AI disclosure and no AI-assisted work on good-first issues. No outside PR was opened.
- [StreetComplete upstream project](https://github.com/streetcomplete/StreetComplete) is a field OpenStreetMap editor. **Actual StreetComplete handling of a generic geo URI was not independently tested on a device.** The issue's proposed URI format is a candidate, not an established app integration.

## Eight-role decision record (one model; logically separated)
1. **Scout — candidate:** A reusable, offline AOI-to-generic-geo-URI helper and tests could reduce effort to prototype the issue's proposed mobile map entry path. No claim of implementation in Field-TM.
2. **Verifier — PROCEED with limited scope:** Open upstream issue and maintainer's suggested URI pattern verified. No evidence the specific feature already exists in production, nor proof it will work on actual StreetComplete devices. Narrow to generic URI generation.
3. **Project Manager — acceptance:** Standard-library-only helper consumes local GeoJSON Polygon/MultiPolygon/Feature/FeatureCollection and a caller-supplied zoom; outputs a deterministic URI; rejects unsupported/invalid inputs; tests normal, multipolygon, antimeridian, and failure cases. No network or write operations.
4. **Builder — DELIVERED:** [Prototype source](2026-11-08-hotosm-geo-intent.py) and [11 regression tests](test_2026-11-08-hotosm-geo-intent.py). Uses a shortest-circular-longitude-arc midpoint for antimeridian cases, latitude bounding midpoint and explicit 1–20 zoom. CLI accepts local GeoJSON file and `--zoom`. This is original proof-of-concept code, not a patch against HOTOSM's application.
5. **10th Man — DISSENT:** A bounding-box midpoint need not lie inside a concave polygon or an island multipolygon. A shortest-arc heuristic can misrepresent extremely wide AOIs. A generic `geo:` link may launch another app or fail to launch StreetComplete; project AOI is not encoded as a polygon and fit-to-extent zoom is not computed. Therefore the tool cannot be represented as a working Field-TM/StreetComplete integration or safe navigational guidance.
6. **Safety Governor — GO for offline prototype; HOLD for external deployment:** No location tracking, third-party writes, API calls, credentials or participant data. Any Field-TM integration needs device tests, maintainer review, upstream licensing/contribution checks, privacy review of how coordinates are shared, and human authorization.
7. **Revision — implemented:** Reject invalid lat/lon, nonfinite values, nonclosed rings, empty collections, unsupported geometries, and out-of-range zoom. Explicitly label URI as generic and document that it is not a guaranteed polygon centroid or StreetComplete deep link.
8. **Outcome — technical artifact only:** Local Python `unittest` run: **11/11 PASS**, `py_compile` PASS on a local mirror of the published prototype. GitHub source/test files independently fetched back after write. No upstream test suite, device test, accepted PR, outside participant, map improvement, or beneficiary outcome. Next unchecked action: have a human developer validate StreetComplete URI handling on Android/iOS and compare Field-TM's actual project AOI data contract before preparing a small upstream integration diff; no unsolicited submission.

## Reproduce
From repository root:

```sh
python -m unittest -v runtime/foundry-fallback/test_2026-11-08-hotosm-geo-intent.py
python runtime/foundry-fallback/2026-11-08-hotosm-geo-intent.py path/to/aoi.geojson --zoom 13
```

**Evidence standard:** A passing offline test shows only the helper's behavior on synthetic fixtures. It is not proof of live field usefulness, NGO acceptance or independent multi-agent execution.

**Compute/budget:** 0 AppDeploy/Foundry AI calls, 0 paid model API calls, 0 deployment, 0 new scheduled task. Protected AppDeploy reserve remains breached according to the queue's latest read-only Nov 8 balance of 279.179185974 credits; no new balance measurement was performed in this run.

**Durable state:** This receipt and the two code files are in the public Humanity Loop repository. No external issue, PR, outreach, financial or production setting was changed.
