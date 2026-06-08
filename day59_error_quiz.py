# Day 59 - Error Finding Quiz

import re

# Basic match
text = "Hello, my email is alice@example.com and phone is +44 7700 900123"

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = re.findall(email_pattern, text)
print(emails)

phone_pattern = r"\+\d{2}\s\d{4}\s\d{6}"
phones = re.findall(phone_pattern, text)
print(phones)

# match vs search
result1 = re.match(r"Hello", text)     # correct - matches at start
result2 = re.match(r"email", text)     # Bug 1 - match only checks start of string, use search
print(result1)
print(result2)

# sub
cleaned = re.sub(r"\s+", " ", "too   many    spaces")
print(cleaned)

# groups
date_pattern = r"(\d{4})-(\d{2})-(\d{2})"
date_text = "Date: 2026-06-08"
match = re.search(date_pattern, date_text)
if match:
    print(match.group(0))   # full match
    print(match.group(1))   # year
    print(match.group(4))   # Bug 2 - only 3 groups, index 4 raises IndexError

# compile
validator = re.compile(r"^[A-Z]{2}\d{2}\s\d{4}$")
print(validator.match("AB12 3456"))    # correct
print(validator.match("ab12 3456"))    # Bug 3 - lowercase, should not match but
                                       # result is None which is correct — not a bug
                                       # Real bug: what about validator.match("AB123456")?
print(bool(validator.match("AB123456")))  # Bug 3 - missing space, returns None