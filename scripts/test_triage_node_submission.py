"""Private-content-free tests for the conservative node review triage CLI."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triage_node_submission import triage, main


GOOD = {
    "submission_id": "11111111-1111-4111-8111-111111111111",
    "work_id": "22222222-2222-4222-8222-222222222222",
    "node_id": "33333333-3333-4333-8333-333333333333",
    "status": "quarantined",
    "result": {"finding": "page shows public guidance"},
    "evidence": [{"url": "https://www.cdc.gov/example", "observed_at": "2026-11-08T18:00:00Z"}],
    "uncertainty": "No human response observed",
}


class TriageTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(json.dumps(GOOD))

    def test_valid_never_autoaccepted(self):
        result = triage(self.data, trusted_risk_tier=0)
        self.assertEqual(result["status"], "human_review_required")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["blockers"], [])
        self.assertIn("source_content_not_independently_verified", result["warnings"])

    def test_unknown_risk_requires_check(self):
        self.assertIn("risk_tier_not_verified", triage(self.data)["warnings"])

    def test_non_tier_zero_blocked(self):
        self.assertIn("outside_tier0_review_scope", triage(self.data, trusted_risk_tier=1)["blockers"])

    def test_not_quarantined_blocked(self):
        self.data["status"] = "accepted"
        self.assertIn("not_quarantined", triage(self.data)["blockers"])

    def test_wrong_identifier_blocked(self):
        self.data["work_id"] = "not-a-uuid"
        self.assertIn("missing_or_invalid_work_id", triage(self.data)["blockers"])

    def test_no_sources_warns(self):
        self.data["evidence"] = []
        result = triage(self.data)
        self.assertIn("no_source_urls", result["warnings"])

    def test_nonpublic_ip_blocked(self):
        self.data["evidence"] = [{"url": "http://127.0.0.1:5432/secret"}]
        self.assertIn("nonpublic_source_url", triage(self.data)["blockers"])

    def test_no_embedded_credentials(self):
        self.data["evidence"] = ["https://alice:secret@example.org/"]
        self.assertIn("credentials_in_source_url", triage(self.data)["blockers"])

    def test_query_secret_detected(self):
        self.data["evidence"] = ["https://example.org/page?token=thisisprivate"]
        self.assertIn("sensitive_query_in_source_url", triage(self.data)["blockers"])

    def test_invalid_scheme_rejected(self):
        self.data["evidence"] = ["file:///etc/passwd"]
        self.assertIn("invalid_source_url", triage(self.data)["blockers"])

    def test_private_content_not_in_report(self):
        self.data["result"] = {"text": "node_token=very-private-token-value"}
        report = json.dumps(triage(self.data, trusted_risk_tier=0))
        self.assertNotIn("very-private-token-value", report)
        self.assertIn("possible_secret_in_submission", report)

    def test_structured_result_required(self):
        self.data["result"] = ""
        self.assertIn("missing_structured_result", triage(self.data)["blockers"])

    def test_uncertainty_missing_warns(self):
        self.data["uncertainty"] = ""
        self.assertIn("uncertainty_not_explained", triage(self.data)["warnings"])

    def test_email_warns_without_disclosing(self):
        self.data["result"]["email"] = "someone@example.org"
        result = triage(self.data)
        self.assertIn("possible_personal_data_review", result["warnings"])
        self.assertNotIn("someone@example.org", json.dumps(result))

    def test_bad_json_cli_fails_safely(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp, "invalid.json")
            path.write_text("{ definitely secret")
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                code = main([str(path)])
            self.assertEqual(code, 2)
            self.assertNotIn("definitely secret", capture.getvalue())

    def test_too_many_evidence_items_warns(self):
        self.data["evidence"] = ["https://example.org"] * 51
        self.assertIn("evidence_truncated_for_triage", triage(self.data)["warnings"])


if __name__ == "__main__":
    unittest.main()
