"""Offline Field-TM planner-input -> conservative StreetComplete AOI link.

Consumes the documented GET /api/v1/projects/{id}/planner-input JSON as a
LOCAL file. Only the public project AOI is used; task assignments and data
extracts are never copied into the result. No HTTP, device, or map writes.

A URI is returned only if a rough Web Mercator viewport fit can use zoom>=14.
This is a *screen-size estimate*, not a verified Android camera fit.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
MERCATOR_LAT_MAX = 85.05112878


def _load_module(filename: str, module_name: str):
    path = HERE / filename
    if not path.is_file():
        raise FileNotFoundError(f"Required companion file missing: {filename}")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _longitude_fraction_span(longitudes: list[float]) -> float:
    """Shortest circular arc in [0,1], suitable for narrow AOIs crossing 180°."""
    xs = sorted((lon % 360) / 360 for lon in longitudes)
    gaps = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    gaps.append(xs[0] + 1 - xs[-1])
    return 1 - max(gaps)


def _mercator_y(lat: float) -> float:
    if abs(lat) > MERCATOR_LAT_MAX:
        raise ValueError("AOI exceeds the Web Mercator latitude limit")
    phi = math.radians(lat)
    return (1 - math.asinh(math.tan(phi)) / math.pi) / 2


def project_aoi_link(
    planner_input: dict[str, Any],
    *,
    viewport_width: int = 360,
    viewport_height: int = 640,
    padding: int = 32,
) -> dict[str, Any]:
    """Return a privacy-minimal link decision for a StreetComplete project.

    A returned URI is an approximate *center* only; no polygon, task boundary,
    user name, team assignment, or data extract is encoded in the geo intent.
    """
    if not isinstance(planner_input, dict):
        raise ValueError("planner-input must be a JSON object")
    project = planner_input.get("project")
    if not isinstance(project, dict) or project.get("field_mapping_app") != "StreetComplete":
        raise ValueError("Only StreetComplete projects are supported")
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (viewport_width, viewport_height, padding)):
        raise ValueError("Viewport dimensions and padding must be integers")
    if viewport_width < 128 or viewport_height < 128 or padding < 0 or 2 * padding >= min(viewport_width, viewport_height):
        raise ValueError("Invalid viewport or padding")
    aoi = planner_input.get("aoi")
    if not isinstance(aoi, dict):
        raise ValueError("Missing project AOI")
    geo = _load_module("2026-11-08-hotosm-geo-intent.py", "hl_aoi_geo_for_viewport")
    vertices = geo._polygon_vertices(aoi)
    if not vertices:
        raise ValueError("Project AOI has no vertices")
    xspan = _longitude_fraction_span([lon for lon, _ in vertices])
    ys = [_mercator_y(lat) for _, lat in vertices]
    yspan = max(ys) - min(ys)
    if xspan <= 0 or yspan <= 0:
        raise ValueError("AOI has zero geographic extent")
    # A bounding arc does not disambiguate polygons spanning most of the globe.
    if xspan >= 0.5:
        raise ValueError("Longitude extent is too wide for a reliable AOI fit")
    usable_width = viewport_width - 2 * padding
    usable_height = viewport_height - 2 * padding
    zoom_x = math.log2(usable_width / (256 * xspan)) if xspan else math.inf
    zoom_y = math.log2(usable_height / (256 * yspan)) if yspan else math.inf
    fit_zoom = min(20, math.floor(min(zoom_x, zoom_y))) if math.isfinite(min(zoom_x, zoom_y)) else 20
    if fit_zoom < 14:
        return {
            "status": "aoi_too_large_for_supported_zoom",
            "uri": None,
            "estimated_fit_zoom": fit_zoom,
            "note": "StreetComplete overrides zoom below 14; do not claim full AOI is visible.",
        }
    wrapper = _load_module("2026-11-08-hotosm-streetcomplete-android-link.py", "hl_android_geo_for_viewport")
    return {
        "status": "estimated_fit_only",
        "uri": wrapper.streetcomplete_android_link(aoi, fit_zoom),
        "estimated_fit_zoom": fit_zoom,
        "note": "Approximate center, not an AOI boundary or guaranteed device viewport.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("planner_input", type=Path, help="LOCAL planner-input JSON; no network requests")
    parser.add_argument("--width", type=int, default=360)
    parser.add_argument("--height", type=int, default=640)
    parser.add_argument("--padding", type=int, default=32)
    args = parser.parse_args()
    if args.planner_input.stat().st_size > 5_000_000:
        parser.error("Local planner-input JSON exceeds 5 MB prototype limit")
    data = json.loads(args.planner_input.read_text(encoding="utf-8"))
    print(json.dumps(project_aoi_link(data, viewport_width=args.width, viewport_height=args.height, padding=args.padding), indent=2))


if __name__ == "__main__":
    main()
