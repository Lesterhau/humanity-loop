"""Scoped receipt-state storage candidate. Local Git objects only.

CAP retains its existing stricter pilot. The four remaining writer groups
use this adapter. No remote push, deploy, secrets, source fetch or settings
changes. Caller must supply independently trusted seed/anchor and exact head.
A local CAS is not remote authorization or independent approval.
"""
import json
import re
import subprocess
from datetime import datetime,timezone
from cap_receipt_pilot import git,commit,require,Hold,SHA,MAX_FILE,MAX_FILES,MAX_TOTAL
from critical_guidance_delta import SOURCES as GUIDANCE
from federal_policy_delta import SOURCES as FEDERAL

G='runtime/critical-guidance-delta/'
F='runtime/federal-policy-delta/'
E='runtime/evidence-integrity-backup/'
O='runtime/ops-sentinel/'
R='runtime/reciprocal-audit/'
EVENT=re.compile(r'events/\d{8}T\d{6}(?:\.\d{1,6})?Z\.json\Z')
SOURCE_KEYS={'critical':{x['key'] for x in GUIDANCE},'federal':{x['key'] for x in FEDERAL}}
PREFIX={'critical':G,'federal':F,'evidence':E,'sentinel':O}
REQUIRED={k:{PREFIX[k]+'latest-run.json'}|{PREFIX[k]+'snapshots/'+s+'.json' for s in keys} for k,keys in SOURCE_KEYS.items()}
REQUIRED.update(evidence={E+n for n in ('latest.json','state.json','review-queue.json')},sentinel={O+'latest.json',R+'latest.json'})

def scoped(writer,path):
    require(writer in REQUIRED,'unknown_writer')
    return path in REQUIRED[writer] or (writer in SOURCE_KEYS and path.startswith(PREFIX[writer]) and EVENT.fullmatch(path[len(PREFIX[writer]):]) is not None)

def manual_path(writer,path):
    return (writer=='critical' and path.startswith(G+'reviews/')) or (writer=='sentinel' and path.startswith(R+'resolutions/'))

def in_scope(writer,path):
    return path.startswith(PREFIX[writer]) or (writer=='sentinel' and path.startswith(R))

def parse(raw):
    require(type(raw) is bytes and 0<len(raw)<=MAX_FILE,'receipt_size')
    def pairs(items):
        obj={}
        for k,v in items:
            require(k not in obj,'duplicate_key')
            obj[k]=v
        return obj
    def bad(_):raise Hold('nonfinite_json')
    obj=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)
    require(type(obj) is dict and type(obj.get('schemaVersion',1)) is int and obj.get('schemaVersion',1)==1,'receipt_shape')
    return obj

def stamp(value):
    require(isinstance(value,str) and value.endswith('Z'),'utc_timestamp_required')
    return datetime.fromisoformat(value[:-1]+'+00:00')

def latest_path(writer):
    return PREFIX[writer]+('latest-run.json' if writer in SOURCE_KEYS else 'latest.json')

def check_counts(obj,pairs):
    for count,items in pairs:
        require(type(obj.get(count)) is int and isinstance(obj.get(items),list) and obj[count]==len(obj[items]),'receipt_totals')

def validate(writer,state,now):
    require(writer in REQUIRED,'unknown_writer')
    require(type(state) is dict and REQUIRED[writer]<=set(state),'missing_writer_state')
    require(len(state)<=MAX_FILES and all(scoped(writer,p) for p in state),'unexpected_receipt_path')
    require(sum(len(v) for v in state.values())<=MAX_TOTAL,'tree_limit')
    parsed={p:parse(v) for p,v in state.items()}
    latest=parsed[latest_path(writer)]
    t=stamp(latest.get('runAt'));require(t<=now,'future_receipt')
    if writer in SOURCE_KEYS:
        check_counts(latest,(('changesDetected','changes'),('failuresCount','failures')))
        require(latest.get('sourcesConfigured')==len(SOURCE_KEYS[writer]),'source_inventory')
        for p,obj in parsed.items():
            if '/snapshots/' in p:
                key=p.rsplit('/',1)[-1][:-5]
                require(obj.get('key')==key,'snapshot_key')
                field='fingerprint' if writer=='critical' else 'hash'
                date='lastChecked' if writer=='critical' else 'capturedAt'
                require(isinstance(obj.get(field),str) and re.fullmatch('[0-9a-f]{64}',obj[field]),'snapshot_digest')
                require(stamp(obj.get(date))<=t,'snapshot_after_run')
                if writer=='critical':
                    import hashlib
                    require(isinstance(obj.get('normalizedText'),str) and hashlib.sha256(obj['normalizedText'].encode()).hexdigest()==obj[field],'snapshot_digest')
                else:
                    # Federal hash covers full text; a truncated excerpt is not the hash input.
                    require(isinstance(obj.get('excerpt'),str) and len(obj['excerpt'])<=8000,'snapshot_excerpt')
            elif '/events/' in p:
                when=stamp(obj.get('runAt'))
                require(when<=t and p.rsplit('/',1)[-1]==obj['runAt'].replace(':','').replace('-','')+'.json','event_time')
        if latest['changesDetected'] or latest['failuresCount']:
            event=PREFIX[writer]+'events/'+latest['runAt'].replace(':','').replace('-','')+'.json'
            require(state.get(event)==state[latest_path(writer)],'latest_event_missing')
    elif writer=='evidence':
        check_counts(latest,(('candidateFindingsCount','candidateFindings'),('failuresCount','failures'),('coverageGapsCount','coverageGaps')))
        s=parsed[E+'state.json'];q=parsed[E+'review-queue.json']
        require(stamp(s.get('updatedAt'))==t,'state_clock_mismatch')
        require(isinstance(s.get('seenDois'),list) and isinstance(s.get('findingKeys'),list) and isinstance(q.get('items'),list),'evidence_state_shape')
        require(latest.get('clinicalConclusions') is None and latest.get('nativeAppDeployStateSynced') is False,'evidence_scope')
        queue_keys(q)
    else:
        require(latest.get('status') in ('healthy','warning','critical') and isinstance(latest.get('checks'),list),'sentinel_shape')
        reciprocal=parsed[R+'latest.json']
        require(stamp(reciprocal.get('runAt'))<=now and reciprocal.get('status') in ('checks-passed','action-proposed') and isinstance(reciprocal.get('findings'),list),'reciprocal_shape')
    return parsed

def queue_keys(q):
    out={}
    for item in q['items']:
        require(type(item) is dict,'review_queue_item')
        key=tuple(item.get(k) for k in ('retractedDoi','citingSource','citingId'))
        require(all(isinstance(k,str) and k for k in key) and key not in out,'review_queue_key')
        out[key]=item
    return out

def transition(writer,old,new,now):
    a=validate(writer,old,now);b=validate(writer,new,now)
    require(set(old)<=set(new),'receipt_history_removed')
    for path in old:
        if '/events/' in path:require(old[path]==new[path],'historical_event_changed')
    for path in (latest_path(writer),R+'latest.json') if writer=='sentinel' else (latest_path(writer),):
        ta=stamp(a[path]['runAt']);tb=stamp(b[path]['runAt'])
        require(tb>=ta,'receipt_time_regression')
        require(tb!=ta or old[path]==new[path],'conflicting_same_timestamp')
    if writer in SOURCE_KEYS:
        date='lastChecked' if writer=='critical' else 'capturedAt'
        for path in REQUIRED[writer]-{latest_path(writer)}:
            ta=stamp(a[path][date]);tb=stamp(b[path][date])
            require(tb>=ta and (tb!=ta or old[path]==new[path]),'snapshot_regression_or_conflict')
    if writer=='evidence':
        old_q=queue_keys(a[E+'review-queue.json']);new_q=queue_keys(b[E+'review-queue.json'])
        # Fail closed at the existing queue's truncation limit. Human decisions
        # are not mutable by this machine writer. Separate reviewed retention
        # and queue update procedures are required, not silent loss.
        require(all(new_q.get(k)==v for k,v in old_q.items()),'review_queue_changed_or_removed')
        require(all(v.get('status')=='unreviewed' for k,v in new_q.items() if k not in old_q),'new_queue_item_not_unreviewed')
    if writer!='sentinel' and new!=old:
        require(stamp(b[latest_path(writer)]['runAt'])>stamp(a[latest_path(writer)]['runAt']),'state_change_without_new_run')

def load(repo,writer,head,*,seed=False):
    require(writer in REQUIRED,'unknown_writer')
    require(isinstance(head,str) and SHA.fullmatch(head),'immutable_commit_required')
    require(git(repo,'cat-file','-t',head)==b'commit\n','commit_required')
    result={};total=0
    for row in git(repo,'ls-tree','-r','-z',head).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);path=path.decode()
        if not scoped(writer,path):
            require(seed and (not in_scope(writer,path) or manual_path(writer,path)),'unexpected_receipt_path')
            continue
        mode,kind,oid=meta.decode().split()
        require(mode=='100644' and kind=='blob','unsafe_receipt_mode')
        size=int(git(repo,'cat-file','-s',oid));total+=size
        require(size<=MAX_FILE and len(result)<MAX_FILES and total<=MAX_TOTAL,'tree_limit')
        result[path]=git(repo,'cat-file','blob',oid)
    return result

def write(repo,state,parent=None):
    return commit(repo,{k:(git(repo,'hash-object','-w','--stdin',data=v).decode().strip(),v) for k,v in state.items()},parent)

def seed(repo,writer,main):
    state=load(repo,writer,main,seed=True)
    validate(writer,state,datetime.now(timezone.utc))
    return write(repo,state)

def propose(repo,writer,prior,state):
    old=load(repo,writer,prior)
    transition(writer,old,state,datetime.now(timezone.utc))
    return prior if state==old else write(repo,state,prior)

def verified_state(repo,writer,anchor,head):
    # Validate every first-parent transition from the separately trusted
    # anchor; no fallback or merge-history ambiguity.
    base=load(repo,writer,anchor)
    now=datetime.now(timezone.utc);validate(writer,base,now)
    require(isinstance(head,str) and SHA.fullmatch(head),'immutable_commit_required')
    try:
        git(repo,'merge-base','--is-ancestor',anchor,head)
    except subprocess.CalledProcessError:
        raise Hold('untrusted_ancestry') from None
    chain=git(repo,'rev-list','--reverse','--first-parent','--max-count=1001',anchor+'..'+head).decode().splitlines()
    require(len(chain)<=1000,'anchor_rotation_required')
    previous=anchor
    for current in chain:
        parents=git(repo,'show','-s','--format=%P',current).decode().split()
        require(parents==[previous],'nonlinear_receipt_history')
        state=load(repo,writer,current)
        transition(writer,base,state,now)
        previous=current;base=state
    require(previous==head,'untrusted_ancestry')
    return base

def advance_local(repo,writer,ref,prior,state):
    # Intentionally only a test namespace. Never touch main or a remote ref.
    require(ref=='refs/heads/receipt-test-'+writer,'local_test_ref_required')
    head=propose(repo,writer,prior,state)
    git(repo,'update-ref',ref,head,prior)
    return head
