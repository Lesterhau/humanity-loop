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
    return (writer=='critical' and path.startswith(G+'reviews/')) or (writer=='evidence' and path.startswith(E+'reviews/')) or (writer=='sentinel' and path.startswith(R+'resolutions/'))

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

def validate(writer,state,now,*,_cache=None):
    require(writer in REQUIRED,'unknown_writer')
    require(type(state) is dict and REQUIRED[writer]<=set(state),'missing_writer_state')
    require(len(state)<=MAX_FILES and all(scoped(writer,p) for p in state),'unexpected_receipt_path')
    require(sum(len(v) for v in state.values())<=MAX_TOTAL,'tree_limit')
    parsed={};next_cache={}
    for p,v in state.items():
        prior=_cache.get(p) if _cache is not None else None
        obj=prior[1] if prior is not None and prior[0]==v else parse(v)
        parsed[p]=obj;next_cache[p]=(v,obj)
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
    if _cache is not None:
        _cache.clear();_cache.update(next_cache)
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
    return _transition_validated(writer,old,new,a,b)

def _transition_validated(writer,old,new,a,b):
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

def load(repo,writer,head,*,seed=False,_cache=None):
    require(writer in REQUIRED,'unknown_writer')
    require(isinstance(head,str) and SHA.fullmatch(head),'immutable_commit_required')
    require(git(repo,'cat-file','-t',head)==b'commit\n','commit_required')
    result={};total=0;next_cache={}
    for row in git(repo,'ls-tree','-r','-l','-z',head).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);path=path.decode()
        if not scoped(writer,path):
            require(seed and (not in_scope(writer,path) or manual_path(writer,path)),'unexpected_receipt_path')
            continue
        mode,kind,oid,size_text=meta.decode().split()
        require(mode=='100644' and kind=='blob','unsafe_receipt_mode')
        size=int(size_text);total+=size
        require(0<size<=MAX_FILE and len(result)<MAX_FILES and total<=MAX_TOTAL,'tree_limit')
        raw=next_cache.get(oid)
        if raw is None and _cache is not None:raw=_cache.get(oid)
        if raw is None:raw=git(repo,'cat-file','blob',oid)
        require(len(raw)==size,'blob_size_mismatch')
        result[path]=raw;next_cache[oid]=raw
    if _cache is not None:
        _cache.clear();_cache.update(next_cache)
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
    blob_cache={};parsed_cache={}
    base=load(repo,writer,anchor,_cache=blob_cache)
    now=datetime.now(timezone.utc);parsed=validate(writer,base,now,_cache=parsed_cache)
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
        state=load(repo,writer,current,_cache=blob_cache)
        new_parsed=validate(writer,state,now,_cache=parsed_cache)
        _transition_validated(writer,base,state,parsed,new_parsed)
        previous=current;base=state;parsed=new_parsed
    require(previous==head,'untrusted_ancestry')
    return base

def advance_local(repo,writer,ref,prior,state):
    # Intentionally only a test namespace. Never touch main or a remote ref.
    require(ref=='refs/heads/receipt-test-'+writer,'local_test_ref_required')
    head=propose(repo,writer,prior,state)
    git(repo,'update-ref',ref,head,prior)
    return head


# Workflow-facing interface. Only local immutable Git objects are accepted.
# This layer deliberately cannot fetch, push, change a ref, or choose an anchor.
# The approved deployment workflow must supply these independently.
def verified_lane(repo,writer,anchor,head):
    if writer!='cap':
        return verified_state(repo,writer,anchor,head)
    import cap_receipt_pilot as cap
    return {p:raw for p,(_,raw) in cap.verified_history(repo,anchor,head).items()}

def hydrate_lane(repo,writer,anchor,head,workspace):
    """Restore independently pinned state into a NEW producer workspace."""
    from pathlib import Path
    workspace=Path(workspace)
    state=verified_lane(repo,writer,anchor,head)
    require(not workspace.exists() and not workspace.is_symlink(),'workspace_must_be_new')
    workspace.mkdir(mode=0o700,parents=False)
    for name,raw in state.items():
        dest=workspace/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(raw)
    return state

def _workspace_file(root,name):
    from pathlib import Path
    root=Path(root)
    require(root.is_dir() and not root.is_symlink(),'workspace_required')
    p=root
    for component in Path(name).parts:
        p=p/component
        require(not p.is_symlink(),'unsafe_workspace_path')
    require(p.is_file() and p.stat().st_size<=MAX_FILE,'workspace_file_required')
    return p.read_bytes()

def prepare_lane(repo,writer,anchor,head,workspace):
    """Validate producer output and make an unreferenced local candidate.
    No destination ref is accepted; caller must separately authorize promotion.
    """
    from pathlib import Path
    import cap_receipt_pilot as cap
    root=Path(workspace)
    prior=verified_lane(repo,writer,anchor,head)
    if writer=='cap':
        return cap.propose(repo,head,_workspace_file(root,cap.LATEST))
    require(writer in REQUIRED,'unknown_writer')
    names=set()
    for prefix in ([PREFIX[writer],R] if writer=='sentinel' else [PREFIX[writer]]):
        directory=root/prefix
        require(directory.is_dir() and not directory.is_symlink(),'workspace_required')
        for p in directory.rglob('*'):
            require(not p.is_symlink(),'unsafe_workspace_path')
            if p.is_dir():continue
            name=p.relative_to(root).as_posix()
            require(scoped(writer,name),'unexpected_receipt_path')
            names.add(name)
            require(len(names)<=MAX_FILES,'tree_limit')
    require(set(prior)<=names,'receipt_history_removed')
    state={}
    size=0
    for name in sorted(names):
        raw=_workspace_file(root,name);size+=len(raw)
        require(size<=MAX_TOTAL,'tree_limit')
        state[name]=raw
    return propose(repo,writer,head,state)

def main():
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser(description='Local receipt cutover interface; never fetches, pushes or changes refs')
    parser.add_argument('operation',choices=('hydrate','candidate','verify'))
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--writer',required=True,choices=('cap','critical','federal','evidence','sentinel'))
    parser.add_argument('--anchor',required=True)
    parser.add_argument('--head',required=True)
    parser.add_argument('--workspace',type=Path)
    args=parser.parse_args()
    if args.operation=='verify':
        state=verified_lane(args.repo,args.writer,args.anchor,args.head)
        print(json.dumps({'writer':args.writer,'head':args.head,'files':len(state)}))
    else:
        if args.workspace is None:parser.error('--workspace is required')
        if args.operation=='hydrate':
            state=hydrate_lane(args.repo,args.writer,args.anchor,args.head,args.workspace)
            print(json.dumps({'writer':args.writer,'head':args.head,'files':len(state)}))
        else:
            print(prepare_lane(args.repo,args.writer,args.anchor,args.head,args.workspace))

if __name__=='__main__':main()
