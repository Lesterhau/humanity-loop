"""Seal an actual receipt before producer cleanup. No upload or reviewer acceptance.
Caller supplies a separately approved certificate/pin and private empty output directory.
Never print or persist plaintext outside the producer's existing temporary directory.
"""
import json
import os
import stat
import sys
from pathlib import Path
from review_envelope import MAX_PACKET, MAX_CERT, check_cert, digest
from review_handoff import seal_review

def read_bounded(path,limit):
    with Path(path).open('rb') as f:
        data=f.read(limit+1)
    if not 0<len(data)<=limit:
        raise ValueError('input_size')
    return data

def destination(path):
    p=Path(path)
    if p.is_symlink() or not p.is_dir():
        raise ValueError('private_empty_destination_required')
    st=p.stat()
    if st.st_uid!=os.getuid() or stat.S_IMODE(st.st_mode)!=0o700 or any(p.iterdir()):
        raise ValueError('private_empty_destination_required')
    return p

def verify_config(cert_path,cert_pin,out):
    cert=read_bounded(cert_path,MAX_CERT)
    check_cert(cert,cert_pin)
    destination(out)
    return cert

def seal_file(receipt,cert_path,cert_pin,out):
    cert=verify_config(cert_path,cert_pin,out)
    p=destination(out)
    raw=read_bounded(receipt,MAX_PACKET)
    sealed,meta=seal_review(raw,cert,cert_pin,digest(raw))
    # Create exclusively; no overwrite. Publish metadata last as completion marker.
    envelope=p/'review.cms'
    manifest=p/'manifest.json'
    created=[]
    try:
        for target,data in ((envelope,sealed),(manifest,(json.dumps(meta,sort_keys=True)+'\n').encode())):
            fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            created.append(target)
            with os.fdopen(fd,'wb') as f:
                f.write(data);f.flush();os.fsync(f.fileno())
        fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
        try: os.fsync(fd)
        finally: os.close(fd)
    except BaseException:
        for target in reversed(created):
            target.unlink(missing_ok=True)
        raise
    return meta

def main():
    try:
        if len(sys.argv)==5 and sys.argv[1]=='preflight':
            verify_config(*sys.argv[2:])
            print('REVIEW_DESTINATION_PREFLIGHT_PASSED')
        elif len(sys.argv)==6 and sys.argv[1]=='seal':
            meta=seal_file(*sys.argv[2:])
            print(json.dumps(meta,sort_keys=True))
        else:
            raise ValueError('invalid_arguments')
    except Exception:
        # Do not echo local paths, certificate contents, raw outputs or exceptions.
        print('REVIEW_HANDOFF_HELD',file=sys.stderr)
        return 2
    return 0

if __name__=='__main__':
    raise SystemExit(main())
