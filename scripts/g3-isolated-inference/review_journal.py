"""Durable, serialized local review lifecycle rehearsal (Linux/POSIX, SQLite).
No network, deployment, scheduler, real reviewer or release authority.
Assumes trusted local host, owner-only root and trusted ancestor paths/clock.
All operational callers must use this journal instead of direct file helpers.
"""
from contextlib import contextmanager
from datetime import timedelta
import fcntl
import json
import os
import sqlite3
import stat
from pathlib import Path

from review_cleanup import validate,MAX_BATCH
from review_handoff import seal_review,open_review
from review_retention import (open_private,inspect,store,retrieve,remove,require,
    id_ok,now_utc,MAX_TTL_HOURS,RetentionHold)

DB='review-ledger.sqlite3'
STATES=('storing','retained','deleting','deleted','hold')

@contextmanager
def journal(root):
    root=Path(root).absolute()
    fd=open_private(root)
    db=None
    try:
        # Lock the dedicated root directory itself; no lockfile replacement race.
        try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise RetentionHold('journal_busy') from None
        try:
            f=os.open(DB,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd)
        except FileExistsError:
            f=os.open(DB,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            st=os.fstat(f)
            require(stat.S_ISREG(st.st_mode) and st.st_uid==os.geteuid() and st.st_nlink==1 and not st.st_mode&0o077,'unsafe_journal')
        finally: os.close(f)
        # Private trusted local root; SQLite rollback journal, full synchronization.
        db=sqlite3.connect(str(root/DB),timeout=1)
        require(db.execute('PRAGMA journal_mode=DELETE').fetchone()[0]=='delete','journal_mode')
        db.execute('PRAGMA synchronous=FULL')
        db.execute('PRAGMA trusted_schema=OFF')
        with db:
            db.execute("""CREATE TABLE IF NOT EXISTS bundles(
                id TEXT PRIMARY KEY, manifest TEXT NOT NULL,
                state TEXT NOT NULL CHECK(state IN ('storing','retained','deleting','deleted','hold')))""")
            db.execute("""CREATE TABLE IF NOT EXISTS transitions(
                seq INTEGER PRIMARY KEY, id TEXT NOT NULL,
                state TEXT NOT NULL, at_utc TEXT NOT NULL, reason TEXT NOT NULL)""")
        os.fsync(fd)
        yield db,fd
    finally:
        if db is not None: db.close()
        os.close(fd)

def row(db,bid):
    require(id_ok(bid),'invalid_bundle_id')
    r=db.execute('SELECT manifest,state FROM bundles WHERE id=?',(bid,)).fetchone()
    require(r is not None,'unrecorded_bundle')
    m=json.loads(r[0])
    validate(m)
    require(m['bundle_id']==bid and r[1] in STATES,'invalid_journal_row')
    return m,r[1]

def transition(db,bid,old,new,now,reason):
    require(new in STATES,'invalid_state')
    with db:
        cur=db.execute('UPDATE bundles SET state=? WHERE id=? AND state=?',(new,bid,old))
        require(cur.rowcount==1,'unexpected_journal_state')
        db.execute('INSERT INTO transitions(id,state,at_utc,reason) VALUES(?,?,?,?)',(bid,new,now.isoformat(),reason))

def retain(root,bid,packet,certificate,cert_pin,receipt_pin,*,now,ttl_hours,storage_authorized=False):
    require(storage_authorized is True,'storage_approval_missing')
    require(id_ok(bid),'invalid_bundle_id')
    require(type(ttl_hours) is int and 1<=ttl_hours<=MAX_TTL_HOURS,'retention_limit')
    now=now_utc(now)
    with journal(root) as (db,fd):
        require(db.execute('SELECT 1 FROM bundles WHERE id=?',(bid,)).fetchone() is None,'bundle_id_already_recorded')
        try: os.stat(bid,dir_fd=fd,follow_symlinks=False)
        except FileNotFoundError: pass
        else: raise RetentionHold('unrecorded_existing_bundle')
        sealed,meta=seal_review(packet,certificate,cert_pin,receipt_pin)
        m=dict(version=1,bundle_id=bid,created_utc=now.isoformat(),
            expires_utc=(now+timedelta(hours=ttl_hours)).isoformat(),
            packet_sha256=receipt_pin,envelope_sha256=meta['envelope_sha256'],
            envelope_bytes=len(sealed),recipient_cert_sha256=cert_pin)
        validate(m)
        # Commit intent and immutable exact manifest BEFORE any artifact write.
        with db:
            db.execute('INSERT INTO bundles(id,manifest,state) VALUES(?,?,?)',
                (bid,json.dumps(m,separators=(',',':')),'storing'))
            db.execute('INSERT INTO transitions(id,state,at_utc,reason) VALUES(?,?,?,?)',
                (bid,'storing',now.isoformat(),'storage_intent'))
        actual=store(root,bid,sealed,envelope_sha256=m['envelope_sha256'],
            packet_sha256=receipt_pin,recipient_cert_sha256=cert_pin,
            now=now,ttl_hours=ttl_hours,storage_authorized=True)
        require(actual==m,'stored_manifest_mismatch')
        transition(db,bid,'storing','retained',now,'storage_verified')
        return m

def recover(root,bid,certificate,cert_pin,key,receipt_pin,envelope_pin,*,now):
    now=now_utc(now)
    with journal(root) as (db,fd):
        m,state=row(db,bid)
        require(state=='retained','not_retained')
        require((cert_pin,receipt_pin,envelope_pin)==(m['recipient_cert_sha256'],m['packet_sha256'],m['envelope_sha256']),'journal_pin_mismatch')
        sealed,actual=retrieve(root,bid,now=now,expected_envelope_sha256=envelope_pin,
            expected_packet_sha256=receipt_pin,expected_recipient_cert_sha256=cert_pin)
        require(actual==m,'journal_manifest_mismatch')
        return open_review(sealed,certificate,cert_pin,key,receipt_pin,envelope_pin)

def reconcile(root,bid,*,now):
    """Only interrupted intents may be reconciled. Never infers deletion from absence."""
    now=now_utc(now)
    with journal(root) as (db,fd):
        m,state=row(db,bid)
        created,_=validate(m)
        require(now>=created,'clock_before_creation')
        if state=='storing':
            try:
                child=open_private(bid,parent_fd=fd)
                try: _,actual,_=inspect(child,bid,now=now,check_expiry=False)
                finally: os.close(child)
                require(actual==m,'journal_manifest_mismatch')
            except (OSError,RetentionHold):
                transition(db,bid,state,'hold',now,'interrupted_storage_unconfirmed')
                return 'hold'
            transition(db,bid,state,'retained',now,'interrupted_storage_verified')
            return 'retained'
        if state=='deleting':
            transition(db,bid,state,'hold',now,'interrupted_deletion_unconfirmed')
            return 'hold'
        return state

def cleanup(root,ids,*,now,deletion_authorized=False):
    require(deletion_authorized is True,'cleanup_approval_missing')
    require(type(ids) is list and len(ids)<=MAX_BATCH and all(id_ok(x) for x in ids) and len(set(ids))==len(ids),'cleanup_batch_limit')
    now=now_utc(now)
    with journal(root) as (db,fd):
        prepared=[]
        for bid in ids:
            m,state=row(db,bid)
            created,expires=validate(m)
            require(now>=created,'clock_before_creation')
            prepared.append((bid,m,state,expires))
        results=[]
        for bid,m,state,expires in prepared:
            if state!='retained' or now<expires:
                results.append({'bundle_id':bid,'status':state if state!='retained' else 'not_expired'})
                continue
            transition(db,bid,'retained','deleting',now,'expiry_deletion_intent')
            try:
                receipt=remove(root,bid,now=now,expected_manifest=m)
                require(receipt.get('deleted') is True and receipt.get('envelope_sha256')==m['envelope_sha256'] and receipt.get('bundle_id')==bid,'invalid_deletion_receipt')
            except (OSError,RetentionHold):
                transition(db,bid,'deleting','hold',now,'deletion_unconfirmed')
                results.append({'bundle_id':bid,'status':'hold'})
                continue
            transition(db,bid,'deleting','deleted',now,'deletion_receipt_verified')
            results.append({'bundle_id':bid,'status':'deleted','receipt':receipt})
        return {'results':results,'independent_review_completed':False,'release_authorized':False}

def state(root,bid):
    with journal(root) as (db,fd):
        m,s=row(db,bid)
        return {'bundle_id':bid,'state':s,'manifest':m,
            'transitions':[dict(state=a,at_utc=b,reason=c) for a,b,c in db.execute(
                'SELECT state,at_utc,reason FROM transitions WHERE id=? ORDER BY seq',(bid,))]}
