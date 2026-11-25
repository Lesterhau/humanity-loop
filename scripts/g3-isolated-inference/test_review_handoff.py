"""Synthetic keys and model text only; no live model or storage destination."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from review_envelope import EnvelopeHold,digest,run,encrypt
from review_packet import ReviewHold
from review_handoff import seal_review,open_review
from test_review_packet import packet

class ReviewHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root=Path(cls.tmp.name)
        for name in ('a','b'):
            key=cls.root/(name+'.key')
            cert=cls.root/(name+'.pem')
            run(['req','-x509','-newkey','rsa:3072','-nodes','-keyout',str(key),'-out',str(cert),'-days','1','-subj','/CN=synthetic-test-only'])
            key.chmod(0o600)
        cls.cert=(cls.root/'a.pem').read_bytes()
        cls.cert_pin=digest(run(['x509','-outform','DER'],cls.cert))
        cls.clear=json.dumps(packet()).encode()
        cls.receipt_pin=digest(cls.clear)

    def seal(self):
        return seal_review(self.clear,self.cert,self.cert_pin,self.receipt_pin)

    def open(self,e,meta,**kwargs):
        return open_review(e,self.cert,self.cert_pin,kwargs.get('key',self.root/'a.key'),kwargs.get('receipt',self.receipt_pin),kwargs.get('envelope',meta['envelope_sha256']))

    def test_round_trip_no_automatic_approval(self):
        e,m=self.seal()
        clear,s=self.open(e,m)
        self.assertEqual(clear,self.clear)
        self.assertEqual(s['review_status'],'pending_separate_human')
        self.assertFalse(m['storage_authorized'])
        self.assertFalse(s['release_authorized'])
        self.assertFalse(s['independent_review_completed'])
        self.assertNotIn(b'Synthetic test text',e)
        self.assertNotIn('Synthetic test text',json.dumps(m))

    def test_held_packet_never_encrypted(self):
        r=packet();r['status']='held';data=json.dumps(r).encode()
        with patch('review_handoff.encrypt') as enc:
            with self.assertRaises(ReviewHold):seal_review(data,self.cert,self.cert_pin,digest(data))
            enc.assert_not_called()

    def test_plaintext_validation_repeated_after_decryption(self):
        r=packet();r['independent_review_completed']=True;data=json.dumps(r).encode()
        e=encrypt(data,self.cert,self.cert_pin,digest(data))
        with self.assertRaises(ReviewHold):
            open_review(e,self.cert,self.cert_pin,self.root/'a.key',digest(data),digest(e))

    def test_wrong_envelope_digest_stops_before_decrypt(self):
        e,m=self.seal()
        with patch('review_handoff.decrypt') as dec:
            with self.assertRaises(EnvelopeHold):self.open(e,m,envelope='0'*64)
            dec.assert_not_called()

    def test_wrong_recipient(self):
        e,m=self.seal()
        with self.assertRaises(EnvelopeHold):self.open(e,m,key=self.root/'b.key')

    def test_wrong_plaintext_receipt(self):
        e,m=self.seal()
        with self.assertRaises(EnvelopeHold):self.open(e,m,receipt='0'*64)

    def test_modified_ciphertext_even_with_recomputed_digest(self):
        e,m=self.seal();bad=bytearray(e);bad[-5]^=1;bad=bytes(bad)
        with self.assertRaises(EnvelopeHold):self.open(bad,m,envelope=digest(bad))

    def test_invalid_certificate_pin(self):
        with self.assertRaises(EnvelopeHold):seal_review(self.clear,self.cert,'0'*64,self.receipt_pin)

    def test_no_private_key_permissions_override(self):
        e,m=self.seal();k=self.root/'a.key';k.chmod(0o644)
        try:
            with self.assertRaises(EnvelopeHold):self.open(e,m)
        finally:k.chmod(0o600)
