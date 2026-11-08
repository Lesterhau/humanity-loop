"""Offline GeoJSON AOI to generic geo: URI proof of concept.

No network access, geocoding, OSM edits, or app launching. The URI is a
candidate for Android geo: intent handling; StreetComplete acceptance is not
established by this module.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _polygon_vertices(obj: dict[str, Any]) -> list[tuple[float, float]]:
    kind = obj.get("type")
    if kind == "Feature":
        geometry = obj.get("geometry")
        if not isinstance(geometry, dict):
            raise ValueError("Feature must contain a geometry object")
        return _polygon_vertices(geometry)
    if kind == "FeatureCollection":
        features = obj.get("features")
        if not isinstance(features, list) or not features:
            raise ValueError("FeatureCollection must contain features")
        vertices: list[tuple[float, float]] = []
        for feature in features:
            if not isinstance(feature, dict):
                raise ValueError("FeatureCollection contains invalid feature")
            vertices.extend(_polygon_vertices(feature))
        return vertices
    if kind not in {"Polygon", "MultiPolygon"}:
        raise ValueError("Only Polygon and MultiPolygon AOIs are supported")
    polygons = [obj.get("coordinates")] if kind == "Polygon" else obj.get("coordinates")
    if not isinstance(polygons, list) or not polygons:
        raise ValueError("Geometry has no polygons")
    vertices: list[tuple[float, float]] = []
    for rings in polygons:
        if not isinstance(rings, list) or not rings:
            raise ValueError("Polygon has no rings")
        for ring in rings:
            if not isinstance(ring, list) or len(ring) < 4 or ring[0] != ring[-1]:
                raise ValueError("Polygon rings must be closed with >=4 coordinates")
            for point in ring:
                if not isinstance(point, (list, tuple)) or len(point) < 2:
                    raise ValueError("Invalid GeoJSON coordinate")
                lon, lat = point[:2]
                if (isinstance(lon, bool) or isinstance(lat, bool)
                        or not isinstance(lon, (int, float))
                        or not isinstance(lat, (int, float))
                        or not math.isfinite(lon) or not math.isfinite(lat)
                        or not -180 <= lon <= 180 or not -90 <= lat <= 90):
                    raise ValueError("Coordinates must be finite lon/lat within bounds")
                vertices.append((float(lon), float(lat)))
    return vertices


def _longitude_midpoint(longitudes: list[float]) -> float:
    """Center of shortest circular longitude arc, robust at antimeridian."""
    positions = sorted(lon % 360 for lon in longitudes)
    if len(positions) == 1:
        center = positions[0]
    else:
        gaps = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
        gaps.append(positions[0] + 360 - positions[-1])
        largest_gap_index = max(range(len(gaps)), key=gaps.__getitem__)
        start = positions[(largest_gap_index + 1) % len(positions)]
        covered_arc = 360 - gaps[largest_gap_index]
        center = (start + covered_arc / 2) % 360
    result = (center + 180) % 360 - 180
    return 0.0 if result == 0 else result


def geo_intent(aoi: dict[str, Any], zoom: int) -> str:
    """Return geo:lat,lon?z=N using bounding-arc midpoint, not centroid.

    Zoom is supplied by the caller; this does NOT calculate a fit-to-AOI zoom.
    """
    if isinstance(zoom, bool) or not isinstance(zoom, int) or not 1 <= zoom <= 20:
        raise ValueError("zoom must be an integer between 1 and 20")
    if not isinstance(aoi, dict):
        raise ValueError("AOI must be a GeoJSON object")
    vertices = _polygon_vertices(aoi)
    latitudes = [lat for _, lat in vertices]
    lat = (min(latitudes) + max(latitudes)) / 2
    lon = _longitude_midpoint([lon for lon, _ in vertices])
    return f"geo:{lat:.6f},{lon:.6f}?z={zoom}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("geojson", type=Path, help="Local Polygon/MultiPolygon GeoJSON file")
    parser.add_argument("--zoom", type=int, required=True, help="Caller-supplied zoom, 1-20")
    args = parser.parse_args()
    print(geo_intent(json.loads(args.geojson.read_text(encoding="utf-8")), args.zoom))


if __name__ == "__main__":
    main()
