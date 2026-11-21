"""Day 214 - PII and Secret Redaction for Logs and Prompts.

Anything that goes to a log (or to a model) is scrubbed first. Patterns
match a TOKEN, not the rest of the line (a greedy `.*` would also delete
the useful text after it), they ignore case (headers arrive as Bearer,
bearer or BEARER), and the function that logs writes the REDACTED text,
never the original. Pattern matching reduces leaks; it cannot catch
every format - PCPP1 standard.
"""
from __future__ import annotations

import re

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("api_key", re.compile(r"sk-[A-Za-z0-9_-]{8,}")),
    ("bearer", re.compile(r"bearer\s+[A-Za-z0-9._~+/-]+=*", re.IGNORECASE)),
    ("email", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("iban", re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")),
]


def redact(text: str) -> tuple[str, dict[str, int]]:
    """Return (redacted_text, how many of each kind were removed)."""
    counts: dict[str, int] = {}
    for label, pattern in _PATTERNS:
        text, found = pattern.subn(f"[{label.upper()} REDACTED]", text)
        if found:
            counts[label] = found
    return text, counts


def safe_log(message: str, sink: list[str]) -> None:
    """Append the REDACTED message to the sink."""
    redacted, _ = redact(message)
    sink.append(redacted)


if __name__ == "__main__":
    sink: list[str] = []
    safe_log("Authorization: Bearer abc.def.ghi; invoice total 8,500,000", sink)
    safe_log("retry with header bearer zzz.yyy.xxx", sink)
    safe_log("payer jane.doe@example.com paid GB29NWBK60161331926819 using key sk-live_ABCD1234efgh5678", sink)
    for line in sink:
        print(line)