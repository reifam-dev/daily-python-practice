# Day 36 - Clean CountDown and NumberRange iterator classes
# New concepts: __iter__, __next__, iterator protocol, StopIteration
# PEP 8, docstrings, type hints, exceptions throughout

from __future__ import annotations


class CountDown:
    """An iterator that counts down from a given start value to zero.

    Implements the iterator protocol via __iter__ and __next__.
    Raises StopIteration when the count reaches below zero.
    """

    def __init__(self, start: int) -> None:
        if not isinstance(start, int) or start < 0:
            raise ValueError("Start must be a non-negative integer.")
        self._start: int = start
        self._current: int = start

    def __iter__(self) -> "CountDown":
        """Return self — this object is both iterable and iterator."""
        return self

    def __next__(self) -> int:
        """Return the next value in the countdown."""
        if self._current < 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value

    def reset(self) -> None:
        """Reset the countdown back to the start value."""
        self._current = self._start


class NumberRange:
    """An iterator that yields integers from start (inclusive) to stop (exclusive).

    Similar to the built-in range() but demonstrates the iterator protocol.
    """

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step <= 0:
            raise ValueError("Step must be a positive integer.")
        if start > stop:
            raise ValueError("Start must be less than or equal to stop.")
        self._start: int = start
        self._stop: int = stop
        self._step: int = step
        self._current: int = start

    def __iter__(self) -> "NumberRange":
        """Return self — this object is both iterable and iterator."""
        return self

    def __next__(self) -> int:
        """Return the next value in the range."""
        if self._current >= self._stop:
            raise StopIteration
        value = self._current
        self._current += self._step
        return value

    def reset(self) -> None:
        """Reset the range back to the start value."""
        self._current = self._start


if __name__ == "__main__":
    try:
        print("CountDown from 5:")
        cd = CountDown(5)
        for n in cd:
            print(f"  {n}")

        print("\nCountDown manually with next():")
        cd2 = CountDown(3)
        print(f"  {next(cd2)}")
        print(f"  {next(cd2)}")
        print(f"  {next(cd2)}")
        print(f"  {next(cd2)}")

        print("\nNumberRange 1 to 10 step 2:")
        nr = NumberRange(1, 10, 2)
        for n in nr:
            print(f"  {n}")

        print("\nAfter reset:")
        nr.reset()
        for n in nr:
            print(f"  {n}")

        print("\nUsing list() on iterator:")
        nr2 = NumberRange(1, 6)
        print(f"  {list(nr2)}")

    except (ValueError, StopIteration) as e:
        print(f"Error: {e}")