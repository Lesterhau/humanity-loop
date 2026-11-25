"""Real CAP producer, synthetic public alert fixtures and disposable local Git."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from cap_daily_audit import build_report,write_report
from cap_receipt_pilot import git,seed,propose,load,read_latest,Hold,LATEST,PREFIX

class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.repo=self.root/'repo';self.repo.mkdir()
        self.g('init','-q','-b','main')
        self.day='2026-11-25'
        self.stamp=self.day+'T12:00:00Z'
        self.raw=self.produce(self.stamp)
        self.put(LATEST,self.raw)
        self.put(PREFIX+'runs/'+self.day+'.json',self.raw)
        self.put(PREFIX+'reviews/human.json',b'{"review":"preserve"}\n')
        self.put('AGENTS.md',b'canonical code\n')
        self.g('add','-A');self.g('commit','-qm','synthetic main')
        self.main=self.g('rev-parse','HEAD')
        self.prior=seed(self.repo,self.main)
    def g(self,*args):
        return git(self.repo,*args).decode().strip()
    def put(self,path,raw):
        p=self.repo/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    def produce(self,stamp,features=None):
        latest,_=write_report(build_report(features or [],stamp),self.root/'producer')
        return latest.read_bytes()
    def later(self):
        return self.produce(self.day+'T13:00:00.123456Z',[{'properties':{'event':'Synthetic fixture'}}])
    def test_seed_only_machine_receipts(self):
        self.assertEqual(set(load(self.repo,self.prior,only=True)),
            {LATEST,PREFIX+'runs/'+self.day+'.json'})
        self.assertEqual(self.g('rev-parse','main'),self.main)
    def test_actual_producer_two_runs_same_day_preserve_history(self):
        first=self.later();next_head=propose(self.repo,self.prior,first)
        second=self.produce(self.day+'T14:00:00Z')
        final=propose(self.repo,next_head,second)
        old=load(self.repo,self.prior,only=True);new=load(self.repo,final,only=True)
        self.assertEqual(new[PREFIX+'runs/'+self.day+'.json'],old[PREFIX+'runs/'+self.day+'.json'])
        self.assertEqual(len(new),4)
        self.assertEqual(read_latest(self.repo,final),second)
        self.assertEqual(self.g('rev-parse',final+'^'),next_head)
        self.assertEqual(self.g('rev-parse','main'),self.main)
    def test_exact_replay_idempotent(self):
        raw=self.later();head=propose(self.repo,self.prior,raw)
        self.assertEqual(propose(self.repo,head,raw),head)
    def test_clock_regression(self):
        with self.assertRaisesRegex(Hold,'receipt_time_regression'):
            propose(self.repo,self.prior,self.produce(self.day+'T11:00:00Z'))
    def test_same_timestamp_conflict(self):
        with self.assertRaisesRegex(Hold,'conflicting_same_timestamp'):
            propose(self.repo,self.prior,self.produce(self.stamp,[{'properties':{'event':'Synthetic'}}]))
    def test_wrong_source(self):
        x=json.loads(self.later());x['source']='https://example.invalid'
        with self.assertRaisesRegex(Hold,'receipt_source'):
            propose(self.repo,self.prior,json.dumps(x).encode())
    def test_count_mismatch(self):
        x=json.loads(self.later());x['bySeverity']['error']+=1
        with self.assertRaisesRegex(Hold,'severity_counts'):
            propose(self.repo,self.prior,json.dumps(x).encode())
    def test_duplicate_json(self):
        with self.assertRaisesRegex(Hold,'duplicate_key'):
            propose(self.repo,self.prior,b'{"schemaVersion":1,"schemaVersion":2}')
    def test_code_tree_not_receipt_branch(self):
        with self.assertRaisesRegex(Hold,'unexpected_receipt_path'):
            propose(self.repo,self.main,self.later())
    def test_stale_compare_and_swap(self):
        self.g('update-ref','refs/heads/receipt-test',self.prior,'0'*40)
        a=propose(self.repo,self.prior,self.later())
        b=propose(self.repo,self.prior,self.produce(self.day+'T15:00:00Z'))
        self.g('update-ref','refs/heads/receipt-test',a,self.prior)
        with self.assertRaises(subprocess.CalledProcessError):
            self.g('update-ref','refs/heads/receipt-test',b,self.prior)
        self.assertEqual(self.g('rev-parse','receipt-test'),a)
    def test_manual_review_untouched(self):
        propose(self.repo,self.prior,self.later())
        self.assertEqual((self.repo/PREFIX/'reviews/human.json').read_bytes(),b'{"review":"preserve"}\n')
    def test_ref_name_not_commit(self):
        with self.assertRaisesRegex(Hold,'immutable_commit_required'):
            propose(self.repo,'main',self.later())

if __name__=='__main__':unittest.main()
