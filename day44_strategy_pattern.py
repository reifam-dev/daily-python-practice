# Day 44 - Clean Strategy pattern
# New concepts: Strategy design pattern, runtime behaviour swapping
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List


class SortStrategy(ABC):
    """Abstract base class for all sorting strategies."""

    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data and return a new sorted list."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the strategy."""
        pass


class BubbleSort(SortStrategy):
    """Concrete strategy — sorts using the bubble sort algorithm."""

    @property
    def name(self) -> str:
        return "BubbleSort"

    def sort(self, data: List[int]) -> List[int]:
        """Return a new list sorted using bubble sort."""
        lst = data.copy()
        n = len(lst)
        for i in range(n):
            for j in range(n - i - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst


class SelectionSort(SortStrategy):
    """Concrete strategy — sorts using the selection sort algorithm."""

    @property
    def name(self) -> str:
        return "SelectionSort"

    def sort(self, data: List[int]) -> List[int]:
        """Return a new list sorted using selection sort."""
        lst = data.copy()
        n = len(lst)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lst[j] < lst[min_idx]:
                    min_idx = j
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
        return lst


class InsertionSort(SortStrategy):
    """Concrete strategy — sorts using the insertion sort algorithm."""

    @property
    def name(self) -> str:
        return "InsertionSort"

    def sort(self, data: List[int]) -> List[int]:
        """Return a new list sorted using insertion sort."""
        lst = data.copy()
        for i in range(1, len(lst)):
            key = lst[i]
            j = i - 1
            while j >= 0 and lst[j] > key:
                lst[j + 1] = lst[j]
                j -= 1
            lst[j + 1] = key
        return lst


class Sorter:
    """Context class that uses a SortStrategy to sort data.

    The strategy can be swapped at runtime without changing this class.
    Demonstrates dependency injection — strategy passed in via constructor.
    """

    def __init__(self, strategy: SortStrategy) -> None:
        if not isinstance(strategy, SortStrategy):
            raise TypeError("strategy must be an instance of SortStrategy.")
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        """Sort data using the current strategy."""
        return self._strategy.sort(data)

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Swap the strategy at runtime."""
        if not isinstance(strategy, SortStrategy):
            raise TypeError("strategy must be an instance of SortStrategy.")
        self._strategy = strategy

    def get_strategy_name(self) -> str:
        """Return the name of the current strategy."""
        return self._strategy.name


if __name__ == "__main__":
    data = [5, 3, 8, 1, 9, 2, 7, 4, 6]

    sorter = Sorter(BubbleSort())
    print(f"Strategy         : {sorter.get_strategy_name()}")
    print(f"Sorted           : {sorter.sort(data)}")

    sorter.set_strategy(SelectionSort())
    print(f"\nStrategy         : {sorter.get_strategy_name()}")
    print(f"Sorted           : {sorter.sort(data)}")

    sorter.set_strategy(InsertionSort())
    print(f"\nStrategy         : {sorter.get_strategy_name()}")
    print(f"Sorted           : {sorter.sort(data)}")

    print(f"\nOriginal unchanged: {data}")