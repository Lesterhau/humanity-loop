#!/usr/bin/env python3

import unittest

from cap_daily_audit import audit_feature, build_report


class CapDailyAuditTests(unittest.TestCase):
    def setUp(self):
        self.now = "2026-09-30T20:00:00Z"

    def test_complete_alert_has_no_findings(self):
        feature = {
            "id": "https://api.weather.gov/alerts/test",
            "properties": {
                "senderName": "NWS Test",
                "event": "Tornado Warning",
                "sent": "2026-09-30T20:00:00Z",
                "expires": "2026-09-30T21:00:00Z",
                "severity": "Extreme",
                "certainty": "Observed",
                "urgency": "Immediate",
                "headline": "Tornado Warning",
                "description": "A tornado is occurring.",
                "instruction": "Take shelter now.",
                "areaDesc": "Test County",
            },
        }
        self.assertEqual(audit_feature(feature, self.now), [])

    def test_immediate_alert_without_instruction_is_flagged(self):
        feature = {
            "id": "https://api.weather.gov/alerts/test",
            "properties": {
                "event": "Flash Flood Warning",
                "sent": "2026-09-30T20:00:00Z",
                "expires": "2026-09-30T21:00:00Z",
                "severity": "Severe",
                "certainty": "Likely",
                "urgency": "Immediate",
                "headline": "Flash Flood Warning",
                "description": "Flooding is occurring.",
                "instruction": "",
                "areaDesc": "Test County",
            },
        }
        titles = {item["title"] for item in audit_feature(feature, self.now)}
        self.assertIn("Immediate alert has no action instruction", titles)

    def test_bad_expiration_is_flagged(self):
        feature = {
            "id": "https://api.weather.gov/alerts/test",
            "properties": {
                "event": "Test",
                "sent": "2026-09-30T20:00:00Z",
                "expires": "2026-09-30T19:00:00Z",
                "severity": "Minor",
                "certainty": "Possible",
                "urgency": "Future",
                "headline": "Test",
                "description": "Test",
                "instruction": "Test.",
                "areaDesc": "Test",
            },
        }
        titles = {item["title"] for item in audit_feature(feature, self.now)}
        self.assertIn("Expiration does not follow sent/effective time", titles)

    def test_report_counts_match_findings(self):
        feature = {"properties": {"urgency": "Immediate"}}
        report = build_report([feature], self.now)
        self.assertEqual(report["findingsCount"], len(report["findings"]))
        self.assertEqual(
            report["findingsCount"],
            sum(report["bySeverity"].values()),
        )


if __name__ == "__main__":
    unittest.main()
