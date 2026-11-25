"""Synthetic packet and recipient only. Simulate interrupted durable operations."""
import json
import tempfile
import unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch

import review_journal as j
from review_envelope import digest,run
from review_retention import RetentionHold
from test_review_packet import packet

class SimulatedCrash(BaseException): pass

class JournalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys=tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.keys.cleanup)
        root=Path(cls.keys.name)
        cls.key=root/'key.pem'; cert=root/'cert.pem'
        run(['req','-x509','-newkey','rsa:3072','-nodes','-keyout',str(cls.key),'-out',str(cert),'-days','1','-subj','/CN=synthetic-journal-only'])
        cls.key.chmod(0o600)
        cls.cert=cert.read_bytes()
        cls.cpin=digest(run(['x509','-outform','DER'],cls.cert))
        cls.data=json.dumps(packet()).encode()
        cls.ppin=digest(cls.data)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.now=datetime(2026,11,24,23,0,tzinfo=timezone.utc)
        self.expiry=self.now+timedelta(hours=1)
        self.bid='review-journal-01'
    def retain(self,**kw):
        args=dict(now=self.now,ttl_hours=1,storage_authorized=True);args.update(kw)
        return j.retain(self.root,self.bid,self.data,self.cert,self.cpin,self.ppin,**args)
    def recover(self,m,now=None):
        return j.recover(self.root,self.bid,self.cert,self.cpin,self.key,self.ppin,m['envelope_sha256'],now=now or self.now)
    def clean(self,**kw):
        args=dict(now=self.expiry,deletion_authorized=True);args.update(kw)
        return j.cleanup(self.root,[self.bid],**args)
    def test_durable_full_lifecycle(self):
        m=self.retain()
        self.assertEqual(j.state(self.root,self.bid)['state'],'retained')
        clear,summary=self.recover(m)
        self.assertEqual(clear,self.data)
        self.assertFalse(summary['independent_review_completed'])
        result=self.clean()
        self.assertTrue(result['results'][0]['receipt']['deleted'])
        s=j.state(self.root,self.bid)
        self.assertEqual([t['state'] for t in s['transitions']],['storing','retained','deleting','deleted'])
        self.assertFalse((self.root/self.bid).exists())
        self.assertNotIn(self.data,(self.root/j.DB).read_bytes())
    def test_crash_after_storage_verified_on_reopen(self):
        original=j.store
        def crash(*a,**kw):
            original(*a,**kw)
            raise SimulatedCrash()
        with patch('review_journal.store',side_effect=crash):
            with self.assertRaises(SimulatedCrash):self.retain()
        s=j.state(self.root,self.bid)
        self.assertEqual(s['state'],'storing')
        with self.assertRaises(RetentionHold):self.recover(s['manifest'])
        self.assertEqual(j.reconcile(self.root,self.bid,now=self.now),'retained')
        self.assertEqual(self.recover(s['manifest'])[0],self.data)
    def test_crash_before_storage_is_hold(self):
        with patch('review_journal.store',side_effect=SimulatedCrash):
            with self.assertRaises(SimulatedCrash):self.retain()
        self.assertEqual(j.reconcile(self.root,self.bid,now=self.now),'hold')
        self.assertEqual(self.clean()['results'][0]['status'],'hold')
    def test_crash_after_delete_not_false_success(self):
        self.retain()
        original=j.remove
        def crash(*a,**kw):
            original(*a,**kw)
            raise SimulatedCrash()
        with patch('review_journal.remove',side_effect=crash):
            with self.assertRaises(SimulatedCrash):self.clean()
        self.assertFalse((self.root/self.bid).exists())
        self.assertEqual(j.state(self.root,self.bid)['state'],'deleting')
        self.assertEqual(j.reconcile(self.root,self.bid,now=self.expiry),'hold')
        self.assertNotIn('deleted',[x['state'] for x in j.state(self.root,self.bid)['transitions']])
    def test_crash_before_delete_no_automatic_retry(self):
        self.retain()
        with patch('review_journal.remove',side_effect=SimulatedCrash):
            with self.assertRaises(SimulatedCrash):self.clean()
        self.assertEqual(j.reconcile(self.root,self.bid,now=self.expiry),'hold')
        self.assertTrue((self.root/self.bid/'review.cms').exists())
        self.assertEqual(self.clean()['results'][0]['status'],'hold')
    def test_duplicate_id_rejected_even_after_deletion(self):
        self.retain();self.clean()
        with self.assertRaisesRegex(RetentionHold,'bundle_id_already_recorded'):self.retain()
    def test_unrecorded_existing_directory_preserved(self):
        p=self.root/self.bid;p.mkdir();(p/'sentinel').write_text('preserve')
        with self.assertRaises(RetentionHold):self.retain()
        self.assertEqual((p/'sentinel').read_text(),'preserve')
    def test_lock_excludes_second_operator(self):
        with j.journal(self.root):
            with self.assertRaisesRegex(RetentionHold,'journal_busy'):self.retain()
    def test_approval_and_unsafe_journal(self):
        with self.assertRaises(RetentionHold):self.retain(storage_authorized=1)
        self.assertEqual(list(self.root.iterdir()),[])
        target=self.root/'unrelated';target.write_text('preserve')
        (self.root/j.DB).symlink_to(target)
        with self.assertRaises(OSError):self.retain()
        self.assertEqual(target.read_text(),'preserve')
    def test_expiry_and_manifest_tampering(self):
        m=self.retain()
        with self.assertRaises(RetentionHold):self.recover(m,self.expiry)
        p=self.root/self.bid/'manifest.json'
        altered=dict(m,expires_utc=(self.expiry+timedelta(hours=1)).isoformat())
        p.write_text(json.dumps(altered))
        with self.assertRaises(RetentionHold):self.recover(m)
        self.assertEqual(self.clean()['results'][0]['status'],'hold')
        self.assertTrue(p.exists())
