"""Offline regression tests for HOTOSM AOI geo-intent prototype."""

import importlib.util
import math
from pathlib import Path
import unittest

MODULE = Path(__file__).with_name("2026-11-08-hotosm-geo-intent.py")
spec = importlib.util.spec_from_file_location("geo_intent_prototype", MODULE)
geo_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geo_module)
geo_intent = geo_module.geo_intent


def square(x0, y0, x1, y1):
    return {"type": "Polygon", "coordinates": [[
        [x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]
    ]]}


class GeoIntentTests(unittest.TestCase):
    def test_normal_polygon(self):
        self.assertEqual(geo_intent(square(10, 20, 12, 22), 13), "geo:21.000000,11.000000?z=13")

    def test_antimeridian_crossing(self):
        self.assertEqual(geo_intent(square(179, -1, -179, 1), 8), "geo:0.000000,-180.000000?z=8")

    def test_negative_longitude(self):
        self.assertEqual(geo_intent(square(-122, 37, -120, 39), 10), "geo:38.000000,-121.000000?z=10")

    def test_feature_collection(self):
        aoi = {"type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": square(0, 0, 2, 2), "properties": {}},
            {"type": "Feature", "geometry": square(4, 4, 6, 6), "properties": {}},
        ]}
        self.assertEqual(geo_intent(aoi, 9), "geo:3.000000,3.000000?z=9")

    def test_multipolygon(self):
        aoi = {"type": "MultiPolygon", "coordinates": [
            square(10, 10, 12, 12)["coordinates"],
            square(14, 14, 16, 16)["coordinates"],
        ]}
        self.assertEqual(geo_intent(aoi, 11), "geo:13.000000,13.000000?z=11")

    def test_reject_unsupported_point(self):
        with self.assertRaisesRegex(ValueError, "Only Polygon"):
            geo_intent({"type": "Point", "coordinates": [1, 2]}, 12)

    def test_reject_invalid_latitude(self):
        with self.assertRaisesRegex(ValueError, "within bounds"):
            geo_intent(square(0, 91, 2, 92), 12)

    def test_reject_nonfinite(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            geo_intent(square(0, 0, math.nan, 2), 12)

    def test_reject_unclosed_ring(self):
        aoi = square(0, 0, 2, 2)
        aoi["coordinates"][0][-1] = [1, 1]
        with self.assertRaisesRegex(ValueError, "closed"):
            geo_intent(aoi, 12)

    def test_reject_invalid_zoom(self):
        for z in (-1, 0, 21, True, 11.5, "12"):
            with self.subTest(z=z), self.assertRaisesRegex(ValueError, "zoom"):
                geo_intent(square(0, 0, 2, 2), z)

    def test_reject_empty_feature_collection(self):
        with self.assertRaisesRegex(ValueError, "contain features"):
            geo_intent({"type": "FeatureCollection", "features": []}, 12)


if __name__ == "__main__":
    unittest.main()
