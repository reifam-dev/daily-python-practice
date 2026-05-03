# Day 23 - Clean ScoreTracker class (PEP 8, docstrings, type hints, exceptions)

from typing import List, Optional


class ScoreTracker:
    """Tracks a collection of scores with basic statistics."""

    def __init__(self) -> None:
        self._scores: List[float] = []

    def add_score(self, score: float) -> None:
        """Add a score. Raises ValueError if score is negative or above 100."""
        if score < 0 or score > 100:
            raise ValueError(f"Score must be between 0 and 100. Got {score}.")
        self._scores.append(score)

    def get_highest(self) -> Optional[float]:
        """Return the highest score, or None if no scores recorded."""
        if not self._scores:
            return None
        return max(self._scores)

    def get_lowest(self) -> Optional[float]:
        """Return the lowest score, or None if no scores recorded."""
        if not self._scores:
            return None
        return min(self._scores)

    def get_average(self) -> Optional[float]:
        """Return the average score, or None if no scores recorded."""
        if not self._scores:
            return None
        return sum(self._scores) / len(self._scores)

    def get_count(self) -> int:
        """Return the number of scores recorded."""
        return len(self._scores)

    def reset(self) -> None:
        """Clear all recorded scores."""
        self._scores = []


if __name__ == "__main__":
    try:
        tracker = ScoreTracker()
        tracker.add_score(85)
        tracker.add_score(92)
        tracker.add_score(78)
        tracker.add_score(95)
        tracker.add_score(60)

        print(f"Scores recorded  : {tracker.get_count()}")
        print(f"Highest          : {tracker.get_highest()}")
        print(f"Lowest           : {tracker.get_lowest()}")
        print(f"Average          : {tracker.get_average():.1f}")

        tracker.reset()
        print(f"After reset      : {tracker.get_count()} scores")
        print(f"Highest after reset: {tracker.get_highest()}")

    except ValueError as e:
        print(f"Error: {e}")