"""Offline review-packet integrity preflight. Never grants independent acceptance."""
import hashlib
import json
import re
import sys
from pathlib import Path
from isolated_adapter import STAGES,MODEL_ID,MODEL_SHA256,MODEL_BYTES,IMAGE,MAX_PREDICT,MAX_TOTAL_SECONDS,MAX_CONTEXT
from structured_scout import parse_scout
from structured_decisions import parse_decision

MAX_PACKET_BYTES=250000
TASK_ID='hl-foundry-lite-onboarding-20261118'

class ReviewHold(ValueError):
    pass

def require(ok,code):
    if not ok:
        raise ReviewHold(code)

def unique_object(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'duplicate_json_key')
        result[k]=v
    return result

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def preflight(data,expected_sha256):
    require(type(data) is bytes and 0<len(data)<=MAX_PACKET_BYTES,'packet_size')
    require(isinstance(expected_sha256,str) and re.fullmatch('[0-9a-f]{64}',expected_sha256) is not None,'expected_digest_required')
    require(digest(data)==expected_sha256,'packet_digest_mismatch')
    try:
        r=json.loads(data,object_pairs_hook=unique_object)
    except (UnicodeError,json.JSONDecodeError):
        raise ReviewHold('invalid_json') from None
    require(isinstance(r,dict),'packet_type')
    require(type(r.get('review_packet_version')) is int and r['review_packet_version']==1,'unsupported_packet_version')
    require(r.get('task_id')==TASK_ID and r.get('status')=='draft_review_pending' and r.get('reason') is None,'wrong_fixture_or_status')
    require(r.get('inference_acceptance_candidate') is True and r.get('control_plane_task_status')=='completed','incomplete_execution')
    require(type(r.get('model_calls')) is int and r['model_calls']==8 and r.get('roles_completed')==list(STAGES),'wrong_stage_count')
    require(r.get('model_id')==MODEL_ID and r.get('model_sha256')==MODEL_SHA256 and r.get('model_bytes')==MODEL_BYTES and r.get('container_image')==IMAGE,'wrong_model_pin')
    for k in ('independent_review_completed','independently_verified','canonical_supabase_claimed','provider_account_cap_verified','eligible_for_win_ledger','scheduled'):
        require(r.get(k) is False,'invalid_acceptance_claim')
    for k in ('external_actions','appdeploy_credits_used'):
        require(type(r.get(k)) is int and r[k]==0,'nonzero_or_untrusted_activity')
    require(r.get('human_review')=='required' and r.get('adapter_failure') is None,'review_or_failure_state')
    raw=r.get('raw_stage_outputs'); drafts=r.get('role_drafts'); receipts=r.get('stage_token_receipts')
    require(isinstance(raw,dict) and isinstance(drafts,dict) and tuple(raw)==STAGES and tuple(drafts)==STAGES,'stage_content_missing_or_unordered')
    require(isinstance(receipts,list) and len(receipts)==8,'missing_token_receipts')
    elapsed=0
    for stage,rec in zip(STAGES,receipts):
        text=raw[stage]
        require(isinstance(text,str) and 0<len(text.strip())<=8000,'invalid_raw_text')
        require(isinstance(rec,dict) and rec.get('stage')==stage and rec.get('finish_reason')=='stop','invalid_stage_receipt')
        nums=[rec.get(k) for k in ('input_tokens','output_tokens','total_tokens','elapsed_ms','call_limit_ms')]
        require(all(type(x) is int for x in nums),'invalid_stage_numbers')
        i,o,total,ms,limit=nums
        require(0<i<=MAX_CONTEXT and 0<o<=MAX_PREDICT and total==i+o<=MAX_CONTEXT,'token_bounds')
        # Millisecond rounding can differ by 1 ms from the floored call limit.
        require(0<=ms<=limit+1 and 0<limit<=45000,'call_deadline')
        elapsed+=ms
        if stage=='scout':
            try: rendered=parse_scout(text)
            except ValueError: raise ReviewHold('scout_parse') from None
            m=r.get('scout_diagnostic')
            require(isinstance(m,dict) and m.get('upstream_pass') is True and m.get('structured_pass') is True and m.get('raw_sha256')==digest(text.encode()),'scout_diagnostic')
        elif stage in ('verify','safety'):
            try: rendered,meta=parse_decision(stage,text)
            except ValueError: raise ReviewHold('decision_parse') from None
            decisions=r.get('decision_diagnostics')
            require(isinstance(decisions,dict),'missing_decisions')
            m=decisions.get(stage)
            require(isinstance(m,dict) and m.get('format_pass') is True and m.get('raw_sha256')==meta['raw_sha256'] and m.get('decision')==meta['decision']==('PROCEED' if stage=='verify' else 'GO') and m.get('reason_code')==meta['reason_code'],'decision_mismatch_or_hold')
        else:
            rendered=text
        require(drafts[stage]==rendered,'draft_projection_mismatch')
    require(elapsed<=MAX_TOTAL_SECONDS*1000+8,'aggregate_deadline')
    return {'packet_sha256':expected_sha256,'integrity_preflight':'passed','stages':8,'review_status':'pending_separate_human','independent_review_completed':False,'release_authorized':False,'eligible_for_win_ledger':False}

def main():
    if len(sys.argv)!=3:
        raise SystemExit('usage: review_packet.py PRIVATE_RECEIPT_FILE TRUSTED_CI_RECEIPT_SHA256')
    try:
        with Path(sys.argv[1]).open('rb') as f:
            data=f.read(MAX_PACKET_BYTES+1)
        summary=preflight(data,sys.argv[2])
    except ReviewHold as e:
        print(json.dumps({'integrity_preflight':'held','reason':str(e),'independent_review_completed':False}))
        return 2
    except (OSError,ValueError,TypeError):
        print(json.dumps({'integrity_preflight':'held','reason':'unreadable_or_invalid_packet','independent_review_completed':False}))
        return 2
    print(json.dumps(summary))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
