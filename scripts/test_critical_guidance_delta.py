#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from critical_guidance_delta import SOURCES, comparable_text, diff_excerpt, normalize_html, run


class CriticalGuidanceDeltaTests(unittest.TestCase):
    def test_normalize_html_excludes_nonvisible_script_content(self):
        html = "<html><script>bad()</script><body><h1>FDA Safety</h1><p>Visible.</p></body></html>"
        self.assertEqual(normalize_html(html), "FDA Safety\nVisible.")

    def test_diff_excerpt_retains_added_and_removed_lines(self):
        diff = diff_excerpt("old warning\nkeep", "new warning\nkeep")
        self.assertIn("- old warning", diff)
        self.assertIn("+ new warning", diff)

    def test_comparable_text_ignores_only_standalone_who_headers(self):
        old = "Alert 3/2026\nProduct name, lot number, and date"
        new = "World Health Organization\n" + old + "\nWorld Health Organization"
        self.assertEqual(comparable_text("who-medical-alerts", old),
                         comparable_text("who-medical-alerts", new))
        self.assertNotEqual(comparable_text("fda-drug-safety", old),
                            comparable_text("fda-drug-safety", new))
        self.assertNotEqual(comparable_text("who-medical-alerts", old),
                            comparable_text("who-medical-alerts", old + "\nNew affected lot"))

    def test_who_header_only_change_emits_no_alert_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("critical_guidance_delta.fetch_text", return_value="Alert 3/2026\nProduct A"):
                run(root)

            def updated(url):
                if url == SOURCES[0]["url"]:
                    return "World Health Organization\nAlert 3/2026\nProduct A\nWorld Health Organization"
                return "Alert 3/2026\nProduct A"

            with patch("critical_guidance_delta.fetch_text", side_effect=updated):
                result = run(root)
            self.assertEqual(result["changesDetected"], 0)
            self.assertEqual(result["failuresCount"], 0)

    def test_who_new_alert_survives_header_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("critical_guidance_delta.fetch_text", return_value="Alert 3/2026\nProduct A"):
                run(root)

            def updated(url):
                if url == SOURCES[0]["url"]:
                    return "World Health Organization\nAlert 3/2026\nProduct A\nNew alert 4/2026: Product B"
                return "Alert 3/2026\nProduct A"

            with patch("critical_guidance_delta.fetch_text", side_effect=updated):
                result = run(root)
            self.assertEqual(result["changesDetected"], 1)
            self.assertEqual(result["changes"][0]["sourceKey"], "who-medical-alerts")
            self.assertIn("New alert 4/2026: Product B", result["changes"][0]["evidenceDiff"])
            self.assertEqual(result["changes"][0]["materiality"], "unreviewed")
            self.assertIsNone(result["changes"][0]["medicalAdvice"])

    def test_first_run_creates_baselines(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("critical_guidance_delta.fetch_text", return_value="baseline"):
                result = run(Path(tmp))
            self.assertEqual(result["baselinesCreated"], len(SOURCES))
            self.assertEqual(result["changesDetected"], 0)

    def test_change_is_unreviewed_not_medical_advice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("critical_guidance_delta.fetch_text", return_value="old"):
                run(root)

            count = {"n": 0}
            def changed(url):
                count["n"] += 1
                return "new" if count["n"] == 1 else "old"

            with patch("critical_guidance_delta.fetch_text", side_effect=changed):
                result = run(root)

            event = result["changes"][0]
            self.assertEqual(event["materiality"], "unreviewed")
            self.assertEqual(event["verificationStatus"], "needs-independent-source-review")
            self.assertIsNone(event["medicalAdvice"])


if __name__ == "__main__":
    unittest.main()
