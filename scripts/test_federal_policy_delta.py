#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from federal_policy_delta import SOURCES, digest, normalize_html, run


class FederalPolicyDeltaTests(unittest.TestCase):
    def test_normalize_html_excludes_scripts_and_styles(self):
        html = """
        <html><head><style>.x{display:none}</style><script>noise()</script></head>
        <body><h1>Official Policy</h1><p>Visible text.</p></body></html>
        """
        self.assertEqual(normalize_html(html), "Official Policy Visible text.")

    def test_digest_is_stable(self):
        self.assertEqual(digest("abc"), digest("abc"))
        self.assertNotEqual(digest("abc"), digest("abd"))

    def test_first_run_creates_baselines_without_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("federal_policy_delta.fetch_text", return_value="baseline"):
                result = run(Path(tmp))
            self.assertEqual(result["baselinesCreated"], len(SOURCES))
            self.assertEqual(result["changesDetected"], 0)
            self.assertEqual(result["failuresCount"], 0)

    def test_second_run_detects_text_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("federal_policy_delta.fetch_text", return_value="baseline"):
                run(root)

            calls = {"count": 0}

            def changed(url):
                calls["count"] += 1
                return "changed text" if calls["count"] == 1 else "baseline"

            with patch("federal_policy_delta.fetch_text", side_effect=changed):
                result = run(root)

            self.assertEqual(result["changesDetected"], 1)
            self.assertEqual(result["changes"][0]["reviewStatus"], "needs-neutral-human-or-agent-review")
            self.assertIsNone(result["changes"][0]["legalConclusion"])


if __name__ == "__main__":
    unittest.main()
