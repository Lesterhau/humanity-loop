"""Exercise the shared storage adapter with the existing real-producer fixtures."""
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch
from datetime import datetime,timedelta,timezone
from cap_receipt_pilot import git,Hold
import receipt_state_store as store
import test_critical_guidance_cutover as guidance
import test_federal_policy_cutover as federal
import test_remaining_receipt_cutover as remaining
from test_evidence_integrity_backup import lookup

class StorageTests(unittest.TestCase):
    def exercise(self,writer,case,initial,updated):
        # Seed exact synthetic canonical commit, then only local data-only refs.
        # The real-producer fixture may already have written the updated event
        # into its working tree. Restore the exact initial state before seeding.
        for path in store.PREFIX.values():
            # Only the selected writer's local fixture namespace is cleared.
            if path==store.PREFIX[writer]:
                import shutil
                shutil.rmtree(case.repo/path,ignore_errors=True)
        if writer=='sentinel':
            import shutil
            shutil.rmtree(case.repo/store.R,ignore_errors=True)
        for path,raw in initial.items():
            p=case.repo/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        git(case.repo,'add','-A');git(case.repo,'commit','--allow-empty','-qm','seed canonical state')
        main=git(case.repo,'rev-parse','HEAD').decode().strip()
        anchor=store.seed(case.repo,writer,main)
        ref='refs/heads/receipt-test-'+writer
        git(case.repo,'update-ref',ref,anchor,'0'*40)
        self.assertEqual(store.verified_state(case.repo,writer,anchor,anchor),initial)
        self.assertEqual(store.advance_local(case.repo,writer,ref,anchor,initial),anchor)
        head=store.advance_local(case.repo,writer,ref,anchor,updated)
        self.assertNotEqual(head,anchor)
        self.assertEqual(store.verified_state(case.repo,writer,anchor,head),updated)
        self.assertEqual(git(case.repo,'rev-parse','main').decode().strip(),main)
        with self.assertRaises(subprocess.CalledProcessError):store.advance_local(case.repo,writer,ref,anchor,updated)
        with self.assertRaises(Hold):store.propose(case.repo,writer,head,{**updated,'AGENTS.md':b'{}'})
        with self.assertRaises(Hold):store.advance_local(case.repo,writer,'refs/heads/main',head,updated)
        with self.assertRaises(Hold):store.verified_state(case.repo,writer,anchor,main)
        self.assertEqual(git(case.repo,'rev-parse',ref).decode().strip(),head)
        return anchor,head

    def test_four_actual_producer_state_paths(self):
        # Fixed future-in-fixture timestamps are compared to a simulated host clock,
        # not trusted from the report. No source network calls.
        class Fixed(datetime):
            @classmethod
            def now(cls,tz=None):return datetime(2026,12,3,tzinfo=timezone.utc)
        with patch.object(store,'datetime',Fixed):
            for writer,cls in [('critical',guidance.GuidanceCutover),('federal',federal.FederalCutover)]:
                case=cls();case.setUp();self.addCleanup(case.doCleanups)
                initial=case.prior
                case.produce(case.root,case.start+timedelta(days=1),lambda url:'Synthetic revision '+url)
                updated=case.read_state(case.root)
                anchor,head=self.exercise(writer,case,initial,updated)
                events=[k for k in updated if '/events/' in k]
                self.assertTrue(events)
                with self.assertRaises(Hold):store.propose(case.repo,writer,head,{k:v for k,v in updated.items() if k!=events[0]})
                poisoned=dict(updated);p=store.latest_path(writer);r=json.loads(poisoned[p]);r['runAt']='2099-01-01T00:00:00Z';poisoned[p]=json.dumps(r).encode()
                with self.assertRaisesRegex(Hold,'future_receipt'):store.propose(case.repo,writer,head,poisoned)
            case=remaining.RemainingCutover();case.setUp();self.addCleanup(case.doCleanups)
            names={n for n in remaining.FILES if n.startswith(remaining.EVIDENCE)}
            case.produce(case.a,lookup(),'2026-11-25T03:23:00Z')
            initial=case.read(case.a,names)
            case.produce(case.a,lookup(),'2026-11-26T03:23:00Z')
            updated=case.read(case.a,names)
            _,head=self.exercise('evidence',case,initial,updated)
            q=store.E+'review-queue.json';bad=dict(updated);obj=json.loads(bad[q]);obj['items'][0]['status']='accepted';bad[q]=json.dumps(obj).encode()
            with self.assertRaisesRegex(Hold,'review_queue_changed_or_removed'):store.propose(case.repo,'evidence',head,bad)
            case=remaining.RemainingCutover();case.setUp();self.addCleanup(case.doCleanups)
            names={remaining.SENTINEL,remaining.RECIPROCAL}
            case.sentinel(case.a,'2026-11-25T04:41:00Z',False);case.reciprocal(case.a,'2026-11-25T04:41:00Z')
            initial=case.read(case.a,names)
            case.sentinel(case.a,'2026-11-25T05:41:00Z',True)
            updated=case.read(case.a,names)
            self.exercise('sentinel',case,initial,updated)
        print('SHARED_RECEIPT_STORAGE_CANDIDATE_PASSED four_writers=4 local_cas=true no_main_write=true')


class IntegratedCutoverTests(unittest.TestCase):
    """One repository, five scoped writers, actual combined watchdog consumer.

    Offline synthetic input only. No remote, production ref, credentials, or
    live workflow modification. The anchors are synthetic, not independent
    attestation or authorization for the real migration.
    """
    def test_integrated_five_writer_shadow_cutover(self):
        import tempfile
        import shutil
        import cap_receipt_pilot as cap
        from cap_receipt_consumer import verified_latest
        from cap_daily_audit import build_report,write_report
        from monitor_cadence_gate import scan_due

        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        root=Path(tmp.name);repo=root/'repository';repo.mkdir()
        git(repo,'init','-q','-b','main')
        (repo/'AGENTS.md').write_text('synthetic immutable code\n')
        now=datetime(2026,11,26,13,tzinfo=timezone.utc)
        first=datetime(2026,11,25,12,tzinfo=timezone.utc)
        class Fixed(datetime):
            @classmethod
            def now(cls,tz=None):return now
        node=shutil.which('node')
        self.assertIsNotNone(node)
        script=Path(__file__).with_name('ops_sentinel.js').resolve()
        def materialize(state,target):
            for path,raw in state.items():
                f=target/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
        def watchdog(receipts,when):
            # Missing/invalid receipt is not replaced by a canonical fallback.
            cmd="""const fs=require('node:fs'),s=require(process.argv[1]),now=Number(process.argv[2]);
const data=JSON.parse(fs.readFileSync(0,'utf8'));
const read=p=>{if(p===s.WORKER)return {schemaVersion:1,status:'worked',runAt:new Date(now).toISOString(),lastVerifiedAt:new Date(now).toISOString()};if(!Object.hasOwn(data,p))throw Error('verified receipt unavailable');return data[p]};
process.stdout.write(JSON.stringify(s.evaluate(now,read)));"""
            data={k:json.loads(v) for k,v in receipts.items()}
            return json.loads(subprocess.run([node,'-e',cmd,str(script),str(int(when.timestamp()*1000))],
                input=json.dumps(data).encode(),capture_output=True,check=True,timeout=15,
                env={'PATH':'/usr/bin:/bin','LANG':'C'}).stdout)
        def cap_report(when):
            stamp=when.isoformat().replace('+00:00','Z')
            latest,_=write_report(build_report([],stamp),root/'cap-producer')
            return latest.read_bytes()

        g=guidance.GuidanceCutover();g.setUp();self.addCleanup(g.doCleanups)
        f=federal.FederalCutover();f.setUp();self.addCleanup(f.doCleanups)
        e=remaining.RemainingCutover();e.setUp();self.addCleanup(e.doCleanups)
        names={n for n in remaining.FILES if n.startswith(remaining.EVIDENCE)}
        e.produce(e.a,lookup(),'2026-11-25T12:00:00Z')
        initial={'critical':g.prior,'federal':f.prior,'evidence':e.read(e.a,names)}
        cap_initial=cap_report(first)
        materialize({cap.LATEST:cap_initial,cap.PREFIX+'runs/2026-11-25.json':cap_initial},repo)
        for state in initial.values():materialize(state,repo)
        e.reciprocal(e.a,'2026-11-25T12:00:00Z')
        baseline=watchdog({cap.LATEST:cap_initial,**{store.latest_path(k):v[store.latest_path(k)] for k,v in initial.items()}},first)
        self.assertEqual(baseline['status'],'healthy')
        initial['sentinel']={remaining.SENTINEL:(json.dumps(baseline,indent=2)+'\n').encode(),
                            remaining.RECIPROCAL:(e.a/remaining.RECIPROCAL).read_bytes()}
        materialize(initial['sentinel'],repo)
        git(repo,'add','-A');git(repo,'commit','-qm','synthetic canonical seed')
        main=git(repo,'rev-parse','main').decode().strip()
        refs={w:'refs/heads/receipt-test-'+w for w in ('cap',*initial)}
        with patch.object(store,'datetime',Fixed),patch.object(cap,'trusted_now',return_value=now):
            anchors={'cap':cap.seed(repo,main),**{w:store.seed(repo,w,main) for w in initial}}
            for w,a in anchors.items():git(repo,'update-ref',refs[w],a,'0'*40)
            # Generate real producer updates from the seeded state, without
            # any live network requests or production data.
            next_time=datetime(2026,11,26,12,tzinfo=timezone.utc)
            g.produce(g.root,next_time,lambda url:'Synthetic revised '+url)
            f.produce(f.root,next_time,lambda url:'Synthetic revised '+url)
            e.produce(e.a,lookup(),'2026-11-26T12:00:00Z')
            updated={'critical':g.read_state(g.root),'federal':f.read_state(f.root),'evidence':e.read(e.a,names)}
            cap_next=cap_report(next_time)
            heads={'cap':cap.propose(repo,anchors['cap'],cap_next)}
            git(repo,'update-ref',refs['cap'],heads['cap'],anchors['cap'])
            for w,state in updated.items():heads[w]=store.advance_local(repo,w,refs[w],anchors[w],state)
            verified={cap.LATEST:verified_latest(repo,anchors['cap'],heads['cap'])}
            for w,state in updated.items():
                readback=store.verified_state(repo,w,anchors[w],heads[w])
                self.assertEqual(readback,state)
                verified[store.latest_path(w)]=readback[store.latest_path(w)]
                materialize(readback,root/'verified-consumer')
                with self.assertRaises(subprocess.CalledProcessError):
                    store.advance_local(repo,w,refs[w],anchors[w],state)
            self.assertEqual(verified[cap.LATEST],cap_next)
            self.assertFalse(scan_due(root/'verified-consumer'/store.latest_path('critical'),'schedule',next_time+timedelta(hours=4)))
            healthy=watchdog(verified,now)
            self.assertEqual(healthy['status'],'healthy')
            self.assertEqual([x['status'] for x in healthy['checks']],['ok']*5)
            # Reject a wrong ancestry and prove that the combined watchdog
            # exposes the missing lane, even though main has an older receipt.
            with self.assertRaises(Hold):
                store.verified_state(repo,'critical',anchors['critical'],heads['federal'])
            unavailable=dict(verified);unavailable.pop(store.latest_path('critical'))
            failure=watchdog(unavailable,now)
            self.assertEqual(failure['status'],'critical')
            self.assertEqual(failure['checks'][2]['status'],'critical')
            self.assertEqual(watchdog(verified,now+timedelta(hours=13))['checks'][2]['status'],'critical')
            # Persist the real combined watchdog result through the fifth
            # adapter, retaining the separately produced reciprocal audit.
            sentinel={remaining.SENTINEL:(json.dumps(healthy,indent=2)+'\n').encode(),
                      remaining.RECIPROCAL:initial['sentinel'][remaining.RECIPROCAL]}
            heads['sentinel']=store.advance_local(repo,'sentinel',refs['sentinel'],anchors['sentinel'],sentinel)
            self.assertEqual(store.verified_state(repo,'sentinel',anchors['sentinel'],heads['sentinel']),sentinel)
            # Known good seed is still readable; no destructive rollback.
            for w,state in initial.items():
                self.assertEqual(store.verified_state(repo,w,anchors[w],anchors[w]),state)
            self.assertEqual(cap.read_latest(repo,anchors['cap']),cap_initial)
            self.assertEqual(git(repo,'rev-parse','main').decode().strip(),main)
            self.assertEqual(git(repo,'status','--porcelain'),b'')
            self.assertEqual(git(repo,'remote'),b'')
            for w,h in heads.items():self.assertEqual(git(repo,'rev-parse',refs[w]).decode().strip(),h)
        print('INTEGRATED_FIVE_WRITER_SHADOW_REHEARSAL_PASSED writers=5 watchdog=healthy missing_lane=critical stale_lane=critical main_unchanged=true remote=false')

if __name__=='__main__':unittest.main()
