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

def at(fn,*args,now,**kwargs):
    # Test-only clock substitution; no public time argument.
    with patch('review_journal._wall_clock',return_value=now):
        return fn(*args,**kwargs)


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
        return at(j.retain,self.root,self.bid,self.data,self.cert,self.cpin,self.ppin,**args)
    def recover(self,m,now=None):
        return at(j.recover,self.root,self.bid,self.cert,self.cpin,self.key,self.ppin,m['envelope_sha256'],now=now or self.now)
    def clean(self,**kw):
        args=dict(now=self.expiry,deletion_authorized=True);args.update(kw)
        return at(j.cleanup,self.root,[self.bid],**args)
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
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.now),'retained')
        self.assertEqual(self.recover(s['manifest'])[0],self.data)
    def test_crash_before_storage_is_hold(self):
        with patch('review_journal.store',side_effect=SimulatedCrash):
            with self.assertRaises(SimulatedCrash):self.retain()
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.now),'hold')
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
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.expiry),'hold')
        self.assertNotIn('deleted',[x['state'] for x in j.state(self.root,self.bid)['transitions']])
    def test_crash_before_delete_no_automatic_retry(self):
        self.retain()
        with patch('review_journal.remove',side_effect=SimulatedCrash):
            with self.assertRaises(SimulatedCrash):self.clean()
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.expiry),'hold')
        self.assertTrue((self.root/self.bid/'review.cms').exists())
        self.assertEqual(self.clean()['results'][0]['status'],'hold')
    def test_duplicate_id_rejected_even_after_deletion(self):
        self.retain();self.clean()
        with self.assertRaisesRegex(RetentionHold,'bundle_id_already_recorded'):self.retain(now=self.expiry)
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
        with self.assertRaisesRegex(RetentionHold,'clock_rollback_detected'):self.recover(m)
        self.assertEqual(self.clean()['results'][0]['status'],'hold')
        self.assertTrue(p.exists())


    def test_held_expired_ciphertext_purge_preserves_unrelated_files(self):
        self.retain()
        p=self.root/self.bid
        (p/'manifest.json').write_text('corrupt')
        (p/'unrelated').write_text('preserve')
        self.assertEqual(self.clean()['results'][0]['status'],'hold')
        result=at(j.purge_expired_held,self.root,self.bid,now=self.expiry,purge_authorized=True)
        self.assertEqual(result['status'],'purged_unverified')
        self.assertFalse(result['deletion_verified'])
        self.assertFalse((p/'review.cms').exists())
        self.assertEqual((p/'manifest.json').read_text(),'corrupt')
        self.assertEqual((p/'unrelated').read_text(),'preserve')
        self.assertEqual(j.state(self.root,self.bid)['state'],'purged_unverified')
        with self.assertRaises(RetentionHold):self.retain()

    def test_held_purge_needs_expiry_and_exact_approval(self):
        self.retain()
        (self.root/self.bid/'manifest.json').write_text('corrupt')
        self.clean()
        for v in (False,1,'true',None):
            with self.assertRaises(RetentionHold):
                at(j.purge_expired_held,self.root,self.bid,now=self.expiry,purge_authorized=v)
        with self.assertRaises(RetentionHold):
            at(j.purge_expired_held,self.root,self.bid,now=self.now,purge_authorized=True)
        self.assertTrue((self.root/self.bid/'review.cms').exists())

    def test_missing_ciphertext_not_certified_as_purged(self):
        self.retain()
        p=self.root/self.bid/'review.cms';p.unlink()
        self.clean()
        r=at(j.purge_expired_held,self.root,self.bid,now=self.expiry,purge_authorized=True)
        self.assertEqual(r['status'],'hold')
        self.assertFalse(r['deletion_verified'])

    def test_purge_does_not_follow_ciphertext_symlink(self):
        self.retain()
        p=self.root/self.bid/'review.cms'
        p.unlink()
        sentinel=self.root/'unrelated';sentinel.write_text('preserve')
        p.symlink_to(sentinel)
        self.clean()
        r=at(j.purge_expired_held,self.root,self.bid,now=self.expiry,purge_authorized=True)
        self.assertEqual(r['status'],'hold')
        self.assertTrue(p.is_symlink())
        self.assertEqual(sentinel.read_text(),'preserve')

    def test_interrupted_purge_never_certifies_deletion(self):
        self.retain()
        p=self.root/self.bid/'manifest.json';p.unlink()
        self.clean()
        import os
        original=os.unlink
        def crash(*args,**kwargs):
            original(*args,**kwargs)
            raise SimulatedCrash()
        with patch('review_journal.os.unlink',side_effect=crash):
            with self.assertRaises(SimulatedCrash):
                at(j.purge_expired_held,self.root,self.bid,now=self.expiry,purge_authorized=True)
        self.assertEqual(j.state(self.root,self.bid)['state'],'purging')
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.expiry),'hold')
        self.assertNotIn('purged_unverified',[t['state'] for t in j.state(self.root,self.bid)['transitions']])

    def test_unexpired_or_retained_bundle_not_purge_eligible(self):
        self.retain()
        with self.assertRaises(RetentionHold):
            at(j.purge_expired_held,self.root,self.bid,now=self.expiry,purge_authorized=True)
        self.assertTrue((self.root/self.bid/'review.cms').exists())

    def test_expired_recovery_cannot_rewind_clock(self):
        m=self.retain()
        with self.assertRaisesRegex(RetentionHold,'expired'):
            self.recover(m,self.expiry)
        with self.assertRaisesRegex(RetentionHold,'clock_rollback_detected'):
            self.recover(m,self.now)
        self.assertEqual(self.clean()['results'][0]['status'],'deleted')

    def test_public_api_rejects_caller_time(self):
        m=self.retain()
        with self.assertRaises(TypeError):
            j.recover(self.root,self.bid,self.cert,self.cpin,self.key,self.ppin,m['envelope_sha256'],now=self.now)

    def test_clock_rollback_prevents_mutation(self):
        self.retain()
        with self.assertRaisesRegex(RetentionHold,'clock_rollback_detected'):
            self.clean(now=self.now-timedelta(seconds=1))
        self.assertEqual(j.state(self.root,self.bid)['state'],'retained')

    def test_clock_watermark_missing_existing_journal_fails_closed(self):
        m=self.retain()
        with j.journal(self.root) as (db,fd):
            with db: db.execute('DELETE FROM clock_watermark')
        with self.assertRaisesRegex(RetentionHold,'clock_watermark_missing'):
            self.recover(m)

    def test_expiry_during_decryption_refuses_plaintext(self):
        m=self.retain()
        with patch('review_journal._wall_clock',side_effect=[self.now,self.expiry]):
            with self.assertRaisesRegex(RetentionHold,'expired_during_recovery'):
                j.recover(self.root,self.bid,self.cert,self.cpin,self.key,self.ppin,m['envelope_sha256'])
        with self.assertRaisesRegex(RetentionHold,'clock_rollback_detected'):
            self.recover(m)


    def test_revocation_before_expiry_is_durable(self):
        m=self.retain()
        result=at(j.revoke,self.root,self.bid,now=self.now,revocation_authorized=True)
        self.assertEqual(result['status'],'revoked')
        self.assertTrue(result['local_removal_confirmed'])
        self.assertFalse((self.root/self.bid).exists())
        with self.assertRaisesRegex(RetentionHold,'not_retained'):self.recover(m)
        self.assertEqual([x['state'] for x in j.state(self.root,self.bid)['transitions']],
                         ['storing','retained','revoking','revoked'])
        with self.assertRaisesRegex(RetentionHold,'bundle_id_already_recorded'):self.retain()

    def test_revocation_requires_exact_approval(self):
        m=self.retain()
        for v in (False,1,'true',None):
            with self.assertRaisesRegex(RetentionHold,'revocation_approval_missing'):
                at(j.revoke,self.root,self.bid,now=self.now,revocation_authorized=v)
        self.assertEqual(self.recover(m)[0],self.data)

    def test_revocation_corrupt_manifest_denies_recovery(self):
        m=self.retain()
        p=self.root/self.bid
        (p/'manifest.json').write_text('corrupt')
        result=at(j.revoke,self.root,self.bid,now=self.now,revocation_authorized=True)
        self.assertEqual(result['status'],'hold')
        self.assertFalse(result['local_removal_confirmed'])
        self.assertTrue(result['journal_access_revoked'])
        with self.assertRaisesRegex(RetentionHold,'not_retained'):self.recover(m)
        self.assertTrue((p/'review.cms').exists())
        self.assertEqual(at(j.purge_expired_held,self.root,self.bid,now=self.expiry,
                         purge_authorized=True)['status'],'purged_unverified')

    def test_interrupted_revocation_not_recovered_as_retained(self):
        m=self.retain()
        with patch('review_journal.remove',side_effect=SimulatedCrash):
            with self.assertRaises(SimulatedCrash):
                at(j.revoke,self.root,self.bid,now=self.now,revocation_authorized=True)
        self.assertEqual(j.state(self.root,self.bid)['state'],'revoking')
        with self.assertRaisesRegex(RetentionHold,'not_retained'):self.recover(m)
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.now),'hold')
        with self.assertRaisesRegex(RetentionHold,'not_retained'):self.recover(m)

    def test_revocation_after_expiry_no_false_review_claim(self):
        self.retain()
        result=at(j.revoke,self.root,self.bid,now=self.expiry,revocation_authorized=True)
        self.assertEqual(result['status'],'revoked')
        self.assertFalse(result['independent_review_completed'])
        with self.assertRaisesRegex(RetentionHold,'revocation_not_eligible'):
            at(j.revoke,self.root,self.bid,now=self.expiry,revocation_authorized=True)
