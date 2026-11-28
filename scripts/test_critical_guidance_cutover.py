"""Disposable critical-guidance cutover compatibility test, no live writer.
Use the real producer and real cadence/watchdog consumers with synthetic source text.
No network, remote refs, credentials, medical conclusions or automatic promotion.
"""
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch
from cap_receipt_pilot import git,commit
from critical_guidance_delta import SOURCES,run,fingerprint
from monitor_cadence_gate import scan_due,receipt_coverage_complete

PREFIX='runtime/critical-guidance-delta/'
LATEST=PREFIX+'latest-run.json'
KEYS={s['key']:s for s in SOURCES}
class GuidanceCutover(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo=Path(self.tmp.name)/'repo'
        self.repo.mkdir()
        git(self.repo,'init','-q','-b','main')
        self.root=self.repo/PREFIX
        self.root.mkdir(parents=True)
        self.start=datetime(2026,11,25,12,tzinfo=timezone.utc)
        self.produce(self.root,self.start,lambda url:'Synthetic baseline '+url)
        (self.repo/'AGENTS.md').write_text('synthetic code\n')
        git(self.repo,'add','-A');git(self.repo,'commit','-qm','synthetic main')
        self.main=git(self.repo,'rev-parse','HEAD').decode().strip()
        self.prior=self.read_state(self.root)
        self.seed=self.store(self.prior)
        git(self.repo,'update-ref','refs/heads/guidance-test',self.seed,'0'*40)

    def produce(self,root,when,fetch):
        class Fixed(datetime):
            @classmethod
            def now(cls,tz=None):return when
        with patch('critical_guidance_delta.datetime',Fixed),patch('critical_guidance_delta.fetch_text',side_effect=fetch):
            return run(root)

    def read_state(self,root):
        result={}
        for f in sorted(root.rglob('*')):
            if f.is_dir():continue
            assert not f.is_symlink() and f.is_file()
            name=f.relative_to(root).as_posix()
            raw=f.read_bytes()
            assert len(raw)<=4*1024*1024
            obj=json.loads(raw)
            if name.startswith('snapshots/'):
                key=name.removeprefix('snapshots/').removesuffix('.json')
                assert key in KEYS and all(obj[k]==v for k,v in KEYS[key].items())
                assert obj['fingerprint']==fingerprint(obj['normalizedText'])
            else:
                assert name=='latest-run.json' or re.fullmatch(r'events/\d{8}T\d{6}(?:\.\d{6})?Z\.json',name)
                assert obj['schemaVersion']==1 and obj['sourcesConfigured']==len(KEYS)
                assert obj['changesDetected']==len(obj['changes'])
                assert obj['failuresCount']==len(obj['failures'])
                assert all(c['materiality']=='unreviewed' and c['severity']=='unreviewed' and c['medicalAdvice'] is None for c in obj['changes'])
                if name.startswith('events/'):
                    assert name=='events/'+obj['runAt'].replace(':','').replace('-','')+'.json'
            result[PREFIX+name]=raw
        assert LATEST in result
        assert all(PREFIX+'snapshots/'+k+'.json' in result for k in KEYS)
        return result

    def store(self,state,parent=None):
        return commit(self.repo,{k:(git(self.repo,'hash-object','-w','--stdin',data=v).decode().strip(),v) for k,v in state.items()},parent)

    def extract(self,head,dest):
        for row in git(self.repo,'ls-tree','-r','-z',head).split(b'\0'):
            if not row:continue
            meta,path=row.split(b'\t',1)
            mode,kind,oid=meta.decode().split()
            name=path.decode()
            assert mode=='100644' and kind=='blob' and name.startswith(PREFIX)
            relative=name.removeprefix(PREFIX)
            assert '..' not in Path(relative).parts
            p=dest/relative;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(git(self.repo,'cat-file','blob',oid))
        return self.read_state(dest)

    def watchdog(self,raw,when):
        node=shutil.which('node')
        self.assertIsNotNone(node)
        script=Path(__file__).with_name('ops_sentinel.js').resolve()
        cmd="const fs=require('node:fs');const s=require(process.argv[1]);const r=s.receiptCheck(...s.CHECKS[2],Number(process.argv[2]),()=>JSON.parse(fs.readFileSync(0,'utf8')));process.stdout.write(JSON.stringify(r))"
        return json.loads(subprocess.run([node,'-e',cmd,str(script),str(int(when.timestamp()*1000))],input=raw,capture_output=True,check=True,timeout=10).stdout)['status']

    def test_dual_write_read_and_rollback(self):
        alternate=Path(self.tmp.name)/'alternate'
        self.assertEqual(self.extract(self.seed,alternate),self.prior)
        when=self.start+timedelta(hours=5)
        def updated(url):
            if url==SOURCES[1]['url']:raise RuntimeError('synthetic source unavailable')
            return 'Synthetic revised text '+url
        self.produce(self.root,when,updated)
        self.produce(alternate,when,updated)
        a=self.read_state(self.root);b=self.read_state(alternate)
        self.assertEqual(a,b)
        head=self.store(b,self.seed)
        git(self.repo,'update-ref','refs/heads/guidance-test',head,self.seed)
        self.assertEqual(self.extract(head,Path(self.tmp.name)/'readback'),a)
        self.assertEqual(self.watchdog(b[LATEST],when),'warning')
        self.assertFalse(receipt_coverage_complete(json.loads(b[LATEST])))
        self.assertFalse(scan_due(alternate/'latest-run.json','schedule',when+timedelta(hours=2)))
        self.assertTrue(scan_due(alternate/'latest-run.json','schedule',when+timedelta(hours=3)))
        prior_events={k:v for k,v in b.items() if k.startswith(PREFIX+'events/')}
        self.assertTrue(prior_events)
        recovered=when+timedelta(hours=3)
        self.produce(alternate,recovered,lambda url:'Synthetic recovery '+url)
        final=self.read_state(alternate)
        self.assertTrue(all(final[k]==v for k,v in prior_events.items()))
        new=self.store(final,head)
        git(self.repo,'update-ref','refs/heads/guidance-test',new,head)
        self.assertEqual(self.watchdog(final[LATEST],recovered),'ok')
        self.assertEqual(self.watchdog(final[LATEST],recovered+timedelta(hours=13)),'critical')
        self.assertFalse(scan_due(alternate/'latest-run.json','schedule',recovered+timedelta(hours=4)))
        self.assertTrue(scan_due(alternate/'latest-run.json','schedule',recovered+timedelta(hours=5)))
        # A stale writer cannot advance the reference. Prior known-good state
        # remains recoverable without mutating main or rewriting archive history.
        with self.assertRaises(subprocess.CalledProcessError):
            git(self.repo,'update-ref','refs/heads/guidance-test',head,self.seed)
        self.assertEqual(self.extract(head,Path(self.tmp.name)/'recovery'),b)
        self.assertEqual(git(self.repo,'rev-parse','main').decode().strip(),self.main)
        print('CRITICAL_GUIDANCE_DUAL_WRITE_REHEARSAL_PASSED sources=3 partial_retry=3h complete_retry=5h stale_threshold=12h history_preserved=true')

if __name__=='__main__':unittest.main()
