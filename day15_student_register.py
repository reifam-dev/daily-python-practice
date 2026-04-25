# Day 15 - Clean StudentRegister class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class StudentRegister:
    """Manages a register of enrolled students."""

    def __init__(self) -> None:
        self._students: List[str] = []

    def add_student(self, name: str) -> None:
        """Add a student to the register. Raises ValueError if already enrolled."""
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty.")
        if name.strip() in self._students:
            raise ValueError(f"'{name}' is already enrolled.")
        self._students.append(name.strip())

    def remove_student(self, name: str) -> None:
        """Remove a student from the register. Raises KeyError if not found."""
        if name not in self._students:
            raise KeyError(f"'{name}' is not enrolled.")
        self._students.remove(name)

    def is_enrolled(self, name: str) -> bool:
        """Return True if the student is enrolled."""
        return name in self._students

    def get_all_students(self) -> List[str]:
        """Return a copy of the full student list."""
        return self._students.copy()

    def get_count(self) -> int:
        """Return the total number of enrolled students."""
        return len(self._students)


if __name__ == "__main__":
    try:
        register = StudentRegister()
        register.add_student("Alice")
        register.add_student("Bob")
        register.add_student("Charlie")

        print(f"Enrolled    : {register.get_all_students()}")
        print(f"Total       : {register.get_count()}")
        print(f"Alice enrolled: {register.is_enrolled('Alice')}")

        register.remove_student("Bob")
        print(f"After removing Bob: {register.get_all_students()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")