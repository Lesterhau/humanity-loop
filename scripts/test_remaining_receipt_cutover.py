"""Last two receipt-writer compatibility rehearsals, disposable Git only."""
import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from cap_receipt_pilot import git,commit
import evidence_integrity_backup as evidence
from test_evidence_integrity_backup import lookup,RETRACTION

EVIDENCE='runtime/evidence-integrity-backup/'
SENTINEL='runtime/ops-sentinel/latest.json'
RECIPROCAL='runtime/reciprocal-audit/latest.json'
FILES={EVIDENCE+n for n in ('latest.json','state.json','review-queue.json')}|{SENTINEL,RECIPROCAL}
SCRIPT=Path(__file__).with_name('ops_sentinel.js').resolve()
RECIP=Path(__file__).with_name('reciprocal_audit.js').resolve()

class RemainingCutover(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.repo=self.root/'git';self.repo.mkdir()
        git(self.repo,'init','-q','-b','main')
        (self.repo/'AGENTS.md').write_text('synthetic code')
        git(self.repo,'add','-A');git(self.repo,'commit','-qm','main')
        self.main=git(self.repo,'rev-parse','HEAD').decode().strip()
        self.a=self.root/'a';self.b=self.root/'b'
        self.a.mkdir();self.b.mkdir()
        self.node=shutil.which('node')
        self.assertIsNotNone(self.node)

    def read(self,root,names):
        return {n:(root/n).read_bytes() for n in names}

    def store(self,state,parent=None):
        assert set(state)<=FILES
        return commit(self.repo,{k:(git(self.repo,'hash-object','-w','--stdin',data=v).decode().strip(),v) for k,v in state.items()},parent)

    def restore(self,head,root,names):
        found={}
        for row in git(self.repo,'ls-tree','-r','-z',head).split(b'\0'):
            if not row:continue
            meta,rawpath=row.split(b'\t',1)
            mode,kind,oid=meta.decode().split()
            name=rawpath.decode()
            self.assertTrue(mode=='100644' and kind=='blob' and name in names)
            raw=git(self.repo,'cat-file','blob',oid)
            self.assertLessEqual(len(raw),4*1024*1024)
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
            found[name]=raw
        self.assertEqual(set(found),names)
        return found

    def advance(self,ref,old,state):
        head=self.store(state,old)
        git(self.repo,'update-ref',ref,head,old)
        with self.assertRaises(subprocess.CalledProcessError):
            git(self.repo,'update-ref',ref,old,'0'*40)
        self.assertEqual(git(self.repo,'rev-parse','main').decode().strip(),self.main)
        return head

    def produce(self,root,fetch,now,*,append_only=False):
        original=evidence.scan
        with patch.object(evidence,'ROOT',root/EVIDENCE),patch.object(evidence,'scan',side_effect=lambda previous:original(fetch=fetch,previous=previous,now=now)),contextlib.redirect_stdout(io.StringIO()):
            evidence.main(append_only=append_only)

    def js(self,source,*args,raw=b''):
        return subprocess.run([self.node,'-e',source,*map(str,args)],input=raw,capture_output=True,check=True,timeout=15).stdout

    def check_evidence(self,raw,stamp):
        cmd="const s=require(process.argv[1]);const fs=require('node:fs');const r=s.receiptCheck(...s.CHECKS[3],Date.parse(process.argv[2]),()=>JSON.parse(fs.readFileSync(0,'utf8')));process.stdout.write(r.status)"
        return self.js(cmd,SCRIPT,stamp,raw=raw).decode()

    def test_evidence_state_queue_and_recovery(self):
        names={n for n in FILES if n.startswith(EVIDENCE)}
        self.produce(self.a,lookup(),'2026-11-25T03:23:00Z')
        queue=self.a/EVIDENCE/'review-queue.json'
        q=json.loads(queue.read_bytes());q['items'][0]['status']='under-review'
        queue.write_text(json.dumps(q)+'\n')
        old=self.read(self.a,names);seed=self.store(old)
        ref='refs/heads/evidence-test';git(self.repo,'update-ref',ref,seed,'0'*40)
        self.assertEqual(self.restore(seed,self.b,names),old)
        second={'message':{'items':RETRACTION['message']['items']+[{'DOI':'10.1000/notice-two','update-to':[{'DOI':'10.1000/original-two','type':'retraction'}]}]}}
        for root in (self.a,self.b):self.produce(root,lookup(crossref=second,failure='citations'),'2026-11-26T03:23:00Z')
        failed=self.read(self.b,names);self.assertEqual(self.read(self.a,names),failed)
        self.assertEqual(json.loads(failed[EVIDENCE+'state.json'])['seenDois'],json.loads(old[EVIDENCE+'state.json'])['seenDois'])
        self.assertEqual(self.check_evidence(failed[EVIDENCE+'latest.json'],'2026-11-26T03:23:00Z'),'warning')
        head=self.advance(ref,seed,failed)
        self.produce(self.b,lookup(crossref=second),'2026-11-27T03:23:00Z')
        final=self.read(self.b,names);report=json.loads(final[EVIDENCE+'latest.json'])
        state=json.loads(final[EVIDENCE+'state.json']);review=json.loads(final[EVIDENCE+'review-queue.json'])
        self.assertEqual(report['candidateFindingsCount'],1)
        self.assertIsNone(report['clinicalConclusions']);self.assertFalse(report['nativeAppDeployStateSynced'])
        self.assertIn('10.1000/original-two',state['seenDois'])
        self.assertEqual(len(review['items']),2);self.assertEqual(review['items'][0]['status'],'under-review')
        self.assertEqual(self.check_evidence(final[EVIDENCE+'latest.json'],'2026-11-27T03:23:00Z'),'ok')
        self.assertEqual(self.check_evidence(final[EVIDENCE+'latest.json'],'2026-11-29T03:23:00Z'),'critical')
        self.advance(ref,head,final)
        self.assertEqual(self.restore(head,self.root/'evidence-recovery',names),failed)
        print('EVIDENCE_INTEGRITY_DUAL_WRITE_REHEARSAL_PASSED queue_preserved=true failed_doi_retry=true stale_threshold=42h')

    def test_append_only_queue_and_canonical_review_boundary(self):
        import receipt_state_store as store
        from datetime import datetime,timezone
        names={n for n in FILES if n.startswith(EVIDENCE)}
        self.produce(self.a,lookup(),'2026-11-25T03:23:00Z',append_only=True)
        path=self.a/EVIDENCE/'review-queue.json'
        queue=json.loads(path.read_bytes())
        queue['items'][0]['status']='under-review'
        # Existing historical decisions and 499 additional synthetic leads.
        queue['items'].extend({'retractedDoi':'10.1000/old-'+str(i),'citingSource':'MED',
            'citingId':str(i),'status':'unreviewed'} for i in range(499))
        path.write_text(json.dumps(queue)+'\n')
        old=self.read(self.a,names)
        for name,raw in old.items():
            target=self.repo/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        review_path=EVIDENCE+'reviews/synthetic-disposition.json'
        review=self.repo/review_path;review.parent.mkdir(parents=True,exist_ok=True)
        review.write_text('{"fixture":true,"status":"under-review"}\n')
        git(self.repo,'add','-A');git(self.repo,'commit','-qm','synthetic historical queue and separate review')
        main=git(self.repo,'rev-parse','main').decode().strip()
        class Fixed(datetime):
            @classmethod
            def now(cls,tz=None):return datetime(2026,12,3,tzinfo=timezone.utc)
        with patch.object(store,'datetime',Fixed):
            anchor=store.seed(self.repo,'evidence',main)
            self.assertEqual(store.verified_state(self.repo,'evidence',anchor,anchor),old)
            workspace=self.root/'append-only-workspace'
            store.hydrate_lane(self.repo,'evidence',anchor,anchor,workspace)
            self.assertFalse((workspace/review_path).exists())
            second={'message':{'items':RETRACTION['message']['items']+[{'DOI':'10.1000/notice-two',
                'update-to':[{'DOI':'10.1000/original-two','type':'retraction'}]}]}}
            self.produce(workspace,lookup(crossref=second),'2026-11-26T03:23:00Z',append_only=True)
            new=self.read(workspace,names)
            items=json.loads(new[EVIDENCE+'review-queue.json'])['items']
            self.assertEqual(len(items),501)
            self.assertEqual(items[:500],queue['items'])
            self.assertEqual(items[-1]['status'],'unreviewed')
            head=store.prepare_lane(self.repo,'evidence',anchor,anchor,workspace)
            self.assertEqual(store.verified_state(self.repo,'evidence',anchor,head),new)
            with self.assertRaisesRegex(store.Hold,'unexpected_receipt_path'):
                store.propose(self.repo,'evidence',head,{**new,review_path:b'{}'})
            self.assertEqual(review.read_text(),'{"fixture":true,"status":"under-review"}\n')
            # Capacity failure must occur before any file write or seen-DOI advance.
            oversized={'schemaVersion':1,'items':[{'synthetic':'x'*(4*1024*1024)}]}
            with patch.object(evidence,'merge_review_queue',return_value=oversized):
                with self.assertRaisesRegex(ValueError,'evidence_queue_capacity_hold'):
                    self.produce(workspace,lookup(),'2026-11-27T03:23:00Z',append_only=True)
            self.assertEqual(self.read(workspace,names),new)
            self.assertEqual(git(self.repo,'rev-parse','main').decode().strip(),main)
        print('EVIDENCE_APPEND_ONLY_QUEUE_PASSED existing=500 retained=501 independent_review_excluded=true capacity_hold_preserves_state=true')

    def sentinel(self,root,stamp,broken):
        cmd="""const fs=require('node:fs'),path=require('node:path'),s=require(process.argv[1]),root=process.argv[2],now=Date.parse(process.argv[3]),broken=process.argv[4]==='true';
const read=p=>{if(p===s.WORKER)return {schemaVersion:1,status:'worked',runAt:new Date(now).toISOString(),lastVerifiedAt:new Date(now).toISOString()};if(broken&&p.includes('critical-guidance'))throw Error('synthetic missing');return {runAt:new Date(now).toISOString(),findings:[],findingsCount:0,changes:[],changesDetected:0,candidateFindings:[],candidateFindingsCount:0,failures:[],failuresCount:0,coverageGaps:[],coverageGapsCount:0}};
const r=s.evaluate(now,read),changed=s.persistReport(r,path.join(root,'runtime/ops-sentinel/latest.json'));process.stdout.write(JSON.stringify({status:r.status,changed,body:s.alertBody(r)}))"""
        return json.loads(self.js(cmd,SCRIPT,root,stamp,str(broken).lower()))

    def reciprocal(self,root,stamp):
        for path,value in {'AUTOMATION-PROMPT.md':'Case Steward; claim timestamps, not verified completed scans','PROJECT-STATE.md':'Foundry','GOVERNANCE.md':'Tier 0','.github/workflows/ops-sentinel.yml':'schedule:','SCOUT-MESH.md':'claims, not verified finished research'}.items():
            p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value)
        cmd="""const r=require(process.argv[1]);r.main(new Date(process.argv[3]),process.argv[2],async()=>{throw Error('synthetic unavailable')}).then(x=>process.stdout.write(JSON.stringify({ran:x.ran,status:x.receipt.publicMethods.status}))).catch(e=>{console.error(e);process.exitCode=1})"""
        return json.loads(self.js(cmd,RECIP,root,stamp).splitlines()[-1])

    def test_sentinel_and_reciprocal_state(self):
        names={SENTINEL,RECIPROCAL}
        self.assertEqual(self.sentinel(self.a,'2026-11-25T04:41:00Z',False)['status'],'healthy')
        self.assertEqual(self.reciprocal(self.a,'2026-11-25T04:41:00Z'),{'ran':True,'status':'unverified'})
        old=self.read(self.a,names);seed=self.store(old)
        ref='refs/heads/sentinel-test';git(self.repo,'update-ref',ref,seed,'0'*40)
        self.assertEqual(self.restore(seed,self.b,names),old)
        for root in (self.a,self.b):
            self.assertFalse(self.sentinel(root,'2026-11-25T05:41:00Z',False)['changed'])
            self.assertFalse(self.reciprocal(root,'2026-11-25T05:41:00Z')['ran'])
            r=self.sentinel(root,'2026-11-25T06:41:00Z',True)
            self.assertEqual(r['status'],'critical');self.assertTrue(r['changed'])
            self.assertIn('Critical Guidance Delta',r['body'])
        failed=self.read(self.b,names);self.assertEqual(failed,self.read(self.a,names))
        self.assertEqual(failed[RECIPROCAL],old[RECIPROCAL])
        head=self.advance(ref,seed,failed)
        self.assertEqual(self.sentinel(self.b,'2026-11-25T07:41:00Z',False)['status'],'healthy')
        self.assertTrue(self.reciprocal(self.b,'2026-12-02T04:41:00Z')['ran'])
        final=self.read(self.b,names);self.advance(ref,head,final)
        self.assertEqual(self.restore(head,self.root/'sentinel-recovery',names),failed)
        print('OPS_SENTINEL_DUAL_WRITE_REHEARSAL_PASSED transition_preserved=true same_day_dedup=true weekly_audit_preserved=true no_issue_writes=true')

if __name__=='__main__':unittest.main()
