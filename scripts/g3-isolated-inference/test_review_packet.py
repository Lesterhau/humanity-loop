"""Synthetic data only. These tests do not reproduce the deleted CI artifact."""
import copy
import json
import unittest
from review_packet import *
from structured_scout import parse_scout
from structured_decisions import parse_decision

def packet():
    scout=json.dumps({'question':'Can an operator understand the consent requirement?','check_1':'Inspect the join page for an explicit retention notice.','check_2':'Confirm the documentation describes a one-task limit.','human_review':'required'})
    decisions={s:json.dumps({'decision':v,'reason_code':'review_ready','rationale':'The proposed draft remains bounded and requires human review.'}) for s,v in [('verify','PROCEED'),('safety','GO')]}
    raw={s:scout if s=='scout' else decisions[s] if s in decisions else 'Synthetic test text: future reviewer should record evidence.' for s in STAGES}
    drafts=dict(raw)
    drafts['scout']=parse_scout(scout)
    meta={}
    for s in decisions:
        drafts[s],meta[s]=parse_decision(s,raw[s])
    r=dict(review_packet_version=1,task_id=TASK_ID,status='draft_review_pending',reason=None,inference_acceptance_candidate=True,control_plane_task_status='completed',model_calls=8,roles_completed=list(STAGES),model_id=MODEL_ID,model_sha256=MODEL_SHA256,model_bytes=MODEL_BYTES,container_image=IMAGE,human_review='required',adapter_failure=None,raw_stage_outputs=raw,role_drafts=drafts,stage_token_receipts=[dict(stage=s,finish_reason='stop',input_tokens=100,output_tokens=30,total_tokens=130,elapsed_ms=1000,call_limit_ms=45000) for s in STAGES],scout_diagnostic=dict(structured_pass=True,upstream_pass=True,raw_sha256=digest(scout.encode())),decision_diagnostics=meta,external_actions=0,appdeploy_credits_used=0)
    for k in ('independent_review_completed','independently_verified','canonical_supabase_claimed','provider_account_cap_verified','eligible_for_win_ledger','scheduled'):r[k]=False
    return r

def encoded(r):
    return json.dumps(r).encode()
def check(r):
    data=encoded(r)
    return preflight(data,digest(data))

class PacketTests(unittest.TestCase):
    def test_integrity_not_approval(self):
        s=check(packet())
        self.assertEqual(s['integrity_preflight'],'passed')
        self.assertFalse(s['independent_review_completed'])
        self.assertFalse(s['release_authorized'])
        self.assertNotIn('Synthetic test text',json.dumps(s))
    def test_digest_bound(self):
        data=encoded(packet())
        with self.assertRaisesRegex(ReviewHold,'packet_digest_mismatch'):preflight(data,'0'*64)
    def test_no_self_certification(self):
        for field in ('independently_verified','independent_review_completed','eligible_for_win_ledger','provider_account_cap_verified'):
            r=packet();r[field]=True
            with self.assertRaisesRegex(ReviewHold,'invalid_acceptance_claim'):check(r)
    def test_missing_raw_stage_and_order(self):
        r=packet();r['raw_stage_outputs'].pop('assign')
        with self.assertRaisesRegex(ReviewHold,'stage_content'):check(r)
        r=packet();r['raw_stage_outputs']=dict(reversed(list(r['raw_stage_outputs'].items())))
        with self.assertRaisesRegex(ReviewHold,'stage_content'):check(r)
    def test_raw_transformation_tamper(self):
        r=packet();r['role_drafts']['assign']='tampered'
        with self.assertRaisesRegex(ReviewHold,'draft_projection_mismatch'):check(r)
        r=packet();r['scout_diagnostic']['raw_sha256']='0'*64
        with self.assertRaisesRegex(ReviewHold,'scout_diagnostic'):check(r)
    def test_decision_hold_cannot_pass(self):
        r=packet()
        raw=json.dumps({'decision':'HOLD','reason_code':'unsafe_scope','rationale':'Separate human review cannot proceed safely.'})
        r['raw_stage_outputs']['safety']=raw
        r['role_drafts']['safety'],r['decision_diagnostics']['safety']=parse_decision('safety',raw)
        with self.assertRaisesRegex(ReviewHold,'decision_mismatch_or_hold'):check(r)
    def test_receipt_budget_and_type(self):
        for key,value in [('output_tokens',257),('input_tokens',True),('elapsed_ms',46000),('total_tokens',0)]:
            r=packet();r['stage_token_receipts'][0][key]=value
            with self.assertRaises(ReviewHold):check(r)
    def test_wrong_model_or_external_activity(self):
        for key,value in [('model_sha256','0'*64),('external_actions',1),('appdeploy_credits_used',False),('model_calls',True),('task_id','external-case')]:
            with self.assertRaises(ReviewHold):check(dict(packet(),**{key:value}))
    def test_duplicate_json_keys(self):
        raw=b'{"task_id":"x","task_id":"y"}'
        with self.assertRaisesRegex(ReviewHold,'duplicate_json_key'):preflight(raw,digest(raw))
    def test_old_receipt_cannot_substitute(self):
        r=packet();r.pop('review_packet_version')
        with self.assertRaisesRegex(ReviewHold,'unsupported_packet_version'):check(r)
