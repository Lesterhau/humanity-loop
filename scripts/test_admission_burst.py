#!/usr/bin/env python3
"""10,000 synthetic registrations, 20 actual concurrent local psql sessions.
No external network, real participant identities, or production credentials."""
import os, subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
assert os.environ.get('PGHOST')=='127.0.0.1'
assert os.environ.get('PGDATABASE')=='admission_ci'
def query(sql):
    return subprocess.run(['psql','-X','-A','-t','-q','-v','ON_ERROR_STOP=1'],
        input=sql,text=True,capture_output=True,check=True,timeout=90).stdout.splitlines()
def worker(i):
    return query('\n'.join(f"SELECT public.synthetic_try_admission('synthetic-{i}-{j}');" for j in range(500)))
with ThreadPoolExecutor(max_workers=20) as pool:
    totals=Counter(x for result in pool.map(worker,range(20)) for x in result)
assert totals=={'admitted':4,'deferred':9996},totals
assert query("SELECT admitted_total||':'||approved_total||':'||(SELECT count(*) FROM hl_control.contributor_nodes) FROM hl_control.admission_budget_candidate;")==['5:5:5']
assert query("SELECT public.synthetic_try_admission('existing-fixture');")==['duplicate']
query("UPDATE hl_control.contributor_nodes SET status='revoked' WHERE token_hash='existing-fixture';")
assert query("SELECT public.synthetic_try_admission('after-revoke');")==['deferred']
assert query("SELECT count(*) FROM hl_control.contributor_nodes WHERE status='revoked';")==['1']
print('MOTHER_ADMISSION_SYNTHETIC_BURST_PASSED requests=10000 admitted=4 deferred=9996 existing=1 cap=5')
print('No production connections, credentials, real identities or external actions.')
