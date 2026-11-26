"""Read the exact previously observed public main; no ref changes."""
import sys
from pathlib import Path
from cap_receipt_pilot import git
from receipt_state_store import seed,load,verified_state
PIN='d3068601c1e17fc0083832259bf3b7698fc0ff52'
def main(repo):
    assert git(repo,'rev-parse','HEAD').decode().strip()==PIN
    refs=git(repo,'for-each-ref','--format=%(objectname) %(refname)')
    for writer in ('critical','federal','evidence','sentinel'):
        original=load(repo,writer,PIN,seed=True)
        candidate=seed(repo,writer,PIN)
        assert verified_state(repo,writer,candidate,candidate)==original
        print('HISTORICAL_WRITER_SEED_PASSED',writer,'files='+str(len(original)))
    assert git(repo,'for-each-ref','--format=%(objectname) %(refname)')==refs
    assert git(repo,'status','--porcelain')==b''
if __name__=='__main__':main(Path(sys.argv[1]).resolve())
