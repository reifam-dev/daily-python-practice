"""Day 173 - Webhook Signature Verification: Error Quiz. Find and fix three bugs."""
import hashlib
import hmac

_WEBHOOK_SECRET = "shared-secret-key"


def compute_signature(payload: str) -> str:
    return hashlib.sha256((payload + _WEBHOOK_SECRET).encode()).hexdigest()


def verify_webhook(payload: str, received_signature: str) -> bool:
    expected_signature = compute_signature(payload)
    return expected_signature == received_signature


if __name__ == "__main__":
    payload = '{"event": "deal_created", "deal_id": "deal-1"}'
    sig = compute_signature(payload)
    print(verify_webhook(payload, sig))
    print(verify_webhook(payload, "tampered-signature"))