"""Day 214 - PII and Secret Redaction for Logs: Error Quiz. Find and fix three bugs."""
import re

_PATTERNS = [
    ("api_key", re.compile(r"sk-[A-Za-z0-9_-]{8,}")),
    ("bearer", re.compile(r"Bearer .*")),
    ("email", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
]


def redact(text: str) -> str:
    for label, pattern in _PATTERNS:
        text = pattern.sub(f"[{label.upper()} REDACTED]", text)
    return text


def safe_log(message: str, sink: list) -> None:
    redacted = redact(message)
    sink.append(message)


if __name__ == "__main__":
    sink = []
    safe_log("Authorization: Bearer abc.def.ghi; invoice total 8,500,000", sink)
    safe_log("retry with header bearer zzz.yyy.xxx", sink)
    safe_log("payer jane.doe@example.com used key sk-live_ABCD1234efgh5678", sink)
    for line in sink:
        print(line)