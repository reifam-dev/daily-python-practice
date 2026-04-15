# Day 5 - Clean NumberStats class (PEP 8, docstrings, type hints, exceptions)

from typing import List

class NumberStats:
    """Simple class for basic statistics on a list of numbers."""

    def __init__(self, numbers: List[float]):
        if not numbers:
            raise ValueError("Numbers list cannot be empty")
        self._numbers = numbers

    def get_sum(self) -> float:
        """Return the sum of all numbers."""
        return sum(self._numbers)

    def get_average(self) -> float:
        """Return the average of the numbers."""
        return self.get_sum() / len(self._numbers)

    def get_max(self) -> float:
        """Return the maximum value."""
        return max(self._numbers)


if __name__ == "__main__":
    try:
        stats = NumberStats([10.5, 20.0, 30.5, 40.0])
        print(f"Sum     : {stats.get_sum()}")
        print(f"Average : {stats.get_average():.2f}")
        print(f"Max     : {stats.get_max()}")
    except ValueError as e:
        print(f"Error: {e}")