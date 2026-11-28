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
        canonical=root/'canonical-heartbeat';canonical.mkdir()
        worker='runtime/ops/hourly-worker.json'
        def heartbeat(when):
            stamp=when.isoformat().replace('+00:00','Z')
            materialize({worker:json.dumps({'schemaVersion':1,'status':'worked',
                'runAt':stamp,'lastVerifiedAt':stamp}).encode()},canonical)
        heartbeat(first)
        def watchdog(receipts,when):
            # Separate on-disk synthetic heartbeat and verified detector paths.
            # A missing detector cannot fall back to a canonical old receipt.
            target=Path(tempfile.mkdtemp(dir=root))
            materialize(receipts,target)
            cmd="""const s=require(process.argv[1]),now=Number(process.argv[2]);
process.stdout.write(JSON.stringify(s.evaluateVerified(now,process.argv[3],process.argv[4])));"""
            return json.loads(subprocess.run([node,'-e',cmd,str(script),str(int(when.timestamp()*1000)),
                str(canonical),str(target)],capture_output=True,check=True,timeout=15,
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
        e.reciprocal(repo,'2026-11-18T12:00:00Z')
        baseline=watchdog({cap.LATEST:cap_initial,**{store.latest_path(k):v[store.latest_path(k)] for k,v in initial.items()}},first)
        self.assertEqual(baseline['status'],'healthy')
        initial['sentinel']={remaining.SENTINEL:(json.dumps(baseline,indent=2)+'\n').encode(),
                            remaining.RECIPROCAL:(repo/remaining.RECIPROCAL).read_bytes()}
        materialize(initial['sentinel'],repo)
        git(repo,'add','-A');git(repo,'commit','-qm','synthetic canonical seed')
        main=git(repo,'rev-parse','main').decode().strip()
        refs={w:'refs/heads/receipt-test-'+w for w in ('cap',*initial)}
        import contextlib,io,sys
        def cli(operation,writer,*args):
            output=io.StringIO()
            argv=['receipt_state_store.py',operation,'--repo',str(repo),'--writer',writer,*map(str,args)]
            with patch.object(sys,'argv',argv),contextlib.redirect_stdout(output):
                store.main()
            return output.getvalue().strip()
        def pinned(w):
            return ['--anchor',anchors[w],'--head',anchors[w]]
        with patch.object(store,'datetime',Fixed),patch.object(cap,'trusted_now',return_value=now):
            before_refs=git(repo,'for-each-ref','--format=%(objectname) %(refname)')
            seeds={w:json.loads(cli('seed',w,'--canonical',main)) for w in refs}
            self.assertTrue(all(s['canonical']==main and s['remote_promoted'] is False and s['writer']==w for w,s in seeds.items()))
            self.assertEqual(git(repo,'for-each-ref','--format=%(objectname) %(refname)'),before_refs)
            anchors={w:s['candidate_anchor'] for w,s in seeds.items()}
            for w,a in anchors.items():git(repo,'update-ref',refs[w],a,'0'*40)
            # Generate real producer updates from the seeded state, without
            # any live network requests or production data.
            workspaces={w:root/('workspace-'+w) for w in anchors}
            for w,a in anchors.items():
                hydrated=json.loads(cli('hydrate',w,*pinned(w),'--workspace',workspaces[w]))
                self.assertEqual(hydrated['head'],a)
                self.assertEqual(hydrated['files'],seeds[w]['files'])
            with self.assertRaisesRegex(Hold,'workspace_must_be_new'):
                store.hydrate_lane(repo,'cap',anchors['cap'],anchors['cap'],workspaces['cap'])
            next_time=datetime(2026,11,26,12,tzinfo=timezone.utc)
            gdir=workspaces['critical']/store.G
            fdir=workspaces['federal']/store.F
            g.produce(gdir,next_time,lambda url:'Synthetic revised '+url)
            f.produce(fdir,next_time,lambda url:'Synthetic revised '+url)
            e.produce(workspaces['evidence'],lookup(),'2026-11-26T12:00:00Z',append_only=True)
            updated={'critical':g.read_state(gdir),'federal':f.read_state(fdir),'evidence':e.read(workspaces['evidence'],names)}
            cap_latest,_=write_report(build_report([],next_time.isoformat().replace('+00:00','Z')),workspaces['cap']/cap.PREFIX)
            cap_next=cap_latest.read_bytes()
            heads={}
            for w in ('cap','critical','federal','evidence'):
                candidate=cli('candidate',w,*pinned(w),'--workspace',workspaces[w])
                check=json.loads(cli('verify',w,'--anchor',anchors[w],'--head',candidate))
                self.assertEqual(check['head'],candidate)
                self.assertEqual(git(repo,'rev-parse',refs[w]).decode().strip(),anchors[w])
                git(repo,'update-ref',refs[w],candidate,anchors[w])
                heads[w]=candidate
            verified={cap.LATEST:store.verified_lane(repo,'cap',anchors['cap'],heads['cap'])[cap.LATEST]}
            for w,state in updated.items():
                readback=store.verified_lane(repo,w,anchors[w],heads[w])
                self.assertEqual(readback,state)
                verified[store.latest_path(w)]=readback[store.latest_path(w)]
                materialize(readback,root/'verified-consumer')
                with self.assertRaises(subprocess.CalledProcessError):
                    store.advance_local(repo,w,refs[w],anchors[w],state)
            self.assertEqual(verified[cap.LATEST],cap_next)
            self.assertFalse(scan_due(root/'verified-consumer'/store.latest_path('critical'),'schedule',next_time+timedelta(hours=4)))
            heartbeat(now)
            # Even a plausible worker report in the migrated workspace cannot
            # substitute for the separate canonical self-report.
            worker_bytes=(canonical/worker).read_bytes()
            (canonical/worker).unlink()
            self.assertEqual(watchdog({**verified,worker:worker_bytes},now)['checks'][4]['status'],'warning')
            heartbeat(now)
            healthy=watchdog(verified,now)
            self.assertEqual(healthy['status'],'healthy')
            self.assertEqual([x['status'] for x in healthy['checks']],['ok']*5)
            # Reject a wrong ancestry and prove that the combined watchdog
            # exposes the missing lane, even though main has an older receipt.
            with self.assertRaises(Hold):
                store.verified_state(repo,'critical',anchors['critical'],heads['federal'])
            unavailable=dict(verified);unavailable.pop(store.latest_path('critical'))
            materialize({store.latest_path('critical'):verified[store.latest_path('critical')]},canonical)
            failure=watchdog(unavailable,now)
            self.assertEqual(failure['status'],'critical')
            self.assertEqual(failure['checks'][2]['status'],'critical')
            self.assertEqual(watchdog(verified,now+timedelta(hours=13))['checks'][2]['status'],'critical')
            # Execute the real weekly producer using canonical documents and
            # the hydrated receipt workspace; no external source fetch.
            reciprocal=Path(__file__).with_name('reciprocal_audit.js').resolve()
            cmd="""const r=require(process.argv[1]);r.main(new Date(process.argv[4]),process.argv[2],async()=>{throw Error('synthetic unavailable')},process.argv[3]).then(x=>process.stdout.write(JSON.stringify({ran:x.ran,status:x.receipt.publicMethods.status}))).catch(e=>{console.error(e);process.exitCode=1})"""
            def run_reciprocal():
                out=subprocess.run([node,'-e',cmd,str(reciprocal),str(repo),str(workspaces['sentinel']),now.isoformat()],capture_output=True,check=True,timeout=15,env={'PATH':'/usr/bin:/bin','LANG':'C'}).stdout
                return json.loads(out.splitlines()[-1])
            self.assertEqual(run_reciprocal(),{'ran':True,'status':'unverified'})
            self.assertEqual(run_reciprocal(),{'ran':False,'status':'unverified'})
            self.assertEqual((repo/remaining.RECIPROCAL).read_bytes(),initial['sentinel'][remaining.RECIPROCAL])
            sentinel={remaining.SENTINEL:(json.dumps(healthy,indent=2)+'\n').encode(),
                      remaining.RECIPROCAL:(workspaces['sentinel']/remaining.RECIPROCAL).read_bytes()}
            self.assertNotEqual(sentinel[remaining.RECIPROCAL],initial['sentinel'][remaining.RECIPROCAL])
            materialize(sentinel,workspaces['sentinel'])
            heads['sentinel']=cli('candidate','sentinel',*pinned('sentinel'),'--workspace',workspaces['sentinel'])
            self.assertEqual(json.loads(cli('verify','sentinel','--anchor',anchors['sentinel'],'--head',heads['sentinel']))['head'],heads['sentinel'])
            self.assertEqual(git(repo,'rev-parse',refs['sentinel']).decode().strip(),anchors['sentinel'])
            git(repo,'update-ref',refs['sentinel'],heads['sentinel'],anchors['sentinel'])
            self.assertEqual(store.verified_lane(repo,'sentinel',anchors['sentinel'],heads['sentinel']),sentinel)
            # A symlink cannot substitute producer data in the candidate path.
            bad=workspaces['sentinel']/remaining.SENTINEL
            bad.unlink()
            bad.symlink_to(repo/'AGENTS.md')
            with self.assertRaisesRegex(Hold,'unsafe_workspace_path'):
                store.prepare_lane(repo,'sentinel',anchors['sentinel'],heads['sentinel'],workspaces['sentinel'])
            # Known good seed is still readable; no destructive rollback.
            for w,state in initial.items():
                self.assertEqual(store.verified_state(repo,w,anchors[w],anchors[w]),state)
            self.assertEqual(cap.read_latest(repo,anchors['cap']),cap_initial)
            self.assertEqual(git(repo,'rev-parse','main').decode().strip(),main)
            self.assertEqual(git(repo,'status','--porcelain'),b'')
            self.assertEqual(git(repo,'remote'),b'')
            for w,h in heads.items():self.assertEqual(git(repo,'rev-parse',refs[w]).decode().strip(),h)
        print('INTEGRATED_FIVE_WRITER_SHADOW_REHEARSAL_PASSED writers=5 watchdog=healthy missing_lane=critical stale_lane=critical main_unchanged=true remote=false heartbeat_canonical=true reciprocal_real_producer=true workflow_cli=true seed_refs_unchanged=true')

class HistoryScalingTests(unittest.TestCase):
    def test_fifty_transitions_read_only_changed_blobs(self):
        import tempfile
        import cap_receipt_pilot as cap
        from cap_daily_audit import build_report
        from cap_receipt_consumer import verified_latest
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        repo=Path(tmp.name)
        git(repo,'init','-q','-b','main')
        first=datetime(2026,11,25,12,tzinfo=timezone.utc)
        now=first+timedelta(days=1)
        def raw(when):
            return (json.dumps(build_report([],when.isoformat().replace('+00:00','Z')),sort_keys=True)+'\n').encode()
        initial=raw(first)
        for path in (cap.LATEST,cap.PREFIX+'runs/2026-11-25.json'):
            file=repo/path;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(initial)
        git(repo,'add','-A');git(repo,'commit','-qm','synthetic seed')
        main=git(repo,'rev-parse','main').decode().strip()
        with patch.object(cap,'trusted_now',return_value=now):
            anchor=cap.seed(repo,main);head=anchor
            for i in range(1,51):
                head=cap.propose(repo,head,raw(first+timedelta(minutes=i)))
            with patch.object(cap,'git',wraps=git) as measured,patch.object(cap,'parse',wraps=cap.parse) as parses:
                state=cap.verified_history(repo,anchor,head)
                reads=sum(c.args[1:3]==('cat-file','blob') for c in measured.call_args_list)
                sizes=sum(c.args[1:3]==('cat-file','-s') for c in measured.call_args_list)
                self.assertEqual(reads,51)
                self.assertEqual(sizes,0)
                self.assertEqual(parses.call_count,51)
            self.assertEqual(len(state),52)
            self.assertEqual(verified_latest(repo,anchor,head),raw(first+timedelta(minutes=50)))
            # A later apparently healthy endpoint cannot conceal an invalid intermediate tree.
            bad=dict(state);bad.pop(cap.PREFIX+'runs/2026-11-25.json')
            broken=cap.commit(repo,bad,head)
            restored=cap.commit(repo,state,broken)
            with self.assertRaisesRegex(Hold,'historical_archive_changed'):
                verified_latest(repo,anchor,restored)
        self.assertEqual(git(repo,'rev-parse','main').decode().strip(),main)
        self.assertEqual(git(repo,'remote'),b'')

        # A shared-lane history with one unchanged and one changed object per run.
        case=remaining.RemainingCutover();case.setUp();self.addCleanup(case.doCleanups)
        case.sentinel(case.a,'2026-11-25T12:00:00Z',False)
        case.reciprocal(case.a,'2026-11-25T12:00:00Z')
        state=case.read(case.a,{remaining.SENTINEL,remaining.RECIPROCAL})
        anchor=store.write(case.repo,state);head=anchor
        class Fixed(datetime):
            @classmethod
            def now(cls,tz=None):return now
        with patch.object(store,'datetime',Fixed):
            for i in range(1,51):
                updated=dict(state);report=json.loads(state[remaining.SENTINEL])
                report['runAt']=(first+timedelta(minutes=i)).isoformat().replace('+00:00','Z')
                updated[remaining.SENTINEL]=json.dumps(report).encode()
                head=store.propose(case.repo,'sentinel',head,updated);state=updated
            with patch.object(store,'git',wraps=git) as measured,patch.object(store,'parse',wraps=store.parse) as parses:
                self.assertEqual(store.verified_state(case.repo,'sentinel',anchor,head),state)
                reads=sum(c.args[1:3]==('cat-file','blob') for c in measured.call_args_list)
                sizes=sum(c.args[1:3]==('cat-file','-s') for c in measured.call_args_list)
                self.assertEqual(reads,52)
                self.assertEqual(sizes,0)
                self.assertEqual(parses.call_count,52)
        print('RECEIPT_HISTORY_SCALING_PASSED transitions_per_lane=50 cap_blob_reads=51 shared_blob_reads=52 per_blob_size_calls=0 intermediate_tamper_rejected=true')


if __name__=='__main__':unittest.main()
