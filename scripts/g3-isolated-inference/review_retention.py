"""Offline encrypted evidence retention candidate. POSIX, trusted private parent.
No network, scheduler, key management, publication or independent approval.
Only the caller can establish that ciphertext came from the reviewed seal step.
"""
import hashlib
import json
import os
import re
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path

MAX_ENVELOPE=270_000
MAX_MANIFEST=4_096
MAX_TTL_HOURS=72
FILES={'review.cms','manifest.json'}

class RetentionHold(ValueError): pass

def require(ok, reason):
    if not ok: raise RetentionHold(reason)

def digest(b): return hashlib.sha256(b).hexdigest()
def pin(p): return isinstance(p,str) and re.fullmatch(r'[0-9a-f]{64}',p) is not None

def now_utc(t):
    require(isinstance(t,datetime) and t.utcoffset() is not None,'trusted_clock_required')
    return t.astimezone(timezone.utc)

def id_ok(v): return isinstance(v,str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{7,63}',v) is not None

def open_private(path, *, parent_fd=None):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent_fd)
    st=os.fstat(fd)
    if st.st_uid!=os.geteuid() or st.st_mode & 0o077:
        os.close(fd); raise RetentionHold('private_directory_required')
    return fd

def read_file(fd,name,limit):
    file_fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
    with os.fdopen(file_fd,'rb') as f:
        st=os.fstat(f.fileno())
        require(stat.S_ISREG(st.st_mode) and st.st_uid==os.geteuid() and st.st_nlink==1 and not st.st_mode & 0o077,'unsafe_file')
        data=f.read(limit+1)
        require(0<len(data)<=limit,'file_size')
        return data

def write_file(fd,name,data):
    file_fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd)
    with os.fdopen(file_fd,'wb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())

def unique(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'duplicate_manifest_key');result[k]=v
    return result

def inspect(fd,bundle_id,*,now,check_expiry=True):
    require(set(os.listdir(fd))==FILES,'incomplete_or_unexpected_bundle')
    try: m=json.loads(read_file(fd,'manifest.json',MAX_MANIFEST),object_pairs_hook=unique)
    except (ValueError,UnicodeError): raise RetentionHold('invalid_manifest') from None
    keys={'version','bundle_id','created_utc','expires_utc','packet_sha256','envelope_sha256','envelope_bytes','recipient_cert_sha256'}
    require(isinstance(m,dict) and set(m)==keys and type(m['version']) is int and m['version']==1 and m['bundle_id']==bundle_id,'manifest_scope')
    require(all(pin(m[k]) for k in ('packet_sha256','envelope_sha256','recipient_cert_sha256')),'invalid_pins')
    try: created=now_utc(datetime.fromisoformat(m['created_utc'])); expires=now_utc(datetime.fromisoformat(m['expires_utc']))
    except (TypeError,ValueError): raise RetentionHold('invalid_timestamp') from None
    require(created<expires<=created+timedelta(hours=MAX_TTL_HOURS) and now>=created,'invalid_retention_window')
    if check_expiry: require(now<expires,'expired')
    data=read_file(fd,'review.cms',MAX_ENVELOPE)
    require(type(m['envelope_bytes']) is int and len(data)==m['envelope_bytes'] and digest(data)==m['envelope_sha256'],'ciphertext_mismatch')
    return data,m,expires

def store(parent,bundle_id,sealed,*,envelope_sha256,packet_sha256,recipient_cert_sha256,now,ttl_hours,storage_authorized=False):
    require(storage_authorized is True,'storage_approval_missing')
    require(id_ok(bundle_id),'invalid_bundle_id')
    require(type(sealed) is bytes and 0<len(sealed)<=MAX_ENVELOPE,'invalid_envelope')
    require(all(pin(x) for x in (envelope_sha256,packet_sha256,recipient_cert_sha256)) and digest(sealed)==envelope_sha256,'invalid_pins')
    require(type(ttl_hours) is int and 1<=ttl_hours<=MAX_TTL_HOURS,'retention_limit')
    now=now_utc(now)
    # Require a CMS AuthEnvelopedData structure, not arbitrary plaintext named .cms.
    # This is a type marker only; recipient identity and AEAD authentication are checked by decryptor.
    require(sealed[:1]==b'\x30' and b'\x06\x0b\x2a\x86\x48\x86\xf7\x0d\x01\x09\x10\x01\x17' in sealed[:32],'cms_auth_envelope_required')
    m=dict(version=1,bundle_id=bundle_id,created_utc=now.isoformat(),expires_utc=(now+timedelta(hours=ttl_hours)).isoformat(),packet_sha256=packet_sha256,envelope_sha256=envelope_sha256,envelope_bytes=len(sealed),recipient_cert_sha256=recipient_cert_sha256)
    pfd=open_private(parent);fd=None;created=False
    try:
        os.mkdir(bundle_id,0o700,dir_fd=pfd);created=True
        fd=open_private(bundle_id,parent_fd=pfd)
        write_file(fd,'review.cms',sealed)
        write_file(fd,'manifest.json',json.dumps(m,separators=(',',':'),allow_nan=False).encode())
        os.fsync(fd);os.fsync(pfd)
        _,actual,_=inspect(fd,bundle_id,now=now)
        return actual
    except Exception:
        if created and fd is not None:
            for name in FILES:
                try: os.unlink(name,dir_fd=fd)
                except FileNotFoundError: pass
            os.rmdir(bundle_id,dir_fd=pfd)
        raise
    finally:
        if fd is not None: os.close(fd)
        os.close(pfd)

def retrieve(parent,bundle_id,*,now,expected_envelope_sha256,expected_packet_sha256,expected_recipient_cert_sha256):
    require(id_ok(bundle_id),'invalid_bundle_id'); now=now_utc(now)
    require(all(pin(p) for p in (expected_envelope_sha256,expected_packet_sha256,expected_recipient_cert_sha256)),'trusted_pins_required')
    pfd=open_private(parent)
    try:
        fd=open_private(bundle_id,parent_fd=pfd)
        try:
            data,m,_=inspect(fd,bundle_id,now=now)
            require((m['envelope_sha256'],m['packet_sha256'],m['recipient_cert_sha256'])==(expected_envelope_sha256,expected_packet_sha256,expected_recipient_cert_sha256),'trusted_pin_mismatch')
            return data,m
        finally: os.close(fd)
    finally: os.close(pfd)

def remove(parent,bundle_id,*,now,revocation_authorized=False,expected_manifest=None):
    """Delete only verified bundle entries after expiry or explicit revocation.
    No secure overwrite guarantee, backups or remote copy deletion.
    Corrupt bundles require authorized manual quarantine/removal.
    """
    require(id_ok(bundle_id),'invalid_bundle_id');now=now_utc(now)
    pfd=open_private(parent)
    try:
        fd=open_private(bundle_id,parent_fd=pfd)
        try:
            _,m,expires=inspect(fd,bundle_id,now=now,check_expiry=False)
            if expected_manifest is not None:
                require(m==expected_manifest,'trusted_manifest_mismatch')
            require(now>=expires or revocation_authorized is True,'not_expired_or_revoked')
            # Ciphertext first, even if the process dies before manifest removal.
            for name in ('review.cms','manifest.json'): os.unlink(name,dir_fd=fd)
            os.fsync(fd)
            os.rmdir(bundle_id,dir_fd=pfd);os.fsync(pfd)
            return {'bundle_id':bundle_id,'envelope_sha256':m['envelope_sha256'],'deleted':True,'reason':'expired' if now>=expires else 'revoked','independent_review_completed':False}
        finally: os.close(fd)
    finally: os.close(pfd)
