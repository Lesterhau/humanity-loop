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
        self.assertIn("Immediate alert lacks separate CAP instruction field", titles)

    def test_nws_test_message_is_not_public_hazard_finding(self):
        feature = {
            "id": "https://api.weather.gov/alerts/urn:oid:KEEPALIVE",
            "properties": {
                "event": "Test Message",
                "urgency": "Immediate",
                "status": "Actual",
                "headline": "",
            },
        }
        self.assertEqual(audit_feature(feature, self.now), [])
        report = build_report([feature], self.now)
        self.assertEqual(report["alertsChecked"], 1)
        self.assertEqual(report["findingsCount"], 0)

    def test_cap_status_test_is_not_public_hazard_finding(self):
        feature = {
            "id": "https://api.weather.gov/alerts/test-status",
            "properties": {
                "event": "Tornado Warning",
                "status": "Test",
                "urgency": "Immediate",
                "headline": "",
            },
        }
        self.assertEqual(audit_feature(feature, self.now), [])

    def test_real_tornado_warning_is_not_filtered(self):
        feature = {
            "id": "https://api.weather.gov/alerts/real-warning",
            "properties": {
                "event": "Tornado Warning",
                "status": "Actual",
                "urgency": "Immediate",
                "headline": "",
                "instruction": "",
            },
        }
        titles = {item["title"] for item in audit_feature(feature, self.now)}
        self.assertIn("Missing headline", titles)
        self.assertIn("Immediate alert lacks separate CAP instruction field", titles)

    def test_optional_instruction_detail_avoids_unverified_safety_claim(self):
        feature = {
            "id": "https://api.weather.gov/alerts/real-warning",
            "properties": {
                "event": "Tornado Warning",
                "status": "Actual",
                "urgency": "Immediate",
                "description": "Shelter in a basement immediately.",
                "instruction": "",
            },
        }
        findings = audit_feature(feature, self.now)
        flagged = [f for f in findings if f["title"] == "Immediate alert lacks separate CAP instruction field"]
        self.assertEqual(len(flagged), 1)
        self.assertIn("before concluding", flagged[0]["detail"])

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
