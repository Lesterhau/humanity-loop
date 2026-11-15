"""Offline, synthetic-only regression tests for human-in-the-loop manual pilot intake."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triage_manual_pilot import triage, main

GOOD = {
    "task_type": "public_page_check",
    "outcome": "no_issue_found",
    "human_checked": True,
    "web_access": "live",
    "source_check": "independently_checked",
    "source_urls": ["https://www.usa.gov/benefits", "https://www.ssa.gov/retirement"],
    "observation": "The official public navigation path works as described.",
    "limitations": "Only one retirement route was reviewed.",
}


class ManualTriageTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(json.dumps(GOOD))

    def review(self, origin="outside_email"):
        return triage(self.case, trusted_origin=origin)

    def test_valid_negative_never_accepted_or_counted_as_node(self):
        result = self.review()
        self.assertEqual(result["status"], "human_review_required")
        self.assertFalse(result["accepted"])
        self.assertFalse(result["registered_node"])
        self.assertFalse(result["public_benefit_verified"])
        self.assertEqual(result["outcome_class"], "no_issue_found")
        self.assertEqual(result["blockers"], [])

    def test_trusted_owner_provenance_separate(self):
        result = self.review("owner_test")
        self.assertEqual(result["origin_class"], "owner_test")
        self.assertIn("owner_test_not_independent_participant", result["warnings"])

    def test_untrusted_sender_claim_cannot_grant_outside_origin(self):
        self.case["origin"] = "outside_email"
        self.case["sender"] = "Independent Reviewer"
        result = triage(self.case)
        self.assertEqual(result["origin_class"], "unknown")
        self.assertIn("sender_provenance_must_be_checked_privately", result["warnings"])

    def test_invalid_provenance_denied(self):
        result = triage(self.case, trusted_origin="accepted_independent")
        self.assertIn("invalid_trusted_origin", result["blockers"])
        self.assertEqual(result["origin_class"], "unknown")

    def test_human_checked_must_be_boolean(self):
        self.case["human_checked"] = "yes"
        self.assertIn("human_check_flag_required", self.review()["blockers"])

    def test_possible_issue_without_human_check_blocked(self):
        self.case["outcome"] = "possible_issue"
        self.case["human_checked"] = False
        self.assertIn("human_confirmation_missing_for_issue", self.review()["blockers"])

    def test_possible_issue_without_independent_source_warned(self):
        self.case["outcome"] = "possible_issue"
        self.case["source_check"] = "not_checked"
        self.assertIn("independent_source_review_required", self.review()["warnings"])
        self.assertFalse(self.review()["accepted"])

    def test_possible_issue_with_confirmed_source_still_needs_human_review(self):
        self.case["outcome"] = "possible_issue"
        result = self.review()
        self.assertFalse(result["accepted"])
        self.assertIn("reviewer_independence_not_verified", result["warnings"])

    def test_blocked_model_not_automatically_source_defect(self):
        self.case["outcome"] = "unable_to_verify"
        self.case["human_checked"] = False
        self.case["web_access"] = "blocked"
        result = self.review()
        self.assertEqual(result["blockers"], [])
        self.assertIn("model_access_limitation_not_public_site_failure", result["warnings"])
        self.assertIn("inconclusive_test_not_a_source_defect", result["warnings"])

    def test_conflicting_human_check_in_blocked_report(self):
        self.case["outcome"] = "unable_to_verify"
        self.assertIn("unable_outcome_conflicts_with_human_check", self.review()["warnings"])

    def test_negative_without_human_check_is_not_trusted(self):
        self.case["human_checked"] = False
        self.assertIn("negative_finding_not_human_checked", self.review()["warnings"])

    def test_bad_outcome_or_access_type_cannot_crash(self):
        self.case["outcome"] = ["accepted"]
        self.case["web_access"] = {"live": True}
        result = self.review()
        self.assertIn("invalid_outcome", result["blockers"])
        self.assertIn("web_access_not_classified", result["warnings"])

    def test_untrusted_source_type_cannot_crash(self):
        self.case["source_urls"] = [42]
        self.assertIn("invalid_source_url", self.review()["blockers"])

    def test_local_or_private_source_blocked(self):
        self.case["source_urls"] = ["http://127.0.0.1/private"]
        self.assertIn("nonpublic_source_url", self.review()["blockers"])

    def test_source_url_credentials_blocked(self):
        self.case["source_urls"] = ["https://bob:secrets@example.org/"]
        self.assertIn("credentials_in_source_url", self.review()["blockers"])

    def test_sensitive_url_query_blocked(self):
        self.case["source_urls"] = ["https://example.org/go?access_token=verysecret"]
        self.assertIn("sensitive_query_in_source_url", self.review()["blockers"])

    def test_missing_source_blocked_even_for_negative(self):
        self.case["source_urls"] = []
        self.assertIn("source_urls_missing_or_too_many", self.review()["blockers"])

    def test_too_many_urls_blocked(self):
        self.case["source_urls"] = ["https://www.usa.gov/benefits"] * 11
        self.assertIn("source_urls_missing_or_too_many", self.review()["blockers"])

    def test_secret_is_flagged_but_not_echoed(self):
        self.case["observation"] = "node_token=aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        result = json.dumps(self.review())
        self.assertIn("possible_secret_present", result)
        self.assertNotIn("aaaaaaaaaaaaaaaaaaaaaaaaaaaa", result)

    def test_private_email_warned_but_not_echoed(self):
        self.case["observation"] = "contact someone@example.com"
        result = json.dumps(self.review())
        self.assertIn("possible_personal_data_present", result)
        self.assertNotIn("someone@example.com", result)

    def test_missing_or_oversized_observation_blocked(self):
        self.case["observation"] = "x" * 3000
        self.assertIn("observation_missing_or_oversized", self.review()["blockers"])

    def test_missing_limitations_warns(self):
        self.case["limitations"] = ""
        self.assertIn("limitations_missing_or_oversized", self.review()["warnings"])

    def test_source_conflict_blocks(self):
        self.case["source_check"] = "conflicting"
        self.assertIn("source_conflict_needs_manual_resolution", self.review()["blockers"])

    def test_unknown_source_review_blocks_invalid_value(self):
        self.case["source_check"] = ["independently_checked"]
        self.assertIn("source_check_invalid", self.review()["blockers"])

    def test_wrong_task_type_blocked(self):
        self.case["task_type"] = "private_data_extraction"
        self.assertIn("wrong_task_type", self.review()["blockers"])

    def test_non_object_report_fail_closed(self):
        result = triage(["fake"], trusted_origin="outside_email")
        self.assertFalse(result["accepted"])
        self.assertIn("invalid_record", result["blockers"])

    def test_input_oversized_cli_errors_with_no_data_leak(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp, "oversized.json")
            path.write_text(json.dumps({"sensitive": "x" * 34_000}), encoding="utf-8")
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                rc = main([str(path)])
            self.assertEqual(rc, 2)
            self.assertNotIn("sensitive", buffer.getvalue())
            self.assertIn("input_unavailable_invalid_or_oversized", buffer.getvalue())

    def test_valid_cli_json_safe_output(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp, "redacted.json")
            path.write_text(json.dumps(self.case), encoding="utf-8")
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                rc = main([str(path), "--trusted-origin", "outside_email"])
            self.assertEqual(rc, 0)
            result = json.loads(buffer.getvalue())
            self.assertFalse(result["accepted"])
            self.assertEqual(result["origin_class"], "outside_email")
            self.assertNotIn("official public navigation", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
