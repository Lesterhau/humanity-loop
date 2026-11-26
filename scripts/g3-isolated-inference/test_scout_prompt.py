import json
import sys
import unittest
from pathlib import Path
from scout_prompt import scout_prompt,scout_diagnostic

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from foundry_lite import proposal_is_actionable,validate_task

GOOD='QUESTION: Can a new operator identify the consent requirement?\nCHECK: Inspect the public page for an explicit retention notice.\nCHECK: Confirm the task limit is shown in the tool documentation.\nHUMAN_REVIEW: required'
class TestScout(unittest.TestCase):
    def test_fixture_prompt_preserves_safety(self):
        task=validate_task(json.loads((ROOT/'foundry-lite/fixtures/public-onboarding-review.json').read_text()))
        p=scout_prompt(task)
        for term in ['no tools or internet','untrusted','No contact','HUMAN_REVIEW: required','exactly four','Never claim']:
            self.assertIn(term,p)
        self.assertIn(task['scope'],p)
        for url in task['public_source_urls']:self.assertIn(url,p)
        with self.assertRaises(ValueError):scout_prompt(dict(task,case_id='OT-013'))
    def test_valid_response(self):
        d=scout_diagnostic(GOOD,proposal_is_actionable)
        self.assertTrue(d['upstream_pass'])
        self.assertTrue(d['distinct_checks'])
        self.assertEqual(d['check_count'],2)
        self.assertFalse(d['placeholder_present'])
    def test_missing_marker_and_short_check(self):
        d=scout_diagnostic(GOOD.replace('HUMAN_REVIEW: required','review later'),proposal_is_actionable)
        self.assertFalse(d['human_review_marker'])
        self.assertFalse(d['upstream_pass'])
        d=scout_diagnostic('QUESTION: A sufficiently long question?\nCHECK: yes\nHUMAN_REVIEW: required',proposal_is_actionable)
        self.assertFalse(d['upstream_pass'])
    def test_false_observation_still_rejected(self):
        d=scout_diagnostic(GOOD+'\nI verified the webpage.',proposal_is_actionable)
        self.assertTrue(d['false_observation_pattern'])
        self.assertFalse(d['upstream_pass'])
    def test_duplicate_checks_and_placeholders(self):
        line='CHECK: Inspect the public page for an explicit retention notice.'
        d=scout_diagnostic(GOOD.replace('CHECK: Confirm the task limit is shown in the tool documentation.',line),proposal_is_actionable)
        self.assertFalse(d['distinct_checks'])
        self.assertTrue(scout_diagnostic(GOOD.replace('Can a new operator identify the consent requirement?','[one concrete question for a future reviewer]'),proposal_is_actionable)['placeholder_present'])
    def test_diagnostic_does_not_leak_text(self):
        d=scout_diagnostic(GOOD+'\nPRIVATE_SENTINEL',proposal_is_actionable)
        self.assertNotIn('PRIVATE_SENTINEL',json.dumps(d))
        self.assertFalse(scout_diagnostic(None,proposal_is_actionable)['upstream_pass'])
