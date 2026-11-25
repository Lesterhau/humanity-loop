"""Bounded expiration sweep over independently recorded manifests, never a directory scan.
Trusted caller supplies authoritative manifests and clock. No scheduler or deployed storage.
"""
import json
from datetime import datetime
from review_retention import remove,require,pin,id_ok,now_utc,MAX_TTL_HOURS,RetentionHold
from datetime import timedelta
MAX_BATCH=25
KEYS={'version','bundle_id','created_utc','expires_utc','packet_sha256','envelope_sha256','envelope_bytes','recipient_cert_sha256'}

def validate(manifest):
    require(type(manifest) is dict and set(manifest)==KEYS,'invalid_trusted_manifest')
    require(type(manifest['version']) is int and manifest['version']==1 and id_ok(manifest['bundle_id']),'invalid_trusted_manifest')
    require(all(pin(manifest[k]) for k in ('packet_sha256','envelope_sha256','recipient_cert_sha256')),'invalid_trusted_manifest')
    require(type(manifest['envelope_bytes']) is int and 0<manifest['envelope_bytes']<=270000,'invalid_trusted_manifest')
    try:
        created=now_utc(datetime.fromisoformat(manifest['created_utc']))
        expires=now_utc(datetime.fromisoformat(manifest['expires_utc']))
    except (ValueError,TypeError):
        raise RetentionHold('invalid_trusted_manifest') from None
    require(created<expires<=created+timedelta(hours=MAX_TTL_HOURS),'invalid_trusted_manifest')
    return created,expires

def sweep(parent, manifests, *, now, deletion_authorized=False):
    require(deletion_authorized is True,'cleanup_approval_missing')
    require(type(manifests) is list and len(manifests)<=MAX_BATCH,'cleanup_batch_limit')
    now=now_utc(now)
    # Validate whole batch before any filesystem mutation.
    prepared=[]
    seen=set()
    for m in manifests:
        created,expires=validate(m)
        require(now>=created and m['bundle_id'] not in seen,'future_or_duplicate_manifest')
        seen.add(m['bundle_id']);prepared.append((dict(m),expires))
    results=[]
    for m,expires in prepared:
        bid=m['bundle_id']
        if now<expires:
            results.append({'bundle_id':bid,'status':'not_expired'})
            continue
        try:
            receipt=remove(parent,bid,now=now,expected_manifest=m)
            results.append({'bundle_id':bid,'status':'deleted','receipt':receipt})
        except FileNotFoundError:
            # Missing or incomplete is not a deletion receipt.
            results.append({'bundle_id':bid,'status':'missing_or_incomplete_unconfirmed'})
        except (RetentionHold,OSError):
            results.append({'bundle_id':bid,'status':'hold_manual_review'})
    return {'results':results,'deleted':sum(r['status']=='deleted' for r in results),
            'held':sum(r['status'] in ('missing_or_incomplete_unconfirmed','hold_manual_review') for r in results),
            'independent_review_completed':False,'release_authorized':False}
