"""Offline regression checks against Field-TM's documented planner-input shape."""
import importlib.util
import math
from pathlib import Path
import unittest

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("hl_planner_viewport", HERE / "2026-11-08-hotosm-fieldtm-planner-viewport.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def square(lon=11.0, lat=21.0, side=0.001):
    return {"type": "Polygon", "coordinates": [[
        [lon, lat], [lon + side, lat], [lon + side, lat + side],
        [lon, lat + side], [lon, lat]
    ]]}


def payload(aoi=None, app="StreetComplete"):
    return {"project": {"id": 3, "name": "Demo", "field_mapping_app": app},
            "aoi": aoi if aoi is not None else square(),
            "features": {"secret": "manager-only data extract"},
            "task_plan": {"features": [{"properties": {"assigned_to": "private volunteer", "comment": "do not export"}}]}}


class PlannerViewportTests(unittest.TestCase):
    def test_documented_planner_input_generates_usable_uri(self):
        out = mod.project_aoi_link(payload())
        self.assertEqual(out["status"], "estimated_fit_only")
        self.assertTrue(out["uri"].startswith("geo:21.000500,11.000500?z="))
        self.assertGreaterEqual(out["estimated_fit_zoom"], 14)

    def test_does_not_leak_task_assignments_or_data_extract(self):
        out = str(mod.project_aoi_link(payload()))
        for private in ("private volunteer", "manager-only", "do not export", "Demo"):
            self.assertNotIn(private, out)

    def test_oversize_project_refuses_misleading_link(self):
        out = mod.project_aoi_link(payload(square(side=5)))
        self.assertIsNone(out["uri"])
        self.assertEqual(out["status"], "aoi_too_large_for_supported_zoom")

    def test_antimeridian_project(self):
        aoi = {"type": "Polygon", "coordinates": [[
            [179.999, 0], [-179.999, 0], [-179.999, 0.001],
            [179.999, 0.001], [179.999, 0]]]}
        out = mod.project_aoi_link(payload(aoi))
        self.assertEqual(out["status"], "estimated_fit_only")
        self.assertIn(",-180.000000?z=", out["uri"])

    def test_feature_wrapped_aoi(self):
        wrapped = {"type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": square(), "properties": {"assigned_to": "secret"}}]}
        self.assertEqual(mod.project_aoi_link(payload(wrapped))["status"], "estimated_fit_only")

    def test_reject_non_streetcomplete_project(self):
        with self.assertRaisesRegex(ValueError, "Only StreetComplete"):
            mod.project_aoi_link(payload(app="ODK"))

    def test_reject_missing_aoi(self):
        bad = payload()
        bad["aoi"] = None
        with self.assertRaisesRegex(ValueError, "Missing project AOI"):
            mod.project_aoi_link(bad)

    def test_reject_invalid_geojson(self):
        with self.assertRaisesRegex(ValueError, "Only Polygon"):
            mod.project_aoi_link(payload({"type": "Point", "coordinates": [1, 2]}))

    def test_reject_invalid_viewport(self):
        for width, height, padding in [(100, 640, 10), (360, 640, 180), (360, 640, -1), (True, 640, 0)]:
            with self.subTest(width=width, height=height, padding=padding), self.assertRaises(ValueError):
                mod.project_aoi_link(payload(), viewport_width=width, viewport_height=height, padding=padding)

    def test_reject_polar_mercator_overflow(self):
        with self.assertRaisesRegex(ValueError, "Mercator latitude"):
            mod.project_aoi_link(payload(square(lat=89, side=0.001)))

    def test_reject_extreme_longitude_extent(self):
        aoi = {"type": "Polygon", "coordinates": [[
            [-170, 0], [-50, 0], [70, 1], [170, 1], [-170, 0]]]}
        with self.assertRaisesRegex(ValueError, "too wide"):
            mod.project_aoi_link(payload(aoi))

    def test_zero_span_polygon_rejected(self):
        aoi = {"type": "Polygon", "coordinates": [[[1, 1], [1, 1], [1, 1], [1, 1]]]}
        with self.assertRaisesRegex(ValueError, "zero geographic extent"):
            mod.project_aoi_link(payload(aoi))


if __name__ == "__main__":
    unittest.main()
