import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from monitor_cadence_gate import scan_due

class CadenceGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "latest.json"
        self.now = datetime(2026, 11, 7, 2, 0, tzinfo=timezone.utc)

    def receipt(self, age_hours):
        when = self.now - timedelta(hours=age_hours)
        self.path.write_text(json.dumps({"runAt": when.isoformat()}))

    def test_recent_success_skips_extra_scheduled_scan(self):
        self.receipt(2)
        self.assertFalse(scan_due(self.path, "schedule", self.now))

    def test_five_hour_receipt_runs_catchup(self):
        self.receipt(5)
        self.assertTrue(scan_due(self.path, "schedule", self.now))

    def test_missing_receipt_runs_scan(self):
        self.assertTrue(scan_due(self.path, "schedule", self.now))

    def test_malformed_receipt_runs_scan(self):
        self.path.write_text("not-json")
        self.assertTrue(scan_due(self.path, "schedule", self.now))

    def test_future_timestamp_runs_scan(self):
        self.receipt(-1)
        self.assertTrue(scan_due(self.path, "schedule", self.now))

    def test_push_and_manual_dispatch_are_always_checked(self):
        self.receipt(1)
        self.assertTrue(scan_due(self.path, "push", self.now))
        self.assertTrue(scan_due(self.path, "workflow_dispatch", self.now))

    def test_unsupported_event_does_not_run(self):
        self.assertFalse(scan_due(self.path, "pull_request", self.now))

if __name__ == "__main__":
    unittest.main()
