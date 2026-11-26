"""Trusted local caller only. No production destination or scheduler is configured."""
from review_handoff import seal_review,open_review
from review_retention import store,retrieve,require,RetentionHold

def retain_review(parent,bundle_id,packet,certificate,cert_pin,receipt_pin,*,now,ttl_hours,storage_authorized=False):
    require(storage_authorized is True,'storage_approval_missing')
    sealed,meta=seal_review(packet,certificate,cert_pin,receipt_pin)
    manifest=store(parent,bundle_id,sealed,envelope_sha256=meta['envelope_sha256'],
                   packet_sha256=receipt_pin,recipient_cert_sha256=cert_pin,
                   now=now,ttl_hours=ttl_hours,storage_authorized=True)
    return manifest

def recover_review(parent,bundle_id,certificate,cert_pin,private_key_path,receipt_pin,envelope_pin,*,now):
    sealed,manifest=retrieve(parent,bundle_id,now=now,expected_envelope_sha256=envelope_pin,
        expected_packet_sha256=receipt_pin,expected_recipient_cert_sha256=cert_pin)
    packet,summary=open_review(sealed,certificate,cert_pin,private_key_path,receipt_pin,envelope_pin)
    return packet,summary
