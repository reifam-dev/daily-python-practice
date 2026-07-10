"""Day 91 - Advanced Typing: Error Quiz.

Find and fix three bugs. No location hints.
"""
from dataclasses import dataclass
from typing import Generic, ParamSpec, Protocol, TypeVar
from collections.abc import Callable
import functools


class Valuable(Protocol):
    """Structural type for anything with a market value."""
    market_value: float


T = TypeVar("T", bound=Valuable)
P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class Deal:
    name: str
    market_value: float


class DealRepository(Generic[T]):
    """Typed container for deal-like objects."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        if not isinstance(item, Valuable):
            raise TypeError("item must satisfy the Valuable protocol")
        self._items.append(item)

    def total_value(self) -> float:
        return sum(item.market_value for item in self._items)

    def top(self, n: int) -> list[T]:
        return sorted(self._items, key=lambda i: i.market_value, reverse=False)[:n]


def logged(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs calls while preserving the wrapped signature."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        func(*args, **kwargs)
    return wrapper


@logged
def value_summary(repo: DealRepository[Deal]) -> float:
    return repo.total_value()


if __name__ == "__main__":
    repository: DealRepository[Deal] = DealRepository()
    repository.add(Deal("Riverside JV", 12_500_000.0))
    repository.add(Deal("Logistics Portfolio", 34_200_000.0))
    print(value_summary(repository))