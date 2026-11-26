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
        for path,raw in initial.items():
            p=case.repo/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        git(case.repo,'add','-A');git(case.repo,'commit','-qm','seed canonical state')
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

if __name__=='__main__':unittest.main()
