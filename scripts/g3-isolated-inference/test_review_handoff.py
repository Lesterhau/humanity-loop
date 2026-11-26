"""Synthetic keys and model text only; no live model or storage destination."""
import json
import tempfile
import unittest
import subprocess
import sys
from seal_receipt import seal_file
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

class ProducerHandoffTests(ReviewHandoffTests):
    def test_actual_sealing_cli_survives_producer_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            out=root/'handoff';out.mkdir(mode=0o700)
            script=Path(__file__).with_name('seal_receipt.py')
            with tempfile.TemporaryDirectory(dir=root) as producer:
                raw=Path(producer)/'receipt.json';raw.write_bytes(self.clear)
                args=[sys.executable,str(script)]
                pre=subprocess.run(args+['preflight',str(self.root/'a.pem'),self.cert_pin,str(out)],capture_output=True,check=True)
                self.assertIn(b'REVIEW_DESTINATION_PREFLIGHT_PASSED',pre.stdout)
                res=subprocess.run(args+['seal',str(raw),str(self.root/'a.pem'),self.cert_pin,str(out)],capture_output=True,check=True)
                self.assertNotIn(b'Synthetic test text',res.stdout+res.stderr)
            self.assertFalse(raw.exists())
            self.assertEqual({p.name for p in out.iterdir()},{'review.cms','manifest.json'})
            m=json.loads((out/'manifest.json').read_bytes())
            clear,summary=self.open((out/'review.cms').read_bytes(),m)
            self.assertEqual(clear,self.clear)
            self.assertFalse(summary['independent_review_completed'])
            self.assertFalse(m['storage_authorized'])
            self.assertFalse(m['release_authorized'])
            self.assertNotIn(b'Synthetic test text',(out/'review.cms').read_bytes())
            self.assertEqual((out/'review.cms').stat().st_mode & 0o777,0o600)
            print('G3_SYNTHETIC_PRODUCER_SEAL_SURVIVES_CLEANUP_PASSED')
    def test_failed_preflight_or_packet_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);out=root/'handoff';out.mkdir(mode=0o700)
            raw=root/'receipt.json';raw.write_bytes(b'{}')
            with self.assertRaises(EnvelopeHold):
                seal_file(raw,self.root/'a.pem','0'*64,out)
            self.assertEqual(list(out.iterdir()),[])
            with self.assertRaises(ReviewHold):
                seal_file(raw,self.root/'a.pem',self.cert_pin,out)
            self.assertEqual(list(out.iterdir()),[])
