# Day 13 - Clean GradeCalculator class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class GradeCalculator:
    """Calculates basic statistics for a set of student grades."""

    PASS_MARK: int = 50

    def __init__(self, grades: List[float]) -> None:
        if not grades:
            raise ValueError("Grades list cannot be empty.")
        if any(g < 0 or g > 100 for g in grades):
            raise ValueError("All grades must be between 0 and 100.")
        self._grades = grades

    def get_average(self) -> float:
        """Return the average grade."""
        return sum(self._grades) / len(self._grades)

    def is_passing(self) -> bool:
        """Return True if average grade meets or exceeds the pass mark."""
        return self.get_average() >= self.PASS_MARK

    def get_highest(self) -> float:
        """Return the highest grade."""
        return max(self._grades)

    def get_lowest(self) -> float:
        """Return the lowest grade."""
        return min(self._grades)


if __name__ == "__main__":
    try:
        calc = GradeCalculator([45.0, 72.0, 88.0, 60.0, 55.0])
        print(f"Average : {calc.get_average():.1f}")
        print(f"Passing : {calc.is_passing()}")
        print(f"Highest : {calc.get_highest()}")
        print(f"Lowest  : {calc.get_lowest()}")
    except ValueError as e:
        print(f"Error: {e}")