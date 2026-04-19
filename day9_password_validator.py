# Day 9 - Clean PasswordValidator class (PEP 8, docstrings, type hints, exceptions)

from typing import List

class PasswordValidator:
    """Validates password strength according to basic security rules."""

    MIN_LENGTH: int = 8

    def __init__(self, password: str):
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        self._password = password.strip()

    def is_valid(self) -> bool:
        """Return True if password meets minimum security criteria."""
        if len(self._password) < self.MIN_LENGTH:
            return False
        if not any(char.isupper() for char in self._password):
            return False
        if not any(char.isdigit() for char in self._password):
            return False
        return True

    def get_issues(self) -> List[str]:
        """Return list of issues with the password."""
        issues = []
        if len(self._password) < self.MIN_LENGTH:
            issues.append("Password is too short")
        if not any(char.isupper() for char in self._password):
            issues.append("Missing uppercase letter")
        if not any(char.isdigit() for char in self._password):
            issues.append("Missing digit")
        return issues


if __name__ == "__main__":
    try:
        validator = PasswordValidator("Password123")
        print(f"Valid: {validator.is_valid()}")
        print(f"Issues: {validator.get_issues()}")
    except Exception as e:
        print(f"Error: {e}")