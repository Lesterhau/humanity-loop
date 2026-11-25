"""Integrated synthetic retention lifecycle, no live inference or external IO."""
import json
import tempfile
import unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch
from review_envelope import EnvelopeHold,digest,run
from review_packet import ReviewHold
from review_retention import RetentionHold,remove
from retained_review import retain_review,recover_review
from test_review_packet import packet

class RetainedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        root=Path(cls.tmp.name)
        cls.key=root/'key.pem'
        cert=root/'cert.pem'
        run(['req','-x509','-newkey','rsa:3072','-nodes','-keyout',str(cls.key),'-out',str(cert),'-days','1','-subj','/CN=synthetic-only'])
        cls.key.chmod(0o600)
        cls.cert=cert.read_bytes()
        cls.cpin=digest(run(['x509','-outform','DER'],cls.cert))
        cls.clear=json.dumps(packet()).encode()
        cls.ppin=digest(cls.clear)
    def setUp(self):
        self.tmp2=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp2.cleanup)
        self.root=Path(self.tmp2.name)
        self.now=datetime(2026,11,24,23,0,tzinfo=timezone.utc)
        self.bid='review-fixture-01'
    def retain(self,**kwargs):
        opts=dict(now=self.now,ttl_hours=24,storage_authorized=True)
        opts.update(kwargs)
        return retain_review(self.root,self.bid,self.clear,self.cert,self.cpin,self.ppin,**opts)
    def recover(self,m,**kwargs):
        return recover_review(self.root,self.bid,self.cert,self.cpin,self.key,self.ppin,m['envelope_sha256'],now=kwargs.get('now',self.now))
    def test_complete_lifecycle(self):
        m=self.retain()
        self.assertEqual(set(p.name for p in (self.root/self.bid).iterdir()),{'review.cms','manifest.json'})
        self.assertNotIn(self.clear,(self.root/self.bid/'review.cms').read_bytes())
        clear,s=self.recover(m)
        self.assertEqual(clear,self.clear)
        self.assertFalse(s['independent_review_completed'])
        self.assertFalse(s['release_authorized'])
        self.assertTrue(remove(self.root,self.bid,now=self.now+timedelta(hours=24))['deleted'])
        self.assertEqual(list(self.root.iterdir()),[])
    def test_approval_before_encryption(self):
        for v in (False,1,'true',None):
            with patch('retained_review.seal_review') as seal:
                with self.assertRaises(RetentionHold):self.retain(storage_authorized=v)
                seal.assert_not_called()
        self.assertEqual(list(self.root.iterdir()),[])
    def test_held_artifact_not_stored(self):
        r=packet();r['status']='held'
        b=json.dumps(r).encode()
        with self.assertRaises(ReviewHold):
            retain_review(self.root,self.bid,b,self.cert,self.cpin,digest(b),now=self.now,ttl_hours=1,storage_authorized=True)
        self.assertEqual(list(self.root.iterdir()),[])
    def test_expiry_prevents_decryption(self):
        m=self.retain()
        with patch('retained_review.open_review') as op:
            with self.assertRaisesRegex(RetentionHold,'expired'):
                self.recover(m,now=self.now+timedelta(hours=24))
            op.assert_not_called()
    def test_wrong_pin_prevents_decryption(self):
        m=self.retain();m['envelope_sha256']='0'*64
        with patch('retained_review.open_review') as op:
            with self.assertRaises(RetentionHold):self.recover(m)
            op.assert_not_called()
    def test_revocation_no_recovery(self):
        m=self.retain()
        self.assertEqual(remove(self.root,self.bid,now=self.now,revocation_authorized=True)['reason'],'revoked')
        with self.assertRaises(FileNotFoundError):self.recover(m)
    def test_no_overwrite(self):
        m=self.retain()
        with self.assertRaises(FileExistsError):self.retain()
        self.assertEqual(self.recover(m)[0],self.clear)
    def test_tamper_and_permissions(self):
        m=self.retain()
        p=self.root/self.bid/'review.cms'
        p.chmod(0o644)
        with self.assertRaises(RetentionHold):self.recover(m)
        p.chmod(0o600)
        p.write_bytes(p.read_bytes()+b'x')
        with self.assertRaises(RetentionHold):self.recover(m)
    def test_retention_bounds(self):
        for t in (0,73,True):
            with self.assertRaises(RetentionHold):self.retain(ttl_hours=t)
        self.assertEqual(list(self.root.iterdir()),[])
    def test_unexpired_delete_denied(self):
        m=self.retain()
        with self.assertRaises(RetentionHold):remove(self.root,self.bid,now=self.now)
        self.assertEqual(self.recover(m)[0],self.clear)
