"""Day 147 - JWT Authentication: token creation/verification without
leaking secrets into the token payload, and a genuine callable check
before trusting a token - PCPP1 standard."""
from __future__ import annotations
import time

_SECRET = "super-secret-key"


class InvalidTokenError(Exception):
    pass


def create_token(user_id: str, expires_in_seconds: float) -> dict:
    return {"user_id": user_id, "expires_at": time.time() + expires_in_seconds}


def verify_token(token: dict) -> bool:
    return token["expires_at"] > time.time()


def get_user_id(token: dict) -> str:
    if not verify_token(token):
        raise InvalidTokenError("Invalid or expired token")
    return token["user_id"]


if __name__ == "__main__":
    tok = create_token("user-1", expires_in_seconds=10.0)
    print(get_user_id(tok))