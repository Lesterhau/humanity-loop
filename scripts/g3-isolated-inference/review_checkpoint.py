"""Bounded private journal checkpoint verification, offline candidate.

A checkpoint must be kept by an independently trusted party outside the
executor's control. A self-generated or locally stored checkpoint is NOT
independent evidence. Hash integrity does not prove physical erasure.
No signing identity, external anchor store, transmission or authorization.
"""
import hashlib
import hmac
import json
from datetime import datetime
from review_cleanup import validate
from review_retention import require,now_utc,pin
from review_journal import journal

MAX_EVENTS=10000
MAX_BUNDLES=2000
DOMAIN=b'HL-review-journal-checkpoint-v1\0'
GENESIS=hashlib.sha256(DOMAIN+b'genesis').hexdigest()
NEXT={
    None:{'storing'},
    'storing':{'retained','hold'},
    'retained':{'deleting','revoking'},
    'deleting':{'deleted','hold'},
    'revoking':{'revoked','hold'},
    'hold':{'purging'},
    'purging':{'purged_unverified','hold'},
    'deleted':set(),'revoked':set(),'purged_unverified':set(),
}
REASONS={
    'storing':{'storage_intent'},
    'retained':{'storage_verified','interrupted_storage_verified'},
    'deleting':{'expiry_deletion_intent'},
    'deleted':{'deletion_receipt_verified'},
    'revoking':{'revocation_intent'},
    'revoked':{'revocation_local_removal_verified'},
    'hold':{'interrupted_storage_unconfirmed','interrupted_deletion_unconfirmed',
            'deletion_unconfirmed','expired_held_purge_unconfirmed','revocation_removal_unconfirmed'},
    'purging':{'expired_held_ciphertext_purge_intent'},
    'purged_unverified':{'named_ciphertext_entry_removed'},
}

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,
                      allow_nan=False).encode('ascii')

def hash_link(prev,entry):
    return hashlib.sha256(DOMAIN+bytes.fromhex(prev)+canonical(entry)).hexdigest()

def snapshot(db,expected=None):
    if expected is not None:
        require(type(expected) is dict and set(expected)=={'version','sequence','head'}
            and type(expected['version']) is int and expected['version']==1
            and type(expected['sequence']) is int and 1<=expected['sequence']<=MAX_EVENTS
            and pin(expected['head']),'invalid_external_checkpoint')
    rows=db.execute('SELECT id,manifest,state FROM bundles ORDER BY id LIMIT ?',(MAX_BUNDLES+1,)).fetchall()
    require(len(rows)<=MAX_BUNDLES,'checkpoint_bundle_limit')
    manifests={};states={}
    for bid,raw,state in rows:
        require(type(raw) is str and len(raw)<=4096,'checkpoint_manifest_limit')
        m=json.loads(raw)
        validate(m)
        require(m['bundle_id']==bid,'checkpoint_bundle_mismatch')
        manifests[bid]=m;states[bid]=state
    events=db.execute('SELECT seq,id,state,at_utc,reason FROM transitions ORDER BY seq LIMIT ?',(MAX_EVENTS+1,)).fetchall()
    require(len(events)<=MAX_EVENTS,'checkpoint_event_limit')
    replay={};prev=GENESIS;last_time=None;anchored=False
    for count,(seq,bid,state,at,reason) in enumerate(events,1):
        require(seq==count and bid in manifests,'checkpoint_sequence_or_bundle')
        require(state in NEXT.get(replay.get(bid),set()) and reason in REASONS[state],
                'checkpoint_transition_invalid')
        t=now_utc(datetime.fromisoformat(at))
        created,expires=validate(manifests[bid])
        require(t>=created and (last_time is None or t>=last_time),'checkpoint_clock_order')
        require(state!='storing' or t==created,'checkpoint_creation_mismatch')
        require(state not in ('deleting','deleted','purging','purged_unverified') or t>=expires,
                'checkpoint_early_expiry_operation')
        entry={'sequence':seq,'bundle_id':bid,'state':state,'at_utc':at,'reason':reason,
               'manifest_sha256':hashlib.sha256(canonical(manifests[bid])).hexdigest()}
        prev=hash_link(prev,entry);replay[bid]=state;last_time=t
        if expected is not None and seq==expected['sequence']:
            require(hmac.compare_digest(prev,expected['head']),'external_checkpoint_mismatch')
            anchored=True
    require(replay==states,'checkpoint_materialized_state_mismatch')
    if expected is not None:
        require(anchored,'external_checkpoint_truncated')
    # A valid prefix does not authenticate newly appended events.
    return {'checkpoint':{'version':1,'sequence':len(events),'head':prev},
            'matches_supplied_checkpoint':anchored,
            'unanchored_events':len(events)-(expected['sequence'] if anchored else 0),
            'independent_review_completed':False,'deletion_independently_verified':False,
            'release_authorized':False}

def checkpoint(root,*,expected=None):
    """Read journal under its existing lock. No actual external anchor action."""
    with journal(root) as (db,fd):
        return snapshot(db,expected)
