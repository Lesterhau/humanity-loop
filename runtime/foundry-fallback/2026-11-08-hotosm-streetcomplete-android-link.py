"""Conservative StreetComplete-on-Android geo URI wrapper for a local GeoJSON AOI.

This is an offline compatibility prototype, not a Field-TM integration.
The existing generic AOI helper accepts zoom 1..20; StreetComplete's
MainNavViewModelImpl currently overrides zooms below 14 to 18. This wrapper
rejects those zooms rather than silently advertising a misleading scale.

No network, device launch, tracking, OSM edits, or third-party code included.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

_HELPER = Path(__file__).with_name("2026-11-08-hotosm-geo-intent.py")


def _generic_geo_intent(aoi: dict[str, Any], zoom: int) -> str:
    """Load the existing original Humanity Loop AOI helper by file path."""
    if not _HELPER.is_file():
        raise FileNotFoundError(f"Required companion AOI helper not found: {_HELPER.name}")
    spec = importlib.util.spec_from_file_location("hl_generic_geo_intent", _HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load companion AOI helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.geo_intent(aoi, zoom)


def streetcomplete_android_link(aoi: dict[str, Any], zoom: int) -> str:
    """Return a generic geo URI whose zoom is not overridden by the cited Android app code.

    The link remains a generic Android geo: intent, not an app-specific link.
    On devices with multiple handlers, another map application may open.
    A polygon center is approximate and can be outside the area of interest.
    """
    if isinstance(zoom, bool) or not isinstance(zoom, int) or not 14 <= zoom <= 20:
        raise ValueError(
            "StreetComplete Android zoom must be an integer 14..20; "
            "the cited app source substitutes zoom 18 when zoom is below 14"
        )
    return _generic_geo_intent(aoi, zoom)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("geojson", type=Path, help="Local Polygon/MultiPolygon GeoJSON file")
    parser.add_argument("--zoom", type=int, required=True, help="Explicit zoom 14..20")
    args = parser.parse_args()
    aoi = json.loads(args.geojson.read_text(encoding="utf-8"))
    print(streetcomplete_android_link(aoi, args.zoom))


if __name__ == "__main__":
    main()
