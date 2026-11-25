"""Disposable Git receipts tested against the existing Ops Sentinel consumer."""
import json
import tempfile
import unittest
from datetime import datetime,timezone,timedelta
from pathlib import Path
from cap_daily_audit import build_report
from cap_receipt_pilot import git,seed,propose,load,commit,Hold,LATEST,PREFIX
from cap_receipt_consumer import assess,verified_latest

class ConsumerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo=Path(self.tmp.name)
        git(self.repo,'init','-q','-b','main')
        self.time=datetime(2026,11,25,12,tzinfo=timezone.utc)
        self.now=int((self.time+timedelta(hours=2)).timestamp()*1000)
        self.old=self.report(self.time)
        for name in (LATEST,PREFIX+'runs/2026-11-25.json'):
            p=self.repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(self.old)
        git(self.repo,'add','-A');git(self.repo,'commit','-qm','synthetic code base')
        self.main=git(self.repo,'rev-parse','HEAD').decode().strip()
        self.anchor=seed(self.repo,self.main)
        self.fresh=self.report(self.time+timedelta(hours=1))
        self.head=propose(self.repo,self.anchor,self.fresh)
    def report(self,t):
        return (json.dumps(build_report([],t.isoformat().replace('+00:00','Z')),sort_keys=True)+'\n').encode()
    def check(self,head,now=None):
        return assess(self.repo,self.anchor,head,self.now if now is None else now)['check']
    def test_fresh_separate_receipt_healthy(self):
        self.assertEqual(verified_latest(self.repo,self.anchor,self.head),self.fresh)
        self.assertEqual(self.check(self.head)['status'],'ok')
        self.assertEqual(git(self.repo,'rev-parse','main').decode().strip(),self.main)
    def test_stale_separate_receipt_critical(self):
        self.assertEqual(self.check(self.head,self.now+41*3600000)['status'],'critical')
    def test_missing_commit_no_main_fallback(self):
        self.assertEqual(self.check('f'*40)['status'],'critical')
    def test_unrelated_history_rejected(self):
        other=commit(self.repo,load(self.repo,self.head,only=True))
        with self.assertRaisesRegex(Hold,'receipt_ancestry_unverified'):
            verified_latest(self.repo,self.anchor,other)
        self.assertEqual(self.check(other)['status'],'critical')
    def test_rewritten_archive_rejected_despite_ancestry(self):
        entries=load(self.repo,self.head,only=True)
        changed=self.report(self.time-timedelta(minutes=1))
        oid=git(self.repo,'hash-object','-w','--stdin',data=changed).decode().strip()
        entries[PREFIX+'runs/2026-11-25.json']=(oid,changed)
        forged=commit(self.repo,entries,self.head)
        with self.assertRaises(Hold):
            verified_latest(self.repo,self.anchor,forged)
        self.assertEqual(self.check(forged)['status'],'critical')
    def test_future_receipt_critical(self):
        head=propose(self.repo,self.head,self.report(self.time+timedelta(hours=4)))
        self.assertEqual(self.check(head)['status'],'critical')

if __name__=='__main__': unittest.main()
