#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from critical_guidance_delta import SOURCES, diff_excerpt, normalize_html, run


class CriticalGuidanceDeltaTests(unittest.TestCase):
    def test_normalize_html_excludes_nonvisible_script_content(self):
        html = "<html><script>bad()</script><body><h1>FDA Safety</h1><p>Visible.</p></body></html>"
        self.assertEqual(normalize_html(html), "FDA Safety\nVisible.")

    def test_diff_excerpt_retains_added_and_removed_lines(self):
        diff = diff_excerpt("old warning\nkeep", "new warning\nkeep")
        self.assertIn("- old warning", diff)
        self.assertIn("+ new warning", diff)

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
