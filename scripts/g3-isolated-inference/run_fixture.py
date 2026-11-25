"""Existing Foundry Lite fixture and control plane, with pinned dependencies."""
import hashlib
import json
import os
import sys
from pathlib import Path
from isolated_adapter import IsolatedLlama, STAGES, MODEL_SHA256, IMAGE, verify_namespace
from scout_prompt import scout_prompt, scout_diagnostic

PINS={
    'scripts/foundry_lite.py':'bcc0bffa0638d8cacc665363bfe8d4f67244ee62',
    'scripts/foundry_control_plane.py':'081f136842c051874c77fa39f30871e249b17376',
    'scripts/foundry_budget_governor.py':'51a9cfeb89a20d50dab2ca7a306838ab7739e955',
    'scripts/foundry_source_evidence.py':'282012b6cacbccad9b7a72ba6cf3bd1adbf5292f',
    'foundry-lite/fixtures/public-onboarding-review.json':'6124158c4909f8de2604839ee6234b9e422da48f',
}

def main():
    verify_namespace()
    if os.environ.get('HL_APPROVED_ONE_SHOT')!='true' or len(sys.argv)!=3:
        raise SystemExit('explicit one-shot approval and paths required')
    root,out=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()
    if out.exists() or root==out or root in out.parents: raise SystemExit('output must be new and outside repository')
    for path,expected in PINS.items():
        data=(root/path).read_bytes()
        if hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()!=expected:
            raise SystemExit('upstream blob mismatch: '+path)
    task=json.loads((root/'foundry-lite/fixtures/public-onboarding-review.json').read_text())
    if task.get('case_id') is not None: raise SystemExit('external case denied')
    sys.path.insert(0,str(root/'scripts'))
    from foundry_lite import run_local, proposal_is_actionable, validate_task
    task=validate_task(task)
    a=IsolatedLlama()
    scout_meta=None
    def invoke(stage,prompt,timeout):
        nonlocal scout_meta
        response=a(stage,scout_prompt(task) if stage=='scout' else prompt,timeout)
        if stage=='scout':
            scout_meta=scout_diagnostic(response,proposal_is_actionable)
            # Reject copied placeholders and duplicate checks as well as upstream failures.
            # Never normalize, fabricate or repair model-generated text.
            if scout_meta['placeholder_present'] or not scout_meta['distinct_checks']:
                raise ValueError('scout_fixture_quality_hold')
        return response
    result=run_local(task,invoke,max_seconds=240)
    complete=(result['status']=='draft_review_pending' and result['model_calls']==8 and tuple(result['roles_completed'])==STAGES and tuple(x['stage'] for x in a.receipts)==STAGES and result['control_plane_task_status']=='completed')
    result.update(model_provider='isolated_llama_cpp_cpu',inference_acceptance_candidate=complete,stage_token_receipts=a.receipts,adapter_failure=a.last_failure,scout_diagnostic=scout_meta,model_sha256=MODEL_SHA256,container_image=IMAGE,independent_review_completed=False,provider_account_cap_verified=False,canonical_supabase_claimed=False,eligible_for_win_ledger=False,network_boundary='isolated namespace, only loopback observed')
    result['note']='Synthetic fixture only; no source retrieval, external action, hosted authentication, provider cap or release claim.'
    data=(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode()
    fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as f: f.write(data)
    # Public log is metadata only; no generated text, task payload or credentials.
    print(json.dumps({'status':result['status'],'reason':result['reason'],'complete_candidate':complete,'attempted_calls':len(a.attempted),'valid_responses':len(a.receipts),'stage_token_receipts':a.receipts,'adapter_failure':a.last_failure,'scout_diagnostic':scout_meta,'receipt_sha256':hashlib.sha256(data).hexdigest(),'human_review_required':True}))
    return 0 if complete else 2
if __name__=='__main__':raise SystemExit(main())
