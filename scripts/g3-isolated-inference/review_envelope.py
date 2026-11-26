"""Offline, fixture-sized CMS envelope candidate. No network or upload.
Recipient cert pin must be obtained via a trusted, independent channel.
A successful decryption is not proof of sender identity or human review.
"""
from __future__ import annotations
import hashlib
import hmac
import os
import re
import subprocess
import tempfile
from pathlib import Path

MAX_PACKET=250_000
MAX_ENVELOPE=270_000
MAX_CERT=32_768
OPENSSL='/usr/bin/openssl'

class EnvelopeHold(ValueError):
    pass

def bounded(data,limit):
    if type(data) is not bytes or not 0<len(data)<=limit:
        raise EnvelopeHold('invalid_size_or_type')
    return data

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require_pin(actual,expected):
    if not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}',expected) or not hmac.compare_digest(actual,expected):
        raise EnvelopeHold('digest_mismatch')

def run(args,data=None):
    try:
        r=subprocess.run([OPENSSL,*args],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15,check=False,env={'PATH':'/usr/bin:/bin','LANG':'C','OPENSSL_CONF':'/dev/null'})
    except (OSError,subprocess.TimeoutExpired):
        raise EnvelopeHold('crypto_unavailable') from None
    if r.returncode:
        raise EnvelopeHold('crypto_failed')
    return r.stdout

def check_cert(cert,expected):
    bounded(cert,MAX_CERT)
    if cert.count(b'-----BEGIN CERTIFICATE-----')!=1 or cert.count(b'-----END CERTIFICATE-----')!=1 or b'PRIVATE KEY' in cert:
        raise EnvelopeHold('single_public_cert_required')
    der=run(['x509','-inform','PEM','-outform','DER'],cert)
    require_pin(digest(der),expected)
    run(['x509','-checkend','0','-noout'],cert)
    pub=run(['x509','-pubkey','-noout'],cert)
    desc=run(['rsa','-pubin','-text','-noout'],pub)
    m=re.search(rb'Public-Key: \((\d+) bit\)',desc)
    if not m or int(m.group(1))<3072:
        raise EnvelopeHold('rsa_3072_required')
    return cert

def encrypt(packet,certificate,cert_pin,receipt_pin):
    bounded(packet,MAX_PACKET)
    require_pin(digest(packet),receipt_pin)
    cert=check_cert(certificate,cert_pin)
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'recipient.pem'
        p.write_bytes(cert)
        encrypted=run(['cms','-encrypt','-binary','-outform','DER','-aes-256-gcm','-recip',str(p),'-keyopt','rsa_padding_mode:oaep','-keyopt','rsa_oaep_md:sha256','-keyopt','rsa_mgf1_md:sha256'],packet)
    bounded(encrypted,MAX_ENVELOPE)
    return encrypted

def decrypt(envelope,certificate,cert_pin,private_key_path,receipt_pin):
    bounded(envelope,MAX_ENVELOPE)
    cert=check_cert(certificate,cert_pin)
    # A trusted reviewer-owned local key file only; no key bytes or passphrase in logs.
    key=Path(private_key_path)
    if not key.is_file() or key.is_symlink() or key.stat().st_mode & 0o077:
        raise EnvelopeHold('private_key_permissions')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'recipient.pem'
        p.write_bytes(cert)
        clear=run(['cms','-decrypt','-binary','-inform','DER','-recip',str(p),'-inkey',str(key.resolve()),'-passin','pass:'],envelope)
    bounded(clear,MAX_PACKET)
    require_pin(digest(clear),receipt_pin)
    return clear
