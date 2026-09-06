"""Day 149 - Secrets Management: secrets loaded from environment
variables, never hardcoded or logged in plaintext - PCPP1 standard."""
from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("SERVICE_API_KEY")
if not _api_key:
    raise ValueError("SERVICE_API_KEY not set - check your .env file")


def connect_to_service() -> str:
    masked = _api_key[:4] + "..." + _api_key[-4:] if len(_api_key) > 8 else "****"
    return f"Connected using key: {masked}"


def log_connection_attempt(username: str) -> None:
    print(f"Login attempt: {username} (password redacted)")


if __name__ == "__main__":
    print(connect_to_service())
    log_connection_attempt("admin")