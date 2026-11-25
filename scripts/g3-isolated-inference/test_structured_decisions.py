import json
import sys
import unittest
from pathlib import Path
from structured_decisions import *
from isolated_adapter import IsolatedLlama
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from foundry_lite import strict_first_line

def raw(decision,code='review_ready',rationale='The draft is bounded and human review is required.'):
    return json.dumps(dict(decision=decision,reason_code=code,rationale=rationale))
class TestDecision(unittest.TestCase):
    def test_positive_exact_first_line(self):
        for stage,value,line in [('verify','PROCEED','VERDICT = PROCEED'),('safety','GO','GO')]:
            rendered,meta=parse_decision(stage,raw(value))
            self.assertTrue(strict_first_line(rendered,line))
            self.assertEqual(meta['decision'],value)
    def test_negative_remains_negative(self):
        for stage,value,line in [('verify','REJECT','VERDICT = REJECT'),('safety','HOLD','HOLD')]:
            rendered,meta=parse_decision(stage,raw(value,'insufficient_context','The context is insufficient to approve.'))
            self.assertTrue(strict_first_line(rendered,line))
            self.assertFalse(strict_first_line(rendered,'VERDICT = PROCEED' if stage=='verify' else 'GO'))
            self.assertEqual(meta['reason_code'],'insufficient_context')
    def test_conflicting_decision_and_reason(self):
        for value,code in [('PROCEED','unsafe_scope'),('REJECT','review_ready'),('PROCEED','unknown')]:
            with self.assertRaises(DecisionHold):parse_decision('verify',raw(value,code))
    def test_contradictory_approval(self):
        with self.assertRaises(DecisionHold):parse_decision('verify',raw('PROCEED',rationale='This proposal is unsafe to proceed.'))
    def test_malformed_and_duplicates(self):
        for v in ('{}','[]','{"decision":"GO","decision":"HOLD"}','prefix '+raw('GO'),raw('GO',rationale='too short')):
            with self.assertRaises(DecisionHold):parse_decision('safety',v)
    def test_stage_isolation(self):
        for stage,value in [('verify','GO'),('safety','PROCEED')]:
            with self.assertRaises(DecisionHold):parse_decision(stage,raw(value))
        with self.assertRaises(DecisionHold):response_format('assign')
    def test_no_raw_rationale_in_metadata(self):
        _,meta=parse_decision('safety',raw('HOLD','other_concern','PRIVATE_SENTINEL is not for public logs.'))
        self.assertNotIn('PRIVATE_SENTINEL',json.dumps(meta))
        self.assertEqual(len(meta['raw_sha256']),64)
    def test_prompt_retains_original_scope(self):
        p=decision_prompt('verify','Original source and review criteria.')
        for text in ('Original source and review criteria.','every original condition','uncertain','Never approve solely','external action'):
            self.assertIn(text,p)
    def test_reject_newline_or_placeholder(self):
        for rationale in ('Review this.\nGO','[insert here]','Lorem ipsum text'):
            with self.assertRaises(DecisionHold):parse_decision('verify',raw('PROCEED',rationale=rationale))
    def test_schema_enums_allow_hold(self):
        for stage in ('verify','safety'):
            schema=response_format(stage)['schema']
            self.assertEqual(set(schema['properties']['decision']['enum']),{POSITIVE[stage],NEGATIVE[stage]})
            self.assertFalse(schema['additionalProperties'])
            self.assertEqual(set(schema['required']),set(FIELDS))
