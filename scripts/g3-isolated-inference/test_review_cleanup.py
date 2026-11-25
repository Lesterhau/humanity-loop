"""Synthetic manifests and temporary files only."""
import copy
import tempfile
import unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from review_retention import store,digest,RetentionHold
from review_cleanup import sweep,MAX_BATCH

class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.now=datetime(2026,11,24,23,0,tzinfo=timezone.utc)
        # Synthetic CMS marker only; cryptographic integration is tested separately.
        self.data=b'\x30\x06\x0b\x2a\x86\x48\x86\xf7\x0d\x01\x09\x10\x01\x17fixture'
    def bundle(self,bid='review-test-01',ttl=1):
        return store(self.root,bid,self.data,envelope_sha256=digest(self.data),
                     packet_sha256='1'*64,recipient_cert_sha256='2'*64,
                     now=self.now,ttl_hours=ttl,storage_authorized=True)
    def clean(self,manifests,**kw):
        args=dict(now=self.now+timedelta(hours=1),deletion_authorized=True)
        args.update(kw)
        return sweep(self.root,manifests,**args)
    def test_expired_only_and_unrelated_preserved(self):
        a=self.bundle();b=self.bundle('review-test-02',2)
        sentinel=self.root/'unrelated';sentinel.write_text('preserve')
        r=self.clean([a,b])
        self.assertEqual(r['deleted'],1)
        self.assertFalse((self.root/a['bundle_id']).exists())
        self.assertTrue((self.root/b['bundle_id']).exists())
        self.assertEqual(sentinel.read_text(),'preserve')
    def test_unlisted_expired_preserved(self):
        a=self.bundle();self.clean([])
        self.assertTrue((self.root/a['bundle_id']).exists())
    def test_approval_strict(self):
        a=self.bundle()
        for v in (False,1,'true',None):
            with self.assertRaises(RetentionHold):self.clean([a],deletion_authorized=v)
        self.assertTrue((self.root/a['bundle_id']).exists())
    def test_manifest_mismatch_holds(self):
        a=self.bundle();altered=dict(a,packet_sha256='3'*64)
        r=self.clean([altered])
        self.assertEqual(r['held'],1)
        self.assertTrue((self.root/a['bundle_id']).exists())
    def test_validate_entire_batch_before_mutation(self):
        a=self.bundle()
        for batch in ([a,{}],[a,a],[a]* (MAX_BATCH+1)):
            with self.assertRaises(RetentionHold):self.clean(batch)
        self.assertTrue((self.root/a['bundle_id']).exists())
    def test_corrupt_bundle_held(self):
        a=self.bundle();p=self.root/a['bundle_id']/'review.cms'
        p.write_bytes(b'corrupt')
        r=self.clean([a]);self.assertEqual(r['held'],1)
        self.assertEqual(p.read_bytes(),b'corrupt')
    def test_unexpected_file_preserved(self):
        a=self.bundle();p=self.root/a['bundle_id']/'unrelated'
        p.write_text('preserve')
        self.assertEqual(self.clean([a])['held'],1)
        self.assertEqual(p.read_text(),'preserve')
    def test_missing_never_certifies_deletion(self):
        a=self.bundle();self.clean([a])
        r=self.clean([a]);self.assertEqual(r['deleted'],0)
        self.assertEqual(r['results'][0]['status'],'missing_or_incomplete_unconfirmed')
    def test_symlink_not_followed(self):
        a=self.bundle();path=self.root/a['bundle_id'];moved=self.root/'target'
        path.rename(moved);path.symlink_to(moved,target_is_directory=True)
        self.assertEqual(self.clean([a])['held'],1)
        self.assertTrue((moved/'review.cms').exists())
    def test_future_manifest_rejected(self):
        a=self.bundle()
        with self.assertRaises(RetentionHold):self.clean([a],now=self.now-timedelta(seconds=1))
        self.assertTrue((self.root/a['bundle_id']).exists())
