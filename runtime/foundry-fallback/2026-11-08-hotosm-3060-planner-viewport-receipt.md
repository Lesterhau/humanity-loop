# HOTOSM Field-TM #3060 — project-level StreetComplete AOI viewport adapter

**Run ID:** HL-FALLBACK-20261108-HOTOSM-3060-PLANNER-VIEWPORT  
**Observation:** 2026-11-08 16:49–16:52 UTC  
**Execution:** Existing Humanity Loop hourly coordinator, **single-model role-separated offline fallback**, not eight independent LLMs.  
**Authority:** Tier-0 source/code inspection, local regression testing and public-safe Humanity Loop repository receipt. No external PR/issue, Android launch, OSM edit, live project API call, AppDeploy model, paid API, deployment, cron or production task mutation.

## New external-source integration finding

[HOTOSM Field-TM issue #3060](https://github.com/hotosm/field-tm/issues/3060) remains open as checked November 8. Its central concern is that road and river mapping does not suit task subdivision; one proposed option is a project AOI geo intent to StreetComplete. This is not proof that an upstream patch would be accepted.

Unlike the previous generic AOI and Android-parser prototypes, this follow-up inspects **Field-TM's actual documented data contract**:
- [GET planner-input backend route](https://github.com/hotosm/field-tm/blob/dev/src/backend/app/projects/task_plan_routes.py): returns project metadata, `aoi=project.outline`, manager-only data extract, and current task plan. This adapter uses **only** project mapping-app choice and AOI.
- [Mapping-app catalogue](https://github.com/hotosm/field-tm/blob/dev/src/backend/app/projects/mapping_apps.py): StreetComplete is already listed as a file-sharing, non-sync mapping app and is recommended for existing road attributes. This is not a claim that Field-TM lacks all StreetComplete support.
- [Task plan documentation](https://github.com/hotosm/field-tm/blob/dev/docs/task-plan.md) and [tasks-section template](https://github.com/hotosm/field-tm/blob/dev/src/backend/app/templates/partials/project_details/tasks_section.html): project tasks and their assignments are separate from the overall project AOI. A project-level link avoids representing roads as individually assigned StreetComplete tasks.
- [StreetComplete source-level zoom behavior](2026-11-08-hotosm-3060-streetcomplete-android-compat.md): requested `z<14` is overridden to 18 in the inspected app code; no actual device behavior has been accepted.

## Distinct executable artifact

- [Offline planner-input adapter](2026-11-08-hotosm-fieldtm-planner-viewport.py), GitHub blob `a60df680a4262fb1aff86b21ce10b3cb120f5bc4`
- [Twelve regression tests](test_2026-11-08-hotosm-fieldtm-planner-viewport.py), blob `0145426928434ee0b173da80eedab42c13956535`

The adapter consumes a **local** copy of Field-TM's `planner-input` JSON, not an authenticated API call. It checks `field_mapping_app == "StreetComplete"`, extracts only `aoi`, estimates Web Mercator bounding coverage for an explicitly specified screen and padding, and generates a generic `geo:` link **only if the estimated fit is at zoom 14–20**. It returns a transparent no-link status for larger areas and rejects malformed AOIs, extreme/polar geometry, invalid viewports, and zero-extent polygons. It does not serialize project name, manager-only `features`, task-plan assignments, comments or participant details into its output.

**Local test:** Python standard-library `unittest` against local copies of the two previously published Humanity Loop companion modules, 12/12 PASS on 2026-11-08; `py_compile` PASS. Cases include actual documented response shape (synthetic data), project-app gating, approximate fit, too-large AOI no-link, dateline, FeatureCollection, privacy nonleakage, polar latitude, wide geometry, invalid viewport, malformed GeoJSON and degenerate polygon. GitHub code/test files were independently fetched after commit. No upstream Field-TM test suite or real project payload was run.

Reproduce from the Humanity Loop repository root:

```sh
python -m unittest -v runtime/foundry-fallback/test_2026-11-08-hotosm-fieldtm-planner-viewport.py
python runtime/foundry-fallback/2026-11-08-hotosm-fieldtm-planner-viewport.py local-planner-input.json --width 360 --height 640 --padding 32
```

## Eight-role review (one underlying model)

1. **Scout:** Move the previous geo-link concept toward Field-TM's real project-data contract rather than another unrelated web audit.
2. **Verifier — PROCEED:** Upstream issue remains open; backend API, app catalogue, task-plan contract and template checked. Prior two artifacts lacked this contract/viewport decision.
3. **PM:** One local, reproducible, privacy-minimal adapter; explicit no-link on too-large AOI; failure tests and no live integration.
4. **Builder — COMPLETE:** Original Python adapter + twelve offline regression tests, verified in public repo.
5. **10th Man — DISSENT:** Bounding-box fit assumes a rectangular screen and generic Web Mercator tiles, not StreetComplete's actual UI padding/camera behavior; a center point may fall outside concave or multipart AOI. The shortest longitude arc may not represent huge polygons. A `geo:` URI may launch another map app. Current Field-TM already offers file/QR exports; upstream maintainers may reject this workflow.
6. **Safety — GO for offline artifact / HOLD for upstream:** No network, credentials, private project data, participant location or map write. HOTOSM's [AI-assisted contribution policy](https://github.com/hotosm/field-tm/blob/dev/AGENTS.md) requires human accountability, testing and truthful AI-level disclosure; no external PR was authorized.
7. **Revision:** Gate strictly to StreetComplete projects, use only AOI, decline unsupported fit instead of silently applying z=14 or pretending task boundaries are transferred.
8. **Outcome:** Reusable technical prototype, **not** a deployed feature, accepted HOTOSM contribution, field observation, outside node submission, beneficiary impact or independent multi-model validation.

## Next unchecked proof

Obtain a consented real Field-TM project `planner-input` fixture (redacted; no assignments or manager-only extract), compare estimated link/zoom against a physical Android device running StreetComplete, and confirm the project AOI is visually reachable. Then prepare a small upstream code integration for human review if the maintainer considers the approach appropriate. Do not open an unsolicited PR or send outreach under this run's authority.

**Budget:** 0 AppDeploy model calls, 0 deployments, 0 paid API calls, 0 new schedules. Previously repository-verified balance: 279.179185974 credits, below the protected 350-credit reserve; **not remeasured** this run.
