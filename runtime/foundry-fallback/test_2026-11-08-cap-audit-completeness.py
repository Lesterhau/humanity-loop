"""Offline regression characterization for Humanity Loop's NWS CAP fetch completeness.

This tests existing behavior, not a deployed fix. Run from repo root:
python -m unittest -v runtime/foundry-fallback/test_2026-11-08-cap-audit-completeness.py

The module is loaded from scripts/cap_daily_audit.py, with urlopen patched.
No HTTP requests, alert issuance, or production changes occur.
"""
from __future__ import annotations
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[2] / "scripts" / "cap_daily_audit.py"
spec = importlib.util.spec_from_file_location("hl_cap_source", SOURCE)
assert spec is not None and spec.loader is not None
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)

class FakeResponse(io.BytesIO):
    status = 200
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()

def fake_fetch(payload):
    raw = json.dumps(payload).encode("utf-8")
    with patch.object(cap, "urlopen", return_value=FakeResponse(raw)) as mocked:
        records = cap.fetch_active_alerts()
        mocked.assert_called_once()
        return records

class CAPCoverageCharacterization(unittest.TestCase):
    def test_251st_alert_is_silently_excluded(self):
        records = [{"id": f"urn:synthetic:{i}"} for i in range(251)]
        result = fake_fetch({"features": records})
        self.assertEqual(len(result), 250)
        self.assertNotIn(records[250], result)
        self.assertEqual(result[-1], records[249])

    def test_null_features_is_treated_as_empty_success(self):
        self.assertEqual(fake_fetch({"features": None}), [])

    def test_missing_features_is_treated_as_empty_success(self):
        self.assertEqual(fake_fetch({"type": "FeatureCollection"}), [])

    def test_non_object_features_are_dropped_without_count(self):
        result = fake_fetch({"features": [{"id": "one"}, None, "invalid", {"id": "two"}]})
        self.assertEqual([r["id"] for r in result], ["one", "two"])

    def test_non_list_features_fail_visible(self):
        with self.assertRaisesRegex(RuntimeError, "feature list"):
            fake_fetch({"features": "not-a-list"})

if __name__ == "__main__":
    unittest.main()
