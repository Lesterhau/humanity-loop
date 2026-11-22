"""G3/G4 offline cross-border source candidate contract and Foundry adapter tests."""
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from foundry_lite import validate_task, offline_review_plan, make_prompt, run_local, main
from foundry_source_evidence import validate_source_packet

ROOT=Path(__file__).resolve().parent.parent / "foundry-lite" / "fixtures"
NOW=datetime(2026,11,22,21,0,tzinfo=timezone.utc)

def fixture(case):
    prefix="ot003-us-bilingual" if case=="US" else "ot013-pk-climate"
    task=json.loads((ROOT/(prefix+"-review.json")).read_text(encoding="utf-8"))
    packet=json.loads((ROOT/(prefix+"-source-candidate.json")).read_text(encoding="utf-8"))
    return validate_task(task),packet

def model(stage,prompt,timeout):
    assert "NO live internet access" in prompt
    assert 0 < timeout <= 45
    if stage=="scout":
        return ("QUESTION: What public text is currently displayed on the primary page?\n"
                "CHECK: Compare today's public statement to the original report.\n"
                "CHECK: Record unknown source limitations and separate language-review needs.\n"
                "HUMAN_REVIEW: required")
    if stage=="verify":
        return "VERDICT = PROCEED\nThis permits a draft only; no source independently checked"
    if stage=="safety":
        return "GO\nOnly a no-tools local draft for a later independent reviewer"
    return "Draft only, no observed source evidence or external action"

class SourceCandidateTests(unittest.TestCase):
    def check(self,case,raw=None,task=None):
        t,p=fixture(case)
        return validate_source_packet(deepcopy(p if raw is None else raw),
                                      t if task is None else task,now=NOW)

    def test_two_real_country_source_candidates_staged_not_accepted(self):
        for case,country in [("US","US"),("PK","PK")]:
            with self.subTest(case=case):
                r=self.check(case)
                self.assertEqual(r["country"],country)
                self.assertEqual(r["review_state"],"pending_independent_review")
                self.assertEqual(r["source_claim_status"],"operator_supplied_not_independently_verified")
                self.assertFalse(r["externally_verified"])
                self.assertFalse(r["eligible_for_win_ledger"])
                self.assertTrue(r["fixture_only"])
                self.assertEqual(r["external_actions"],0)
                self.assertEqual(r["model_calls"],0)

    def test_pakistan_84_divided_by_117_is_71_point_8_not_81_point_6(self):
        r=self.check("PK")
        check=r["arithmetic_checks"][0]
        self.assertEqual(check["calculated_percent_1dp"],"71.8")
        self.assertEqual(check["claimed_percent"],"81.6")
        self.assertEqual(check["arithmetic_status"],"discrepancy_candidate")
        self.assertFalse(check["independent_source_verification"])
        self.assertIn("not establish the underlying count",check["interpretation"])

    def test_us_two_languages_require_qualified_human_review(self):
        r=self.check("US")
        self.assertEqual(r["languages"],["en","es"])
        self.assertTrue(r["language_competence_required"])
        self.assertEqual(len(r["observations"]),2)

    def test_country_and_case_cannot_be_swapped(self):
        for change in [{"country":"US"},{"case_id":"OT-003"},{"languages":["en","es"]}]:
            t,p=fixture("PK")
            p.update(change)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError,"packet_jurisdiction_mismatch"):
                validate_source_packet(p,t,now=NOW)

    def test_packet_requires_country_language_case_in_task(self):
        t,p=fixture("PK")
        t.pop("country")
        with self.assertRaisesRegex(ValueError,"task_jurisdiction_not_declared"):
            validate_source_packet(p,t,now=NOW)

    def test_unlisted_source_or_private_host_rejected(self):
        t,p=fixture("PK")
        p["observations"][0]["source_url"]="https://another.example.org/unapproved"
        with self.assertRaisesRegex(ValueError,"source_not_approved_in_task"):
            validate_source_packet(p,t,now=NOW)
        p["observations"][0]["source_url"]="https://127.0.0.1/internal"
        with self.assertRaisesRegex(ValueError,"numeric_source_host_forbidden"):
            validate_source_packet(p,t,now=NOW)

    def test_future_timestamp_rejected(self):
        t,p=fixture("PK")
        p["observations"][0]["observed_at_utc"]="2026-12-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError,"future_observation_refused"):
            validate_source_packet(p,t,now=NOW)

    def test_missing_external_review_and_autopublish_rejected(self):
        t,p=fixture("PK")
        for k,val,error in [("review_state","accepted","review_not_preapproved"),
                             ("consent_to_publish",True,"no_external_actions"),
                             ("external_actions",True,"no_external_actions")]:
            bad=deepcopy(p);bad[k]=val
            with self.subTest(k=k),self.assertRaisesRegex(ValueError,error):
                validate_source_packet(bad,t,now=NOW)

    def test_source_snippet_limit_and_secret_signals(self):
        t,p=fixture("PK")
        p["observations"][0]["excerpt"]="X"*710
        with self.assertRaisesRegex(ValueError,"invalid_observation_excerpt"):
            validate_source_packet(p,t,now=NOW)
        p["observations"][0]["excerpt"]="private data password=abc"
        with self.assertRaisesRegex(ValueError,"sensitive_excerpt_forbidden"):
            validate_source_packet(p,t,now=NOW)

    def test_numeric_denominator_and_claim_bounded(self):
        t,p=fixture("PK")
        for part,whole,claimed in [(84,0,81.6),(118,117,81.6),(84,117,120)]:
            bad=deepcopy(p)
            bad["arithmetic_checks"][0].update(part=part,whole=whole,claimed_percent=claimed)
            with self.subTest(whole=whole,part=part,claimed=claimed),self.assertRaisesRegex(ValueError,"invalid_arithmetic_range"):
                validate_source_packet(bad,t,now=NOW)

    def test_plan_mode_creates_review_questions_and_math_without_inference(self):
        t,p=fixture("PK")
        r=offline_review_plan(t,p)
        self.assertEqual(r["status"],"offline_review_plan_only")
        self.assertEqual(r["model_calls"],0)
        self.assertFalse(r["independently_verified"])
        self.assertEqual(r["source_candidate"]["country"],"PK")
        self.assertEqual(r["source_candidate"]["arithmetic_checks"][0]["calculated_percent_1dp"],"71.8")
        self.assertFalse(r["source_candidate"]["eligible_for_win_ledger"])

    def test_prompt_includes_staged_evidence_but_disclaims_source_verification(self):
        t,p=fixture("PK")
        prepared=validate_source_packet(p,t,now=NOW)
        out=make_prompt("verify",t,{"scout":"proposed question only"},prepared)
        self.assertIn("UNVERIFIED SOURCE CANDIDATES",out)
        self.assertIn('"country": "PK"',out)
        self.assertIn("source review",out)
        self.assertIn("84 of the 117",out)

    def test_model_run_still_labels_countries_unverified_and_no_external_claims(self):
        t,p=fixture("PK")
        r=run_local(t,model,max_seconds=120,source_packet=p)
        self.assertEqual(r["status"],"draft_review_pending")
        self.assertEqual(r["model_calls"],8)
        self.assertEqual(r["source_candidate_status"],"operator_supplied_not_independently_verified")
        self.assertFalse(r["independently_verified"])
        self.assertEqual(r["external_actions"],0)
        self.assertEqual(r["appdeploy_credits_used"],0)
        self.assertEqual(r["offline_fallback"]["source_candidate"]["country"],"PK")

    def test_cli_plan_packet_without_llm_or_network(self):
        paths=["ot013-pk-climate-review.json","ot013-pk-climate-source-candidate.json"]
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"out.json"
            self.assertEqual(main(["--input",str(ROOT/paths[0]),"--source-packet",str(ROOT/paths[1]),
                                   "--mode","plan","--output",str(out)]),0)
            result=json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(result["model_calls"],0)
            self.assertEqual(result["source_candidate"]["country"],"PK")
            self.assertEqual(result["source_candidate"]["arithmetic_checks"][0]["arithmetic_status"],"discrepancy_candidate")

    def test_malformed_cross_border_task_rejected(self):
        t,_=fixture("US")
        t["languages"]=["en","en"]
        with self.assertRaisesRegex(ValueError,"duplicate_languages"):
            validate_task(t)
        t,_=fixture("US")
        t.pop("country")
        with self.assertRaisesRegex(ValueError,"partial_cross_border_context"):
            validate_task(t)

if __name__=="__main__":
    unittest.main()
