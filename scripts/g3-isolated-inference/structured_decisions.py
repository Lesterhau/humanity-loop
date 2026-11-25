"""Structured decision transport, not a substitute for substantive review."""
import hashlib
import json
import re

POSITIVE={'verify':'PROCEED','safety':'GO'}
NEGATIVE={'verify':'REJECT','safety':'HOLD'}
CODES=('review_ready','non_actionable','unsupported_claim','unsafe_scope','missing_human_review','insufficient_context','other_concern')
FIELDS=('decision','reason_code','rationale')

class DecisionHold(ValueError):
    pass

def response_format(stage):
    if stage not in POSITIVE:
        raise DecisionHold('invalid_stage')
    return {'type':'json_object','schema':{
        'type':'object','properties':{
            'decision':{'type':'string','enum':[POSITIVE[stage],NEGATIVE[stage]]},
            'reason_code':{'type':'string','enum':list(CODES)},
            'rationale':{'type':'string','minLength':10,'maxLength':180}
        },'required':list(FIELDS),'additionalProperties':False}}

def decision_prompt(stage,prompt):
    response_format(stage)
    if not isinstance(prompt,str) or not prompt.strip():
        raise DecisionHold('invalid_prompt')
    return prompt+(
        '\nFORMAT ONLY: Instead of the requested first line, return one JSON object with '
        'decision, reason_code, rationale. All original substantive decision criteria still apply. '
        f'Choose {POSITIVE[stage]} only if every original condition passes; choose {NEGATIVE[stage]} '
        'when any condition fails, is uncertain, or evidence is insufficient. '
        'Use review_ready only for a positive decision; otherwise use one of '
        +', '.join(CODES[1:])+'. Write a specific 10-180 character rationale on one line. '
        'Do not claim live verification or approve external action. The decision is only '
        'about a draft for separate human review. Never approve solely to complete the workflow.'
    )

def _unique(pairs):
    result={}
    for k,v in pairs:
        if k in result: raise DecisionHold('duplicate_key')
        result[k]=v
    return result

def parse_decision(stage,raw):
    response_format(stage)
    if not isinstance(raw,str) or not 0<len(raw)<=8000:
        raise DecisionHold('invalid_text')
    try:
        obj=json.loads(raw,object_pairs_hook=_unique)
    except json.JSONDecodeError:
        raise DecisionHold('invalid_json') from None
    if not isinstance(obj,dict) or set(obj)!=set(FIELDS):
        raise DecisionHold('wrong_fields')
    v,c,r=(obj[k] for k in FIELDS)
    if not isinstance(v,str) or v not in (POSITIVE[stage],NEGATIVE[stage]):
        raise DecisionHold('invalid_decision')
    if not isinstance(c,str) or c not in CODES or ((v==POSITIVE[stage])!=(c=='review_ready')):
        raise DecisionHold('decision_reason_mismatch')
    if not isinstance(r,str) or not 10<=len(r)<=180 or r!=r.strip() or not r.isprintable() or not re.search(r'[A-Za-z]{3}',r):
        raise DecisionHold('invalid_rationale')
    if re.search(r'[\[\]{}]|\b(?:placeholder|lorem ipsum|insert here)\b',r,re.I):
        raise DecisionHold('placeholder')
    # This catches common explicit contradictory approvals, not all semantic errors.
    # Human review remains mandatory even for a syntactically valid positive decision.
    if v==POSITIVE[stage] and re.search(r'(?i)\b(?:cannot proceed|must hold|should reject|unsafe to proceed|not actionable|not safe)\b',r):
        raise DecisionHold('contradictory_positive')
    rendered=('VERDICT = '+v if stage=='verify' else v)+'\n'+r
    meta={'format_pass':True,'decision':v,'reason_code':c,'rationale_chars':len(r),
          'raw_sha256':hashlib.sha256(raw.encode('utf-8')).hexdigest()}
    return rendered,meta
