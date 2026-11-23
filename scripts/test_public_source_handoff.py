"""Offline G3: convert real saved snapshot to strictly unreviewed Foundry plan."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from public_source_handoff import make_review_candidate, main
from foundry_lite import offline_review_plan, validate_task, main as foundry_main
from foundry_source_evidence import validate_source_packet

ROOT=Path(__file__).resolve().parent.parent
SNAPSHOT_PATH=ROOT/"runtime/mission/2026-11-23-ot013-official-html-snapshot.json"
TASK_PATH=ROOT/"foundry-lite/fixtures/ot013-pk-climate-review.json"
SNAPSHOT=json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
TASK=json.loads(TASK_PATH.read_text(encoding="utf-8"))
NOW=datetime(2026,11,23,0,30,tzinfo=timezone.utc)

class HandoffTests(unittest.TestCase):
    def candidate(self,snapshot=None,task=None):
        return make_review_candidate(deepcopy(SNAPSHOT if snapshot is None else snapshot),
                                     deepcopy(TASK if task is None else task),now=NOW)

    def test_actual_archived_live_snapshot_produces_unreviewed_source_packet(self):
        p=self.candidate()
        self.assertEqual(p["case_id"],"OT-013")
        self.assertEqual(p["country"],"PK")
        self.assertEqual(p["languages"],["en"])
        self.assertFalse(p["fixture_only"])
        self.assertEqual(p["review_state"],"pending_independent_review")
        self.assertEqual(len(p["observations"]),2)
        self.assertEqual(p["arithmetic_checks"][0]["source_index"],1)
        normalized=validate_source_packet(p,validate_task(TASK),now=NOW)
        self.assertEqual(normalized["arithmetic_checks"][0]["calculated_percent_1dp"],"71.8")
        self.assertFalse(normalized["eligible_for_win_ledger"])
        self.assertFalse(normalized["externally_verified"])
        self.assertEqual(normalized["external_actions"],0)
        self.assertEqual(normalized["model_calls"],0)

    def test_actual_snapshot_to_foundry_review_plan_without_model_calls(self):
        p=self.candidate()
        plan=offline_review_plan(TASK,p)
        self.assertEqual(plan["status"],"offline_review_plan_only")
        self.assertEqual(plan["model_calls"],0)
        self.assertEqual(plan["public_sources_fetched"],0)
        self.assertFalse(plan["independently_verified"])
        self.assertEqual(plan["source_candidate"]["country"],"PK")
        self.assertFalse(plan["source_candidate"]["eligible_for_win_ledger"])
        self.assertEqual(plan["source_candidate"]["arithmetic_checks"][0]["calculated_percent_1dp"],"71.8")

    def test_reject_forged_country_url_and_case(self):
        for key,val in [
            ("case_id","OT-003"),
            ("country","US"),
            ("languages",["en","es"]),
            ("source_url","https://another.example.org/")
        ]:
            s=deepcopy(SNAPSHOT);s[key]=val
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,"handoff_snapshot_context_mismatch"):
                self.candidate(snapshot=s)

    def test_reject_missing_human_review_or_added_external_write(self):
        for key,val in [
            ("independently_reviewed",True),("confirmed_public_correction",True),
            ("eligible_for_win_ledger",True),("external_write_actions",1),
            ("model_calls",1),("scheduled",True)
        ]:
            s=deepcopy(SNAPSHOT);s[key]=val
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,"handoff_must_be_unreviewed_read_only"):
                self.candidate(snapshot=s)

    def test_reject_fake_hash_or_math_or_time(self):
        cases=[
            (("raw_sha256","Z"*64),"handoff_digest_invalid"),
            (("observed_at_utc","2030-01-01T00:00:00Z"),"handoff_timestamp_invalid"),
            (("http_status",302),"handoff_unrecognized_retrieval"),
        ]
        for (key,value),error in cases:
            s=deepcopy(SNAPSHOT);s[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,error):
                self.candidate(snapshot=s)
        s=deepcopy(SNAPSHOT);s["arithmetic"]["computed_percent_1dp"]="81.6"
        with self.assertRaisesRegex(ValueError,"handoff_invalid_arithmetic"):
            self.candidate(snapshot=s)

    def test_no_source_citation_if_required_excerpts_absent(self):
        s=deepcopy(SNAPSHOT)
        s["indicators"]["narrative_117"]["observed_in_visible_html"]=False
        with self.assertRaisesRegex(ValueError,"handoff_required_text_unobserved"):
            self.candidate(snapshot=s)

    def test_cli_real_snapshot_to_foundry_cli_plan_is_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet=Path(tmp)/"candidate.json";plan=Path(tmp)/"plan.json"
            self.assertEqual(main(["--task",str(TASK_PATH),"--snapshot",str(SNAPSHOT_PATH),
                                   "--output",str(packet)]),0)
            self.assertTrue(packet.exists())
            self.assertEqual(foundry_main(["--input",str(TASK_PATH),"--source-packet",str(packet),
                                            "--mode","plan","--output",str(plan)]),0)
            result=json.loads(plan.read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"offline_review_plan_only")
            self.assertEqual(result["model_calls"],0)
            self.assertEqual(result["appdeploy_credits_used"],0)
            self.assertEqual(result["source_candidate"]["arithmetic_checks"][0]["arithmetic_status"],"discrepancy_candidate")
            self.assertFalse(result["independently_verified"])

    def test_output_overwrite_refused_without_mutating_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"packet.json"
            out.write_text("keep-me",encoding="utf-8")
            self.assertEqual(main(["--task",str(TASK_PATH),"--snapshot",str(SNAPSHOT_PATH),
                                   "--output",str(out)]),2)
            self.assertEqual(out.read_text(encoding="utf-8"),"keep-me")

if __name__=="__main__":
    unittest.main()
