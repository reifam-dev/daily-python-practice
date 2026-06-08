# Day 59 - Clean re module examples
# New concepts: re.match, re.search, re.findall, re.sub, re.compile, groups
# PEP 8, docstrings, type hints, exceptions throughout

import re
from typing import List, Optional, Tuple


# Compiled patterns — compile once, use many times
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)
PHONE_PATTERN = re.compile(
    r"\+\d{1,3}\s\d{3,4}\s\d{6}"
)
DATE_PATTERN = re.compile(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
)
POSTCODE_PATTERN = re.compile(
    r"^[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}$"
)


def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from text."""
    return EMAIL_PATTERN.findall(text)


def extract_phones(text: str) -> List[str]:
    """Extract all phone numbers from text."""
    return PHONE_PATTERN.findall(text)


def parse_date(text: str) -> Optional[Tuple[str, str, str]]:
    """Extract year, month, day from text containing a date.

    Returns a tuple of (year, month, day) or None if no date found.
    Uses named groups for clarity.
    """
    match = DATE_PATTERN.search(text)
    if match:
        return match.group("year"), match.group("month"), match.group("day")
    return None


def clean_whitespace(text: str) -> str:
    """Replace multiple whitespace characters with a single space."""
    return re.sub(r"\s+", " ", text).strip()


def is_valid_postcode(postcode: str) -> bool:
    """Return True if the postcode matches UK format."""
    return bool(POSTCODE_PATTERN.match(postcode.upper()))


if __name__ == "__main__":
    print("=== Email extraction ===\n")
    text = "Contact alice@example.com or bob@company.co.uk for info."
    emails = extract_emails(text)
    print(f"  Found {len(emails)} email(s): {emails}\n")

    print("=== Phone extraction ===\n")
    text2 = "Call +44 7700 900123 or +1 555 123456 for support."
    phones = extract_phones(text2)
    print(f"  Found {len(phones)} phone(s): {phones}\n")

    print("=== match vs search ===\n")
    sample = "Today is 2026-06-08 and tomorrow is 2026-06-09"
    print(f"  re.match  (from start) : {re.match(DATE_PATTERN, sample)}")
    print(f"  re.search (anywhere)   : {re.search(DATE_PATTERN, sample)}\n")

    print("=== Named groups — date parsing ===\n")
    result = parse_date("Meeting on 2026-06-08 confirmed.")
    if result:
        year, month, day = result
        print(f"  Year: {year}, Month: {month}, Day: {day}\n")

    print("=== re.sub — clean whitespace ===\n")
    messy = "too   many    spaces   here"
    print(f"  Before : '{messy}'")
    print(f"  After  : '{clean_whitespace(messy)}'\n")

    print("=== UK postcode validation ===\n")
    postcodes = ["SW1A 1AA", "EC1A 1BB", "w1a 1hq", "12345", "HA9 0WS"]
    for pc in postcodes:
        print(f"  {pc:<12} → {'✓' if is_valid_postcode(pc) else '✗'}")

    print("\n=== re.findall with groups ===\n")
    text3 = "Dates: 2026-06-05, 2026-06-06, 2026-06-07"
    all_dates = re.findall(
        r"(\d{4})-(\d{2})-(\d{2})", text3
    )
    print(f"  All dates: {all_dates}")