#!/usr/bin/env python3
"""Disposable PostgreSQL interest-cap rehearsal; no real user data or HTTP traffic."""
import os,subprocess,hashlib
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
assert os.environ.get('PGHOST')=='127.0.0.1'
assert os.environ.get('PGDATABASE')=='admission_ci'
def q(sql):
    return subprocess.run(['psql','-X','-A','-t','-q','-v','ON_ERROR_STOP=1'],
        input=sql,text=True,capture_output=True,check=True,timeout=120).stdout.splitlines()
def h(i): return hashlib.sha256(f'disposable-interest-fixture-{i}'.encode()).hexdigest()
def call(i,consent='true',version='interest-v1'):
    return f"SELECT hl_interest_candidate.record_interest('{h(i)}',{consent},'{version}');"
assert q(call(-1))==['closed']
assert q(call(-1,'false'))==['invalid']
assert q(call(-1,'true','wrong'))==['invalid']
assert q("SELECT has_schema_privilege('anon','hl_interest_candidate','USAGE') OR has_function_privilege('service_role','hl_interest_candidate.record_interest(text,boolean,text)','EXECUTE');")==['f']
q("UPDATE hl_interest_candidate.budget SET capacity=10000;")
def worker(i): return q('\n'.join(call(i*500+j) for j in range(500)))
with ThreadPoolExecutor(max_workers=20) as pool:
    totals=Counter(x for result in pool.map(worker,range(20)) for x in result)
assert totals=={'recorded':10000},totals
def counts(): return q("SELECT occupied||':'||(SELECT count(*) FROM hl_interest_candidate.tickets)||':'||capacity FROM hl_interest_candidate.budget;")
assert counts()==['10000:10000:10000']
# Repeat the same participant-held ticket concurrently, even when full.
with ThreadPoolExecutor(max_workers=20) as pool:
    retry=Counter(x for result in pool.map(lambda _:q(call(0)),range(100)) for x in result)
assert retry=={'already_recorded':100},retry
assert q(call(10000))==['closed']
assert counts()==['10000:10000:10000']
assert q(f"SELECT hl_interest_candidate.withdraw_interest('{h(0)}');")==['withdrawn_or_absent']
assert q(f"SELECT hl_interest_candidate.withdraw_interest('{h(0)}');")==['withdrawn_or_absent']
assert counts()==['9999:9999:10000']
assert q(call(10000))==['recorded']
# Age one synthetic ticket only; no wall-clock override exposed to clients.
q(f"UPDATE hl_interest_candidate.tickets SET created_at=clock_timestamp()-interval '31 days',expires_at=clock_timestamp()-interval '1 day' WHERE ticket_hash='{h(1)}';".replace("clock_timestamp()","statement_timestamp()"))
assert q(call(1))==['expired']
assert q("SELECT hl_interest_candidate.purge_expired(1);")==['1']
assert q("SELECT hl_interest_candidate.purge_expired(1);")==['0']
assert counts()==['9999:9999:10000']
assert q("SELECT count(*) FROM hl_control.contributor_nodes;")==['5']
print('MOTHER_INTEREST_REHEARSAL_PASSED unique=10000 retries=100 overflow=1 withdrawn=1 expired_purged=1 node_count_unchanged=5')
