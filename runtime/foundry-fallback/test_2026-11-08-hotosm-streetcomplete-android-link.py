"""Original offline tests for StreetComplete Android geo-URI compatibility wrapper."""

import importlib.util
import math
from pathlib import Path
import unittest

HERE = Path(__file__).parent
MODULE = HERE / "2026-11-08-hotosm-streetcomplete-android-link.py"
spec = importlib.util.spec_from_file_location("hl_streetcomplete_android_link", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def square(west=10, south=20, east=12, north=22):
    return {"type": "Polygon", "coordinates": [[
        [west, south], [east, south], [east, north], [west, north], [west, south]
    ]]}


class StreetCompleteAndroidLinkTests(unittest.TestCase):
    def test_zoom_14_kept(self):
        self.assertEqual(module.streetcomplete_android_link(square(), 14), "geo:21.000000,11.000000?z=14")

    def test_zoom_18_kept(self):
        self.assertEqual(module.streetcomplete_android_link(square(), 18), "geo:21.000000,11.000000?z=18")

    def test_zoom_20_kept(self):
        self.assertEqual(module.streetcomplete_android_link(square(), 20), "geo:21.000000,11.000000?z=20")

    def test_reject_zoom_below_14_to_avoid_override(self):
        for z in (1, 8, 10, 13):
            with self.subTest(z=z), self.assertRaisesRegex(ValueError, "substitutes zoom 18"):
                module.streetcomplete_android_link(square(), z)

    def test_reject_invalid_zoom(self):
        for z in (-1, 0, 21, True, 14.0, "14"):
            with self.subTest(z=z), self.assertRaises(ValueError):
                module.streetcomplete_android_link(square(), z)

    def test_antimeridian(self):
        self.assertEqual(
            module.streetcomplete_android_link(square(179, -1, -179, 1), 14),
            "geo:0.000000,-180.000000?z=14",
        )

    def test_invalid_geojson_still_rejected(self):
        with self.assertRaisesRegex(ValueError, "Only Polygon"):
            module.streetcomplete_android_link({"type": "Point", "coordinates": [1, 2]}, 14)

    def test_nonfinite_geojson_still_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            module.streetcomplete_android_link(square(10, 20, math.nan, 22), 14)

    def test_missing_companion_fails_closed(self):
        original = module._HELPER
        try:
            module._HELPER = HERE / "does-not-exist.py"
            with self.assertRaises(FileNotFoundError):
                module.streetcomplete_android_link(square(), 14)
        finally:
            module._HELPER = original


if __name__ == "__main__":
    unittest.main()
