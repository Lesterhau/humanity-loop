"""Read pinned public historical receipts; construct local unreferenced test commits.
No push, network source fetch, source re-publication or changes to checked-out files.
"""
import sys
from pathlib import Path
from datetime import timedelta
from cap_daily_audit import build_report
from cap_receipt_pilot import git,seed,propose,load,parse,LATEST,PREFIX,read_latest
import json

BASE='e15ad3f8257187648a73decc235342be8e509ef2'

def main(repo):
    assert git(repo,'rev-parse','HEAD').decode().strip()==BASE
    assert git(repo,'status','--porcelain')==b''
    refs=git(repo,'show-ref')
    original=load(repo,BASE,only=False)
    assert len(original)==56 # 55 historical machine archives and latest; review remains on main.
    start=seed(repo,BASE)
    assert load(repo,start,only=True)==original
    timestamp=(parse(original[LATEST][1])+timedelta(seconds=1)).isoformat().replace('+00:00','Z')
    raw=(json.dumps(build_report([],timestamp),indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
    updated=propose(repo,start,raw)
    final=load(repo,updated,only=True)
    assert len(final)==57
    assert all(final[k]==v for k,v in original.items() if k!=LATEST)
    assert read_latest(repo,updated)==raw
    assert git(repo,'show-ref')==refs
    assert git(repo,'status','--porcelain')==b''
    assert git(repo,'rev-parse','HEAD').decode().strip()==BASE
    print('CAP_HISTORICAL_SEED_REHEARSAL_PASSED archives=55 latest=1 preserved_archives=55 new_archive=1')

if __name__=='__main__':
    main(Path(sys.argv[1]).resolve())
