"""Offline CAP consumer compatibility rehearsal; no live watchdog changes.

The anchor must be independently obtained from an approved receipt history.
A coherent untrusted anchor is not evidence of authenticity. No remote fetch,
fallback to main, credential access, or changes to repository refs.
"""
import json
import subprocess
import shutil
from pathlib import Path
from cap_receipt_pilot import LATEST,require,Hold

def verified_latest(repo,anchor,head):
    from cap_receipt_pilot import verified_history
    return verified_history(repo,anchor,head)[LATEST][1]

def assess(repo,anchor,head,now_ms):
    # Test-only fixed clock. Invoke the existing watchdog's real CAP check.
    require(type(now_ms) is int and 0<=now_ms<8640000000000000,'invalid_test_clock')
    try:
        raw=verified_latest(repo,anchor,head)
    except (Hold,ValueError,TypeError,KeyError,OSError,subprocess.SubprocessError):
        raw=b'null'
    script=Path(__file__).resolve().parent/'ops_sentinel.js'
    source="""const fs=require('node:fs');
const s=require(process.argv[1]);
const now=Number(process.argv[2]);
const result=s.receiptCheck(...s.CHECKS[0],now,()=>JSON.parse(fs.readFileSync(0,'utf8')));
process.stdout.write(JSON.stringify(result));"""
    # Resolve the trusted CI runner's installed Node executable before clearing
    # the child environment. Do not forward runner credentials or NODE_OPTIONS.
    node=shutil.which('node')
    require(node is not None and Path(node).is_absolute(),'node_runtime_unavailable')
    proc=subprocess.run([node,'-e',source,str(script),str(now_ms)],
        input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        timeout=10,check=True,env={'PATH':'/usr/bin:/bin','LANG':'C'})
    result=json.loads(proc.stdout)
    return {'check':result,'live_cutover':False,'independent_attestation':False}
