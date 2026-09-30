"""Day 173 - Webhook Signature Verification: uses hmac.new (a genuine
keyed HMAC), and compares signatures with hmac.compare_digest, which
runs in constant time - a plain == comparison leaks timing
information an attacker can exploit to guess the signature byte by
byte - PCPP1 standard."""
from __future__ import annotations
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

_WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "dev-secret-for-local-testing")


def compute_signature(payload: str) -> str:
    return hmac.new(
        _WEBHOOK_SECRET.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()


def verify_webhook(payload: str, received_signature: str) -> bool:
    expected_signature = compute_signature(payload)
    return hmac.compare_digest(expected_signature, received_signature)


if __name__ == "__main__":
    payload = '{"event": "deal_created", "deal_id": "deal-1"}'
    sig = compute_signature(payload)
    print(verify_webhook(payload, sig))
    print(verify_webhook(payload, "tampered-signature"))