"""Fixture-only review handoff. No IO destinations, keys, network or reviewer claims."""
from review_packet import preflight
from review_envelope import encrypt,decrypt,digest,require_pin

def seal_review(packet,certificate,cert_pin,receipt_pin):
    # A valid hash alone must never make a held or fabricated-release packet eligible.
    summary=preflight(packet,receipt_pin)
    sealed=encrypt(packet,certificate,cert_pin,receipt_pin)
    return sealed,{'packet_sha256':summary['packet_sha256'],
                   'envelope_sha256':digest(sealed),
                   'envelope_bytes':len(sealed),
                   'independent_review_completed':False,
                   'release_authorized':False,
                   'storage_authorized':False}

def open_review(sealed,certificate,cert_pin,private_key_path,receipt_pin,envelope_pin):
    # Both expected hashes must come from an independently trusted receipt.
    require_pin(digest(sealed),envelope_pin)
    packet=decrypt(sealed,certificate,cert_pin,private_key_path,receipt_pin)
    summary=preflight(packet,receipt_pin)
    # Returning bytes to a trusted local caller is not external transfer or publication.
    return packet,summary
