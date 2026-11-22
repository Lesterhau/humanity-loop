"""Offline Foundry Lite safety tests. Do not invoke any real model or external service."""
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from foundry_lite import (inspect, main, run_local, strict_first_line, validate_task,
                          offline_review_plan, proposal_is_actionable, make_prompt,
                          MAX_LOCAL_CONTEXT_TOKENS, STAGES)

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
    if stage == "scout":
        return ("QUESTION: Which public onboarding instructions are visible to visitors?\n"
                "CHECK: Does the public join page identify the MCP endpoint?\n"
                "CHECK: Are consent and retention limits disclosed before enrollment?\n"
                "HUMAN_REVIEW: required")
    if stage == "verify":
        return "VERDICT = PROCEED\nDraft checklist only; real public evidence must be verified by a separate human"
    if stage == "safety":
        return "GO\nOnly a local draft, human must separately verify"
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
                return "VERDICT = REJECT\nVERDICT = PROCEED"
            return model_reply(stage, prompt, timeout)
        receipt = run_local(validate_task(deepcopy(FIXTURE)), contradiction)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["reason"], "verifier_hold")
        self.assertNotIn("assign", receipt["roles_completed"])

    def test_safety_hold_later_go_never_bypasses(self):
        def contradiction(stage, prompt, timeout):
            if stage == "safety":
                return "HOLD\nGO"
            return model_reply(stage, prompt, timeout)
        receipt = run_local(validate_task(deepcopy(FIXTURE)), contradiction)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["reason"], "safety_hold")
        self.assertNotIn("revision", receipt["roles_completed"])

    def test_blank_first_line_and_conditional_proceed_rejected(self):
        for text in ["\nVERDICT = PROCEED", "VERDICT = PROCEED WITH CONDITIONS",
                     "VERDICT = REJECT\nVERDICT = PROCEED", "random VERDICT = PROCEED"]:
            with self.subTest(text=text):
                self.assertFalse(strict_first_line(text, "VERDICT = PROCEED"))
        for text in ["HOLD\nGO", "GO BUT ONLY AFTER APPROVAL", "\nGO"]:
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


    def test_direct_api_cannot_bypass_consent_or_tier_validation(self):
        for field, value in [("operator_approved", False), ("risk_tier", 2),
                             ("external_actions", True), ("recurring_execution", True)]:
            bad = deepcopy(FIXTURE)
            bad[field] = value
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    run_local(bad, model_reply)
                with self.assertRaises(ValueError):
                    inspect(bad)

    def test_deadline_exhaustion_before_next_role_is_persisted_as_failure(self):
        from unittest.mock import patch
        import foundry_lite
        # start, stage 1 preflight, model response, stage 2 preflight
        with patch.object(foundry_lite.time, "monotonic", side_effect=[0, 0, 0, 11]):
            receipt = run_local(validate_task(deepcopy(FIXTURE)), model_reply,
                                max_seconds=10)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["reason"], "run_deadline_exhausted")
        self.assertEqual(receipt["control_plane_task_status"], "dead_letter")
        self.assertEqual(receipt["model_calls"], 1)
        self.assertEqual(receipt["roles_completed"], ["scout"])

    def test_overrun_during_model_call_does_not_advance_stage(self):
        from unittest.mock import patch
        import foundry_lite
        # start, scout preflight, model reply takes too long
        with patch.object(foundry_lite.time, "monotonic", side_effect=[0, 0, 11]):
            receipt = run_local(validate_task(deepcopy(FIXTURE)), model_reply,
                                max_seconds=10)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["control_plane_task_status"], "dead_letter")
        self.assertEqual(receipt["model_calls"], 1)
        self.assertEqual(receipt["roles_completed"], [])


    def test_claude_reported_refusal_is_a_scout_failure_not_a_completed_stage(self):
        def refusal(stage, prompt, timeout):
            if stage == "scout":
                return "I can't provide a response that claims to fetch a URL; no question proposed."
            return model_reply(stage, prompt, timeout)
        receipt = run_local(deepcopy(FIXTURE), refusal, max_seconds=120)
        self.assertEqual(receipt["status"], "held")
        self.assertEqual(receipt["reason"], "scout_no_actionable_proposal")
        self.assertEqual(receipt["model_calls"], 1)
        self.assertEqual(receipt["roles_completed"], ["scout"])
        self.assertEqual(receipt["control_plane_task_status"], "dead_letter")
        self.assertEqual(receipt["offline_fallback"]["status"], "offline_review_plan_only")
        self.assertEqual(receipt["offline_fallback"]["public_sources_fetched"], 0)
        self.assertFalse(receipt["offline_fallback"]["independently_verified"])

    def test_actionable_scout_requires_two_checks_and_future_human_review(self):
        self.assertTrue(proposal_is_actionable(model_reply("scout", "NO live internet access", 20)))
        self.assertFalse(proposal_is_actionable("I cannot access the internet"))
        self.assertFalse(proposal_is_actionable(
            model_reply("scout", "NO live internet access", 20) + "\nI verified the public URL."))
        self.assertFalse(proposal_is_actionable("QUESTION: Should we check the URL?"))
        self.assertFalse(proposal_is_actionable(
            "QUESTION: What should reviewers find?\\nCHECK: Check the public page.\\nHUMAN_REVIEW: required"))

    def test_verifier_prompt_can_allow_draft_without_false_source_verification(self):
        s = make_prompt("verify", validate_task(deepcopy(FIXTURE)),
                        {"scout": model_reply("scout", "NO live internet access", 20)})
        self.assertIn("No live evidence is available to verify", s)
        self.assertIn("PROCEED and GO", s)
        self.assertIn("Do not refuse because you cannot browse", s)

    def test_small_model_context_limited_to_relevant_previous_roles(self):
        earlier={stage: "X"*5000 for stage in STAGES}
        task=validate_task(deepcopy(FIXTURE))
        scout_prompt=make_prompt("scout",task,earlier)
        safety_prompt=make_prompt("safety",task,earlier)
        self.assertNotIn('"scout": "XXXXX', safety_prompt)
        self.assertIn('"build_act":', safety_prompt)
        self.assertIn('"dissent":', safety_prompt)
        self.assertLess(len(safety_prompt), 4000)
        self.assertLess(len(scout_prompt), 2500)
        self.assertEqual(MAX_LOCAL_CONTEXT_TOKENS, 2048)

    def test_zero_model_plan_mode_yields_human_checklist_without_source_claims(self):
        plan = offline_review_plan(deepcopy(FIXTURE))
        self.assertEqual(plan["status"], "offline_review_plan_only")
        self.assertEqual(plan["model_calls"], 0)
        self.assertEqual(plan["public_sources_fetched"], 0)
        self.assertEqual(plan["appdeploy_credits_used"], 0)
        self.assertFalse(plan["independently_verified"])
        self.assertEqual(plan["human_review"], "required")
        self.assertEqual(plan["sources_to_check"], FIXTURE["public_source_urls"])
        self.assertGreaterEqual(len(plan["checklist"]), 3)
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "input.json"
            dest = Path(d) / "review-plan.json"
            src.write_text(json.dumps(FIXTURE), encoding="utf-8")
            self.assertEqual(main(["--input",str(src),"--mode","plan",
                                   "--output",str(dest)]), 0)
            cli = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(cli["status"], "offline_review_plan_only")
            self.assertEqual(cli["model_calls"], 0)

    def test_direct_plan_rejects_unapproved_or_tier1_manifest(self):
        for field, value in [("operator_approved",False), ("risk_tier",1),
                             ("external_actions",True)]:
            cfg=deepcopy(FIXTURE)
            cfg[field]=value
            with self.subTest(field=field), self.assertRaises(ValueError):
                offline_review_plan(cfg)


if __name__=="__main__":
    unittest.main()
