"""Offline Foundry Lite safety tests. Do not invoke any real model or external service."""
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from foundry_lite import inspect, main, run_local, strict_first_line, validate_task, STAGES

FIXTURE = {
    "task_id": "test-foundry-001",
    "title": "Draft a public-interest review checklist",
    "scope": "Prepare a bounded checklist using only supplied public-source URLs, with external verification left to a human.",
    "risk_tier": 0,
    "operator_approved": True,
    "external_actions": False,
    "recurring_execution": False,
    "public_source_urls": ["https://www.usa.gov/benefits"],
}


def model_reply(stage, prompt, timeout):
    assert "NO live internet access" in prompt
    assert 0 < timeout <= 45
    if stage == "verify":
        return "VERDICT = PROCEED\\nScoped to unverified public-only checklist"
    if stage == "safety":
        return "GO\\nOnly a local draft, human must separately verify"
    return f"{stage}: review-only draft, no external source independently verified"


class FoundryLiteTests(unittest.TestCase):
    def test_default_preflight_cost_zero_without_model(self):
        receipt = inspect(validate_task(deepcopy(FIXTURE)))
        self.assertEqual(receipt["status"], "preflight_only")
        self.assertEqual(receipt["model_calls"], 0)
        self.assertEqual(receipt["appdeploy_credits_used"], 0)
        self.assertFalse(receipt["independently_verified"])
        self.assertEqual(receipt["public_sources_fetched"], 0)

    def test_end_to_end_eight_role_local_draft_is_not_accepted_public_benefit(self):
        receipt = run_local(validate_task(deepcopy(FIXTURE)), model_reply, max_seconds=120)
        self.assertEqual(receipt["status"], "draft_review_pending")
        self.assertEqual(receipt["roles_completed"], STAGES)
        self.assertEqual(receipt["model_calls"], 8)
        self.assertEqual(receipt["control_plane_task_status"], "completed")
        self.assertFalse(receipt["independently_verified"])
        self.assertFalse(receipt["canonical_supabase_claimed"])
        self.assertEqual(receipt["external_actions"], 0)
        self.assertEqual(receipt["appdeploy_credits_used"], 0)

    def test_verifier_reject_later_proceed_never_bypasses(self):
        def contradiction(stage, prompt, timeout):
            if stage == "verify":
                return "VERDICT = REJECT\\nVERDICT = PROCEED"
            return model_reply(stage, prompt, timeout)
        receipt = run_local(validate_task(deepcopy(FIXTURE)), contradiction)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["reason"], "verifier_hold")
        self.assertNotIn("assign", receipt["roles_completed"])

    def test_safety_hold_later_go_never_bypasses(self):
        def contradiction(stage, prompt, timeout):
            if stage == "safety":
                return "HOLD\\nGO"
            return model_reply(stage, prompt, timeout)
        receipt = run_local(validate_task(deepcopy(FIXTURE)), contradiction)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["reason"], "safety_hold")
        self.assertNotIn("revision", receipt["roles_completed"])

    def test_blank_first_line_and_conditional_proceed_rejected(self):
        for text in ["\\nVERDICT = PROCEED", "VERDICT = PROCEED WITH CONDITIONS",
                     "VERDICT = REJECT\\nVERDICT = PROCEED", "random VERDICT = PROCEED"]:
            with self.subTest(text=text):
                self.assertFalse(strict_first_line(text, "VERDICT = PROCEED"))
        for text in ["HOLD\\nGO", "GO BUT ONLY AFTER APPROVAL", "\\nGO"]:
            self.assertFalse(strict_first_line(text, "GO"))

    def test_stage_failure_fails_closed_and_never_calls_later_roles(self):
        calls = []
        def faulty(stage, prompt, timeout):
            calls.append(stage)
            raise TimeoutError("local model unavailable")
        receipt = run_local(validate_task(deepcopy(FIXTURE)), faulty)
        self.assertEqual(receipt["status"], "held")
        self.assertTrue(receipt["reason"].startswith("local_model_or_stage_failed"))
        self.assertEqual(calls, ["scout"])
        self.assertEqual(receipt["control_plane_task_status"], "dead_letter")

    def test_unsafe_tier_consent_external_and_recurring_inputs_rejected(self):
        for field, value in [
            ("risk_tier", 1), ("risk_tier", True), ("operator_approved", False),
            ("external_actions", True), ("recurring_execution", True),
        ]:
            with self.subTest(field=field, value=value):
                bad = deepcopy(FIXTURE);bad[field] = value
                with self.assertRaises(ValueError):
                    validate_task(bad)

    def test_rejects_nonpublic_or_credential_urls(self):
        for url in [
            "http://www.usa.gov/benefits", "https://127.0.0.1/secrets",
            "https://localhost/private", "https://user:pass@host.example/test",
            "file:///etc/passwd",
        ]:
            with self.subTest(url=url):
                bad = deepcopy(FIXTURE);bad["public_source_urls"] = [url]
                with self.assertRaises(ValueError):
                    validate_task(bad)

    def test_inspect_cli_creates_read_only_receipt_and_no_model(self):
        with tempfile.TemporaryDirectory() as d:
            input_path = Path(d) / "input.json"
            output_path = Path(d) / "output.json"
            input_path.write_text(json.dumps(FIXTURE), encoding="utf-8")
            rc = main(["--input",str(input_path),"--output",str(output_path)])
            self.assertEqual(rc, 0)
            obj = json.loads(output_path.read_text())
            self.assertEqual(obj["status"], "preflight_only")
            self.assertEqual(obj["model_calls"], 0)

    def test_local_mode_requires_explicit_opt_in_and_named_local_model(self):
        with tempfile.TemporaryDirectory() as d:
            input_path = Path(d) / "input.json"
            input_path.write_text(json.dumps(FIXTURE), encoding="utf-8")
            self.assertEqual(main(["--input",str(input_path),"--mode","ollama"]),2)

    def test_role_limit_equals_8_and_fails_on_overlong_output(self):
        self.assertEqual(len(STAGES), 8)
        def too_big(stage, prompt, timeout): return "X" * 8100
        result = run_local(validate_task(deepcopy(FIXTURE)), too_big)
        self.assertEqual(result["status"],"held")
        self.assertEqual(result["control_plane_task_status"],"dead_letter")


if __name__=="__main__":
    unittest.main()
