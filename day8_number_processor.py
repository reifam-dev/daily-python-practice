# Day 8 - Clean NumberProcessor class (PEP 8, docstrings, type hints, exceptions)

from typing import List

class NumberProcessor:
    """Processes basic statistics on a list of numbers."""

    def __init__(self, numbers: List[float]):
        if not numbers:
            raise ValueError("Numbers list cannot be empty")
        self._numbers = numbers

    def get_max(self) -> float:
        """Return the maximum value."""
        return max(self._numbers)

    def get_min(self) -> float:
        """Return the minimum value."""
        return min(self._numbers)

    def get_sum(self) -> float:
        """Return the sum of all numbers."""
        return sum(self._numbers)

    def get_average(self) -> float:
        """Return the average of the numbers."""
        return self.get_sum() / len(self._numbers)


if __name__ == "__main__":
    try:
        processor = NumberProcessor([10.5, 5.0, 8.5, 12.0, 3.5])
        print(f"Max     : {processor.get_max()}")
        print(f"Min     : {processor.get_min()}")
        print(f"Sum     : {processor.get_sum()}")
        print(f"Average : {processor.get_average():.2f}")
    except ValueError as e:
        print(f"Error: {e}")