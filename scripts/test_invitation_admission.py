#!/usr/bin/env python3
"""Actual concurrent SQL transactions in the existing disposable fixture only."""
import hashlib
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
assert os.environ.get('PGHOST')=='127.0.0.1'
assert os.environ.get('PGDATABASE')=='admission_ci'

def q(sql):
    return subprocess.run(['psql','-X','-A','-t','-q','-v','ON_ERROR_STOP=1'],
        input=sql,text=True,capture_output=True,timeout=30)

def ok(sql):
    r=q(sql)
    if r.returncode: raise AssertionError(r.stderr)
    return r.stdout.splitlines()

def denied(sql,reason):
    r=q(sql)
    assert r.returncode and reason in r.stderr,r.stderr

def h(s): return hashlib.sha256(s.encode()).hexdigest()

def issue(i):
    return f"SELECT hl_control.issue_invitation_candidate('{h(i)}',clock_timestamp()+interval '1 hour');"

def redeem(i,t):
    return f"SELECT hl_control.redeem_invitation_candidate('{h(i)}','{h(t)}');"

def counts():
    return ok("SELECT admitted_total||':'||approved_total||':'||(SELECT count(*) FROM hl_control.contributor_nodes) FROM hl_control.admission_budget_candidate;")

assert counts()==['5:5:5']
ok("UPDATE hl_control.admission_budget_candidate SET approved_total=7;")
ok(issue('invited-one')+issue('invited-two'))
denied(issue('oversubscribed'),'invitation_capacity_unavailable')
denied("INSERT INTO hl_control.contributor_nodes(token_hash) VALUES('uninvited');",'invitation_unavailable')
denied(redeem('unknown','bad'),'invitation_unavailable')
assert counts()==['5:7:5']
# Conflict no-op and failed transaction do not consume reserved capacity.
ok(f"INSERT INTO hl_control.contributor_nodes(token_hash,invitation_hash) VALUES('existing-fixture','{h('invited-two')}') ON CONFLICT DO NOTHING;")
ok("BEGIN;"+redeem('invited-two','rolled-back')+"ROLLBACK;")
assert counts()==['5:7:5']
with ThreadPoolExecutor(max_workers=20) as pool:
    ids=list(pool.map(lambda _:ok(redeem('invited-one','same-client-token'))[0],range(20)))
assert len(set(ids))==1
assert counts()==['6:7:6']
denied(redeem('invited-one','different-token'),'invitation_unavailable')
denied("INSERT INTO hl_control.contributor_nodes(token_hash) VALUES('uninvited-again');",'invitation_unavailable')
node2=ok(redeem('invited-two','second-token'))[0]
assert node2!=ids[0]
assert counts()==['7:7:7']
ok(f"UPDATE hl_control.contributor_nodes SET status='revoked' WHERE node_id='{ids[0]}';")
denied(redeem('invited-one','same-client-token'),'invitation_unavailable')
ok("UPDATE hl_control.admission_budget_candidate SET approved_total=8;")
ok(issue('expiring'))
ok(f"UPDATE hl_control.invitation_candidate SET expires_at=clock_timestamp()-interval '1 second' WHERE invitation_hash='{h('expiring')}';")
denied(redeem('expiring','expired-token'),'invitation_unavailable')
ok(issue('replacement'))
assert counts()==['7:8:7']
assert ok("SELECT has_function_privilege('anon','hl_control.redeem_invitation_candidate(text,text)','EXECUTE') OR has_function_privilege('service_role','hl_control.issue_invitation_candidate(text,timestamptz)','EXECUTE');")==['f']
print('MOTHER_INVITATION_RETRY_REHEARSAL_PASSED concurrent_same_invitation=20 unique_nodes=1 uninvited_denied=true rollback_preserved=true revoked_retry_denied=true expiry_releases_reservation=true')
