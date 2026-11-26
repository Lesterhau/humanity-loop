"""Offline CAP receipt cutover candidate. Local Git only; never push or fetch.

A reviewed seed and separately protected receipt branch are prerequisites.
No source fetch, remote credentials, or production workflow changes.
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime,timezone
from pathlib import Path

PREFIX='runtime/cap-daily-audit/'
LATEST=PREFIX+'latest.json'
ARCHIVE=re.compile(re.escape(PREFIX)+r'runs/(?:\d{4}-\d{2}-\d{2}|\d{8}T\d{12}Z-[a-f0-9]{64})\.json\Z')
SHA=re.compile(r'[a-f0-9]{40}\Z')
MAX_FILE=4*1024*1024
MAX_FILES=10000
MAX_TOTAL=32*1024*1024
SOURCE='https://api.weather.gov/alerts/active'

class Hold(ValueError): pass

def require(ok,reason):
    if not ok: raise Hold(reason)

def git(repo,*args,data=None,index=None):
    # No inherited Git configuration or credential/remote environment.
    env={'PATH':'/usr/bin:/bin','LANG':'C','GIT_CONFIG_NOSYSTEM':'1',
         'GIT_CONFIG_GLOBAL':'/dev/null','GIT_TERMINAL_PROMPT':'0',
         'GIT_AUTHOR_NAME':'Synthetic CAP rehearsal','GIT_AUTHOR_EMAIL':'cap@example.invalid',
         'GIT_COMMITTER_NAME':'Synthetic CAP rehearsal','GIT_COMMITTER_EMAIL':'cap@example.invalid'}
    if index is not None: env['GIT_INDEX_FILE']=str(index)
    return subprocess.run(['git','-C',str(repo),*args],input=data,stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,timeout=20,check=True,env=env).stdout

def parse(raw):
    require(type(raw) is bytes and 0<len(raw)<=MAX_FILE,'receipt_size')
    def pairs(items):
        out={}
        for key,value in items:
            require(key not in out,'duplicate_key')
            out[key]=value
        return out
    def bad(_): raise Hold('nonfinite_json')
    obj=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)
    require(type(obj) is dict and set(obj)=={'schemaVersion','runAt','source','alertsChecked',
        'findingsCount','bySeverity','findings'},'receipt_shape')
    require(type(obj['schemaVersion']) is int and obj['schemaVersion']==1 and obj['source']==SOURCE,'receipt_source')
    stamp=obj['runAt']
    require(type(stamp) is str and stamp.endswith('Z'),'receipt_clock')
    dt=datetime.fromisoformat(stamp[:-1]+'+00:00')
    require(dt.utcoffset()==timezone.utc.utcoffset(dt),'receipt_clock')
    counts=obj['bySeverity']; findings=obj['findings']
    require(type(obj['alertsChecked']) is int and 0<=obj['alertsChecked']<=250 and
        type(obj['findingsCount']) is int and 0<=obj['findingsCount']<=400 and
        type(findings) is list and len(findings)==obj['findingsCount'] and
        type(counts) is dict and set(counts)=={'error','warning','advisory'} and
        all(type(v) is int and v>=0 for v in counts.values()),'receipt_counts')
    seen=dict.fromkeys(counts,0)
    for f in findings:
        require(type(f) is dict and set(f)=={'alertId','sender','event','sent','sourceUrl',
            'severity','title','detail','status','firstSeen'} and
            all(type(v) is str and len(v)<=4096 for v in f.values()) and
            f['severity'] in seen and f['status']=='open' and f['firstSeen']==stamp,'finding_shape')
        seen[f['severity']]+=1
    require(seen==counts,'severity_counts')
    return dt

def scoped(path):
    return path==LATEST or ARCHIVE.fullmatch(path) is not None

def load(repo,head,*,only):
    require(type(head) is str and SHA.fullmatch(head),'immutable_commit_required')
    require(git(repo,'cat-file','-t',head)==b'commit\n','commit_required')
    entries={};total=0
    for row in git(repo,'ls-tree','-r','-z',head).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1);path=path.decode('utf-8')
        if not scoped(path):
            require(not only,'unexpected_receipt_path')
            require(not path.startswith(PREFIX) or path.startswith(PREFIX+'reviews/'),'unexpected_seed_path')
            continue
        mode,kind,oid=meta.decode('ascii').split()
        require(mode=='100644' and kind=='blob','unsafe_receipt_mode')
        size=int(git(repo,'cat-file','-s',oid))
        total+=size
        require(len(entries)<MAX_FILES and size<=MAX_FILE and total<=MAX_TOTAL,'tree_limit')
        raw=git(repo,'cat-file','blob',oid)
        try:
            dt=parse(raw)
            if path!=LATEST:
                name=path.rsplit('/',1)[-1]
                if len(name)==15: # YYYY-MM-DD.json
                    require(name==dt.date().isoformat()+'.json','archive_date_mismatch')
                else:
                    expected=dt.strftime('%Y%m%dT%H%M%S%fZ')+'-'+hashlib.sha256(raw).hexdigest()+'.json'
                    require(name==expected,'archive_digest_or_time_mismatch')
        except (ValueError,TypeError,KeyError) as exc:
            raise Hold('invalid_receipt:'+path+':'+type(exc).__name__+':'+str(exc)[:90]) from None
        entries[path]=(oid,raw)
    require(LATEST in entries,'missing_latest')
    latest_raw=entries[LATEST][1]
    archives=[raw for path,(_,raw) in entries.items() if path!=LATEST]
    require(any(raw==latest_raw for raw in archives),'latest_not_archived')
    require(all(parse(raw)<=parse(latest_raw) for raw in archives),'archive_newer_than_latest')
    return entries

def commit(repo,entries,parent=None):
    with tempfile.TemporaryDirectory() as tmp:
        idx=Path(tmp)/'index'
        git(repo,'read-tree','--empty',index=idx)
        data=b''.join(f'100644 {oid}\t{path}\0'.encode() for path,(oid,raw) in sorted(entries.items()))
        git(repo,'update-index','-z','--index-info',data=data,index=idx)
        tid=git(repo,'write-tree',index=idx).decode().strip()
        args=['commit-tree',tid]
        if parent: args.extend(['-p',parent])
        return git(repo,*args,data=b'Synthetic CAP receipt candidate\n').decode().strip()

def trusted_now():
    # Offline rehearsal uses the local UTC host clock. A live writer must
    # establish independent clock/anchor custody; report timestamps are not authority.
    return datetime.now(timezone.utc)

def seed(repo,main):
    """Extract scoped receipts from exact reviewed code commit, no other files."""
    now=trusted_now()
    entries=load(repo,main,only=False)
    require(parse(entries[LATEST][1])<=now,'future_seed_receipt')
    return commit(repo,entries)

def propose(repo,prior,report):
    """Consume actual producer report bytes, not an arbitrary code-tree diff."""
    now=trusted_now()
    entries=load(repo,prior,only=True)
    dt=parse(report);previous=parse(entries[LATEST][1])
    require(previous<=now,'future_prior_receipt_hold')
    require(dt<=now,'future_receipt')
    require(dt>=previous,'receipt_time_regression')
    if dt==previous:
        require(report==entries[LATEST][1],'conflicting_same_timestamp')
        return prior
    digest=hashlib.sha256(report).hexdigest()
    path=PREFIX+'runs/'+dt.strftime('%Y%m%dT%H%M%S%fZ')+'-'+digest+'.json'
    require(path not in entries,'archive_collision')
    require(len(entries)<MAX_FILES and sum(len(raw) for _,raw in entries.values())-
        len(entries[LATEST][1])+2*len(report)<=MAX_TOTAL,'tree_limit')
    oid=git(repo,'hash-object','-w','--stdin',data=report).decode().strip()
    entries[path]=(oid,report);entries[LATEST]=(oid,report)
    return commit(repo,entries,prior)

def read_latest(repo,head):
    return load(repo,head,only=True)[LATEST][1]
