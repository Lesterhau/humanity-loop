"""Offline provenance verification candidate, synthetic fixtures only.

Use GitHub CLI verification against independently approved immutable signer
and source pins. No signing, uploading, fetching roots, or approval action.
This does not attest model behavior, deletion, or independent human review.
The CLI, root and policy must be provisioned by a trusted reviewer.
"""
import hashlib
import hmac
import json
import re
from pathlib import Path
import subprocess
import tempfile
from review_retention import require,RetentionHold,pin

GH='/usr/bin/gh'
PREDICATE='https://slsa.dev/provenance/v1'
MAX_SUBJECT=270000
MAX_BUNDLE=2000000
MAX_ROOT=4000000
MAX_RESULT=4000000
REPO=re.compile(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+')
SHA=re.compile(r'[0-9a-f]{40}')
WORKFLOW=re.compile(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml')
KEYS={'repository','signer_workflow','source_commit','signer_commit','source_ref',
      'subject_sha256','trusted_root_sha256'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def validate_policy(policy):
    require(type(policy) is dict and set(policy)==KEYS,'invalid_provenance_policy')
    require(all(type(v) is str for v in policy.values()),'invalid_provenance_policy')
    require(REPO.fullmatch(policy['repository']) is not None
        and WORKFLOW.fullmatch(policy['signer_workflow']) is not None,'invalid_signer_identity')
    require(all(SHA.fullmatch(policy[k]) is not None for k in ('source_commit','signer_commit')),
            'immutable_commit_pins_required')
    require(re.fullmatch(r'refs/heads/[A-Za-z0-9_./-]+',policy['source_ref']) is not None,
            'exact_source_ref_required')
    require(all(pin(policy[k]) for k in ('subject_sha256','trusted_root_sha256')),
            'invalid_provenance_digest')

def checked_bytes(data,maximum,label):
    require(type(data) is bytes and 0<len(data)<=maximum,label)

def verify_synthetic(subject,bundle,trusted_root,policy,*,synthetic_fixture_authorized=False):
    """Return only metadata. Caller must be a trusted local fixture reviewer.

    The policy is an independent trust input, never derive it from the
    artifact, attestation predicate, or worker's claimed receipt.
    CLI uses local bundle/root. Run on a network-disabled reviewer host.
    No authorization is implied by a verified provenance claim.
    """
    require(synthetic_fixture_authorized is True,'synthetic_provenance_approval_missing')
    validate_policy(policy)
    checked_bytes(subject,MAX_SUBJECT,'invalid_subject_size')
    checked_bytes(bundle,MAX_BUNDLE,'invalid_bundle_size')
    checked_bytes(trusted_root,MAX_ROOT,'invalid_root_size')
    require(hmac.compare_digest(digest(subject),policy['subject_sha256']),'subject_digest_mismatch')
    require(hmac.compare_digest(digest(trusted_root),policy['trusted_root_sha256']),'trusted_root_digest_mismatch')
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp)
        for name,content in [('fixture.bin',subject),('bundle.jsonl',bundle),('root.jsonl',trusted_root)]:
            f=base/name;f.write_bytes(content);f.chmod(0o600)
        args=[GH,'attestation','verify',str(base/'fixture.bin'),
            '--repo',policy['repository'],'--bundle',str(base/'bundle.jsonl'),
            '--custom-trusted-root',str(base/'root.jsonl'),
            '--signer-workflow',policy['signer_workflow'],
            '--signer-digest',policy['signer_commit'],
            '--source-digest',policy['source_commit'],
            '--source-ref',policy['source_ref'],
            '--predicate-type',PREDICATE,
            '--cert-oidc-issuer','https://token.actions.githubusercontent.com',
            '--deny-self-hosted-runners','--format','json']
        try:
            result=subprocess.run(args,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,timeout=30,check=False,
                env={'PATH':'/usr/bin:/bin','HOME':tmp,'GH_CONFIG_DIR':tmp,'GH_PROMPT_DISABLED':'1',
                     'GH_NO_UPDATE_NOTIFIER':'1','GH_NO_EXTENSION_UPDATE_NOTIFIER':'1','LANG':'C'})
        except (OSError,subprocess.TimeoutExpired):
            raise RetentionHold('provenance_verifier_unavailable') from None
        require(result.returncode==0,'provenance_verification_failed')
        checked_bytes(result.stdout,MAX_RESULT,'invalid_verifier_result')
        try: verified=json.loads(result.stdout)
        except (ValueError,UnicodeError): raise RetentionHold('invalid_verifier_result') from None
        require(type(verified) is list and len(verified)>0 and all(
            type(x) is dict and type(x.get('verificationResult')) is dict for x in verified),
            'no_verified_attestation')
    return {'subject_sha256':policy['subject_sha256'],'verified_attestation_count':len(verified),
        'source_commit':policy['source_commit'],'signer_commit':policy['signer_commit'],
        'synthetic_fixture_only':True,'independent_review_completed':False,
        'deletion_independently_verified':False,'real_evidence_accepted':False,
        'release_authorized':False}
