"""Disposable federal-policy cutover compatibility test, no live writer.
Use the real producer and real watchdog consumer with synthetic source text.
No network, remote refs, credentials, legal conclusions or automatic promotion.
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
from federal_policy_delta import SOURCES,run,digest,MAX_EXCERPT

PREFIX='runtime/critical-guidance-delta/'
LATEST=PREFIX+'latest-run.json'
KEYS={s['key']:s for s in SOURCES}
class FederalCutover(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo=Path(self.tmp.name)/'repo'
        self.repo.mkdir()
        git(self.repo,'init','-q','-b','main')
        self.root=self.repo/PREFIX
        self.root.mkdir(parents=True)
        self.start=datetime(2026,11,25,12,tzinfo=timezone.utc)
        self.produce(self.root,self.start,lambda url:('X'*MAX_EXCERPT+' original tail') if url==SOURCES[0]['url'] else 'Synthetic baseline '+url)
        (self.repo/'AGENTS.md').write_text('synthetic code\n')
        git(self.repo,'add','-A');git(self.repo,'commit','-qm','synthetic main')
        self.main=git(self.repo,'rev-parse','HEAD').decode().strip()
        self.prior=self.read_state(self.root)
        self.seed=self.store(self.prior)
        git(self.repo,'update-ref','refs/heads/federal-test',self.seed,'0'*40)

    def produce(self,root,when,fetch):
        class Fixed(datetime):
            @classmethod
            def now(cls,tz=None):return when
        with patch('federal_policy_delta.datetime',Fixed),patch('federal_policy_delta.fetch_text',side_effect=fetch):
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
                assert re.fullmatch(r'[0-9a-f]{64}',obj['hash'])
                assert isinstance(obj['excerpt'],str) and len(obj['excerpt'])<=MAX_EXCERPT
                # Hash covers full source text, not just the stored excerpt.
                if len(obj['excerpt'])<MAX_EXCERPT: assert obj['hash']==digest(obj['excerpt'])
            else:
                assert name=='latest-run.json' or re.fullmatch(r'events/\d{8}T\d{6}(?:\.\d{6})?Z\.json',name)
                assert obj['schemaVersion']==1 and obj['sourcesConfigured']==len(KEYS)
                assert obj['changesDetected']==len(obj['changes'])
                assert obj['failuresCount']==len(obj['failures'])
                assert all(c['reviewStatus']=='needs-neutral-human-or-agent-review' and c['legalConclusion'] is None for c in obj['changes'])
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
        cmd="const fs=require('node:fs');const s=require(process.argv[1]);const r=s.receiptCheck(...s.CHECKS[1],Number(process.argv[2]),()=>JSON.parse(fs.readFileSync(0,'utf8')));process.stdout.write(JSON.stringify(r))"
        return json.loads(subprocess.run([node,'-e',cmd,str(script),str(int(when.timestamp()*1000))],input=raw,capture_output=True,check=True,timeout=10).stdout)['status']

    def test_dual_write_read_and_rollback(self):
        self.assertEqual(len(KEYS),17)
        alternate=Path(self.tmp.name)/'alternate'
        self.assertEqual(self.extract(self.seed,alternate),self.prior)
        when=self.start+timedelta(days=1)
        # Change beyond the stored excerpt: full-source hash must still differ.
        changed_url=SOURCES[0]['url']
        failed_url=SOURCES[1]['url']
        def updated(url):
            if url==failed_url: raise RuntimeError('synthetic source unavailable')
            if url==changed_url: return 'X'*MAX_EXCERPT+' changed beyond excerpt'
            return 'Synthetic baseline '+url
        self.produce(self.root,when,updated)
        self.produce(alternate,when,updated)
        a=self.read_state(self.root);b=self.read_state(alternate)
        self.assertEqual(a,b)
        latest=json.loads(b[LATEST])
        self.assertEqual((latest['changesDetected'],latest['failuresCount']),(1,1))
        self.assertEqual(latest['changes'][0]['sourceKey'],SOURCES[0]['key'])
        self.assertEqual(latest['changes'][0]['olderExcerpt'],latest['changes'][0]['newerExcerpt'])
        self.assertNotEqual(latest['changes'][0]['olderHash'],latest['changes'][0]['newerHash'])
        self.assertEqual(latest['failures'][0]['sourceKey'],SOURCES[1]['key'])
        for source in SOURCES[1:]:
            key=PREFIX+'snapshots/'+source['key']+'.json'
            self.assertEqual(b[key],self.prior[key])
        head=self.store(b,self.seed)
        git(self.repo,'update-ref','refs/heads/federal-test',head,self.seed)
        self.assertEqual(self.extract(head,Path(self.tmp.name)/'readback'),a)
        self.assertEqual(self.watchdog(b[LATEST],when),'warning')
        prior_events={k:v for k,v in b.items() if k.startswith(PREFIX+'events/')}
        self.assertTrue(prior_events)
        recovered=when+timedelta(days=1)
        self.produce(alternate,recovered,lambda url:'Synthetic recovery '+url)
        final=self.read_state(alternate)
        self.assertTrue(all(final[k]==v for k,v in prior_events.items()))
        new=self.store(final,head)
        git(self.repo,'update-ref','refs/heads/federal-test',new,head)
        self.assertEqual(self.watchdog(final[LATEST],recovered),'ok')
        self.assertEqual(self.watchdog(final[LATEST],recovered+timedelta(hours=41)),'critical')
        with self.assertRaises(subprocess.CalledProcessError):
            git(self.repo,'update-ref','refs/heads/federal-test',head,self.seed)
        self.assertEqual(self.extract(head,Path(self.tmp.name)/'recovery'),b)
        self.assertEqual(git(self.repo,'rev-parse','main').decode().strip(),self.main)
        print('FEDERAL_POLICY_DUAL_WRITE_REHEARSAL_PASSED sources=17 unchanged_snapshots=16 partial_warning=true stale_threshold=40h history_preserved=true')

if __name__=='__main__':unittest.main()
