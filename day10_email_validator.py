# Day 10 - Clean EmailValidator class (PEP 8, docstrings, type hints, exceptions)

from typing import List

class EmailValidator:
    """Simple email format validator."""

    def __init__(self, email: str):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        self._email = email.strip().lower()

    def is_valid(self) -> bool:
        """Return True if email has basic valid format (@ and .)."""
        if not self._email or "@" not in self._email:
            return False
        if "." not in self._email:
            return False
        return True

    def get_issues(self) -> List[str]:
        """Return list of issues found."""
        issues = []
        if "@" not in self._email:
            issues.append("Missing '@' symbol")
        if "." not in self._email:
            issues.append("Missing '.' symbol")
        return issues


if __name__ == "__main__":
    try:
        validator = EmailValidator("test@example.com")
        print(f"Valid: {validator.is_valid()}")
        print(f"Issues: {validator.get_issues()}")
    except Exception as e:
        print(f"Error: {e}")