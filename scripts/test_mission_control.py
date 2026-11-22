"""Offline mission-control gates: structural constraints are not impact verification."""
import json
import sys
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from mission_control import validate_and_select

ROOT=Path(__file__).resolve().parent.parent
CONFIG=json.loads((ROOT/"ops/mission-control.json").read_text(encoding="utf-8"))
WINS=(ROOT/"WIN-LEDGER.md").read_text(encoding="utf-8")

def at(s): return datetime.fromisoformat(s.replace("Z","+00:00"))

class MissionTests(unittest.TestCase):
    def call(self,cfg=None,wins=WINS,at_time="2026-11-22T05:00:00Z"):
        return validate_and_select(deepcopy(CONFIG if cfg is None else cfg),wins,now=at(at_time))

    def test_current_canonical_file_valid_and_wins_ledger_consistent(self):
        r=self.call()
        self.assertTrue(r["validated"])
        self.assertEqual(r["active_gate"],"G2")
        self.assertEqual(r["verified_win_records"],4)
        self.assertEqual(r["focus_case_count"],2)
        self.assertFalse(r["external_volunteers_required"])
        self.assertFalse(r["can_autocontact_institutions"])
        self.assertEqual(r["new_model_calls"],0)
        self.assertEqual(r["new_scheduled_jobs"],0)

    def test_fourth_win_is_irs_partial_outcome_not_a_fifth_or_whole_case_closure(self):
        self.assertIn("WIN-004 — IRS corrected tax-year-2025 EITC",WINS)
        self.assertEqual(WINS.count("## WIN-004"),1)
        cfg=deepcopy(CONFIG)
        self.assertEqual(cfg["milestones"][0]["status"],"achieved")
        self.assertEqual(cfg["milestones"][1]["status"],"active")
        self.assertEqual(cfg["milestones"][1]["measured_case_completions_under_gate"],0)
        self.assertTrue(any("ot005-2026-11-22-irs-outcome-adjudication" in url
                            for url in cfg["milestones"][0]["proof_urls"]))

    def test_no_due_research_does_not_manufacture_activity(self):
        r=self.call()
        self.assertEqual(r["status"],"wait_for_due_or_new_evidence")
        self.assertNotIn("case_id",r)
        self.assertIn("remain idle",r["next_action"])
        self.assertEqual(r["next_due_at"],"2026-11-30T18:00:00+00:00")

    def test_due_one_action_is_read_only_and_case_specific(self):
        r=self.call(at_time="2026-12-01T00:00:00Z")
        self.assertEqual(r["status"],"due")
        self.assertEqual(r["case_id"],"OT-003")
        self.assertEqual(r["action_type"],"read_only_primary_source_check")
        self.assertEqual(r["risk_tier"],0)
        self.assertTrue(r["source_url"].startswith("https://"))
        self.assertFalse(r["can_autocontact_institutions"])

    def test_unverified_win_count_is_rejected(self):
        cfg=deepcopy(CONFIG)
        cfg["baseline"]["verified_outcomes"]=5
        with self.assertRaisesRegex(ValueError,"win_count_mismatch"):
            self.call(cfg)

    def test_duplicate_win_ids_are_rejected(self):
        fake=WINS+"\n## WIN-003 — fabricated duplicate\n"
        with self.assertRaisesRegex(ValueError,"duplicate_win_id"):
            self.call(wins=fake)

    def test_milestone_cannot_be_marked_achieved_without_verification(self):
        cfg=deepcopy(CONFIG)
        cfg["milestones"][0].pop("proof_urls",None)
        with self.assertRaisesRegex(ValueError,"achieved_gate_missing_proof"):
            self.call(cfg)
        cfg=deepcopy(CONFIG)
        cfg["baseline"]["verified_outcomes"]=3
        prior_to_fourth=WINS.split("## WIN-004",1)[0]
        with self.assertRaisesRegex(ValueError,"outcome_gate_without_external_win"):
            self.call(cfg,wins=prior_to_fourth)

    def test_gate_cannot_skip_prerequisite(self):
        cfg=deepcopy(CONFIG)
        cfg["milestones"][0]["status"]="blocked"
        cfg["milestones"][1]["status"]="active"
        with self.assertRaisesRegex(ValueError,"active_gate_before_prerequisite"):
            self.call(cfg)

    def test_dependency_on_recruiting_other_people_is_rejected(self):
        cfg=deepcopy(CONFIG)
        cfg["milestones"][0]["independent_volunteer_required"]=True
        with self.assertRaisesRegex(ValueError,"external_volunteer_is_blocking"):
            self.call(cfg)
        cfg=deepcopy(CONFIG)
        cfg["operating_rules"]["independent_volunteer_blocking"]=True
        with self.assertRaisesRegex(ValueError,"dependency_on_volunteer"):
            self.call(cfg)

    def test_wip_fails_closed_above_two(self):
        cfg=deepcopy(CONFIG)
        cfg["focus_cases"].append(deepcopy(cfg["focus_cases"][0]))
        with self.assertRaisesRegex(ValueError,"invalid_case_wip"):
            self.call(cfg)

    def test_no_routine_repeat_contact_or_fake_case_win(self):
        cfg=deepcopy(CONFIG)
        cfg["focus_cases"][0]["contact_limit_exhausted"]=False
        with self.assertRaisesRegex(ValueError,"unsupervised_repeat_contact"):
            self.call(cfg)
        cfg=deepcopy(CONFIG)
        cfg["focus_cases"][0]["do_not_count_as_win"]=False
        with self.assertRaisesRegex(ValueError,"unverified_case_claimed_as_win"):
            self.call(cfg)

    def test_only_safe_public_source_url_is_admitted(self):
        cfg=deepcopy(CONFIG)
        cfg["focus_cases"][0]["source_url"]="http://127.0.0.1/sensitive"
        with self.assertRaisesRegex(ValueError,"unsafe_public_source"):
            self.call(cfg)

    def test_absolute_no_unapproved_spend_or_high_risk_actions(self):
        cfg=deepcopy(CONFIG)
        cfg["end_state"]["acceptance"]["unapproved_spend_usd"]=1
        with self.assertRaisesRegex(ValueError,"safety_budget_floor_relaxed"):
            self.call(cfg)

    def test_due_cannot_precede_last_contact(self):
        cfg=deepcopy(CONFIG)
        cfg["focus_cases"][0]["next_due_utc"]="2026-11-21T00:00:00Z"
        with self.assertRaisesRegex(ValueError,"review_due_before_last_contact"):
            self.call(cfg)

if __name__=="__main__":
    unittest.main()
