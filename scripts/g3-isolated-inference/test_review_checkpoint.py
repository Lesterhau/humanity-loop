"""Synthetic checkpoint probes. The test harness is the external anchor holder."""
import tempfile
import unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json
import review_journal as j
import review_checkpoint as c
from review_retention import RetentionHold
from test_review_journal import at
from review_envelope import digest,run
from test_review_packet import packet

class CheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys=tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.keys.cleanup)
        root=Path(cls.keys.name)
        cls.key=root/'key.pem'; cert=root/'cert.pem'
        run(['req','-x509','-newkey','rsa:3072','-nodes','-keyout',str(cls.key),'-out',str(cert),'-days','1','-subj','/CN=synthetic-checkpoint'])
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
        self.bid='review-checkpoint-01'
    def retain(self):
        return at(j.retain,self.root,self.bid,self.data,self.cert,self.cpin,self.ppin,
                  now=self.now,ttl_hours=1,storage_authorized=True)
    def anchor(self):
        return c.checkpoint(self.root)['checkpoint']
    def mutate(self,sql,args=()):
        with j.journal(self.root) as (db,fd):
            with db: db.execute(sql,args)
    def test_prefix_and_unanchored_tail(self):
        self.retain()
        a=self.anchor()
        self.assertEqual(a['sequence'],2)
        self.assertTrue(c.checkpoint(self.root,expected=a)['matches_supplied_checkpoint'])
        at(j.cleanup,self.root,[self.bid],now=self.expiry,deletion_authorized=True)
        r=c.checkpoint(self.root,expected=a)
        self.assertEqual(r['unanchored_events'],2)
        self.assertFalse(r['deletion_independently_verified'])
        self.assertFalse(r['release_authorized'])
    def test_unanchored_not_independent(self):
        self.retain()
        r=c.checkpoint(self.root)
        self.assertFalse(r['matches_supplied_checkpoint'])
        self.assertEqual(r['unanchored_events'],2)
    def test_edited_manifest_rejected_against_anchor(self):
        m=self.retain();a=self.anchor()
        m['envelope_sha256']='1'*64
        self.mutate('UPDATE bundles SET manifest=?',(json.dumps(m),))
        with self.assertRaisesRegex(RetentionHold,'external_checkpoint_mismatch'):
            c.checkpoint(self.root,expected=a)
    def test_state_rewrite_detected(self):
        self.retain();a=self.anchor()
        self.mutate("UPDATE bundles SET state='deleted'")
        with self.assertRaisesRegex(RetentionHold,'checkpoint_materialized_state_mismatch'):
            c.checkpoint(self.root,expected=a)
    def test_truncated_history_rejected(self):
        self.retain();a=self.anchor()
        self.mutate("DELETE FROM transitions WHERE seq=2")
        self.mutate("UPDATE bundles SET state='storing'")
        with self.assertRaisesRegex(RetentionHold,'external_checkpoint_truncated'):
            c.checkpoint(self.root,expected=a)
    def test_coherent_history_edit_rejected_against_anchor(self):
        self.retain()
        at(j.cleanup,self.root,[self.bid],now=self.expiry,deletion_authorized=True)
        a=self.anchor()
        self.mutate("UPDATE transitions SET reason='interrupted_storage_verified' WHERE seq=2")
        with self.assertRaisesRegex(RetentionHold,'external_checkpoint_mismatch'):
            c.checkpoint(self.root,expected=a)
    def test_invalid_transition_rejected_without_anchor(self):
        self.retain()
        self.mutate("UPDATE transitions SET state='deleted',reason='deletion_receipt_verified' WHERE seq=2")
        self.mutate("UPDATE bundles SET state='deleted'")
        with self.assertRaisesRegex(RetentionHold,'checkpoint_transition_invalid'):
            c.checkpoint(self.root)
    def test_invalid_anchor(self):
        self.retain();a=self.anchor()
        for bad in (dict(a,sequence=True),dict(a,head='invalid'),dict(a,version=True),dict(a,sequence=0)):
            with self.assertRaisesRegex(RetentionHold,'invalid_external_checkpoint'):
                c.checkpoint(self.root,expected=bad)
