"""Mock CLI contract only; no real attestation or GitHub/OIDC call."""
import subprocess
import unittest
from unittest.mock import patch
from pathlib import Path
from review_retention import RetentionHold
import review_provenance as p

class ProvenanceContractTests(unittest.TestCase):
    def setUp(self):
        self.subject=b'synthetic fixture only'
        self.bundle=b'synthetic mock bundle'
        self.root=b'synthetic mock root'
        self.policy=dict(repository='Lesterhau/humanity-loop',
          signer_workflow='Lesterhau/humanity-loop/.github/workflows/synthetic.yml',
          source_commit='1'*40,signer_commit='2'*40,source_ref='refs/heads/reviewed-fixture',
          subject_sha256=p.digest(self.subject),trusted_root_sha256=p.digest(self.root))
    def verify(self,**kw):
        args=dict(synthetic_fixture_authorized=True);args.update(kw)
        return p.verify_synthetic(self.subject,self.bundle,self.root,self.policy,**args)
    def test_exact_pins_and_no_approval(self):
        def mock(args,**kwargs):
            for flag,val in [('--repo',self.policy['repository']),('--source-digest','1'*40),
                ('--signer-digest','2'*40),('--source-ref','refs/heads/reviewed-fixture'),
                ('--signer-workflow',self.policy['signer_workflow']),('--predicate-type',p.PREDICATE)]:
                self.assertEqual(args[args.index(flag)+1],val)
            self.assertIn('--deny-self-hosted-runners',args)
            self.assertEqual(Path(args[3]).read_bytes(),self.subject)
            self.assertEqual(Path(args[args.index('--bundle')+1]).read_bytes(),self.bundle)
            self.assertEqual(Path(args[args.index('--custom-trusted-root')+1]).read_bytes(),self.root)
            self.assertNotIn('GH_TOKEN',kwargs['env'])
            return subprocess.CompletedProcess(args,0,b'[{"verificationResult":{}}]',b'')
        with patch('review_provenance.subprocess.run',side_effect=mock):
            r=self.verify()
        self.assertEqual(r['verified_attestation_count'],1)
        self.assertFalse(r['release_authorized'])
        self.assertFalse(r['real_evidence_accepted'])
    def test_wrong_subject_and_root_stop_before_cli(self):
        with patch('review_provenance.subprocess.run') as cli:
            self.policy['subject_sha256']='0'*64
            with self.assertRaisesRegex(RetentionHold,'subject_digest_mismatch'):self.verify()
            self.policy['subject_sha256']=p.digest(self.subject)
            self.policy['trusted_root_sha256']='0'*64
            with self.assertRaisesRegex(RetentionHold,'trusted_root_digest_mismatch'):self.verify()
            cli.assert_not_called()
    def test_missing_approval_and_mutable_signer_rejected(self):
        with patch('review_provenance.subprocess.run') as cli:
            with self.assertRaisesRegex(RetentionHold,'approval_missing'):self.verify(synthetic_fixture_authorized=1)
            self.policy['signer_commit']='main'
            with self.assertRaisesRegex(RetentionHold,'immutable_commit_pins_required'):self.verify()
            cli.assert_not_called()
    def test_nonzero_exit_never_accepted(self):
        with patch('review_provenance.subprocess.run',return_value=subprocess.CompletedProcess([],1,b'[{"verificationResult":{}}]',b'')):
            with self.assertRaisesRegex(RetentionHold,'provenance_verification_failed'):self.verify()
    def test_empty_malformed_verification_result_rejected(self):
        for out in (b'[]',b'{}',b'not-json',b'[{}]'):
            with patch('review_provenance.subprocess.run',return_value=subprocess.CompletedProcess([],0,out,b'')):
                with self.assertRaises(RetentionHold):self.verify()
    def test_timeout_or_missing_cli(self):
        for exc in (OSError(),subprocess.TimeoutExpired([],30)):
            with patch('review_provenance.subprocess.run',side_effect=exc):
                with self.assertRaisesRegex(RetentionHold,'provenance_verifier_unavailable'):self.verify()
