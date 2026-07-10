"""Day 91 - Advanced Typing: TypeVar, Generic, Protocol, ParamSpec.

A typed, generic repository for financial deal objects, demonstrating
structural typing (Protocol) and a signature-preserving decorator
(ParamSpec) - PCPP1 standard.
"""
from __future__ import annotations

import functools
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, ParamSpec, Protocol, TypeVar, runtime_checkable


@runtime_checkable
class Valuable(Protocol):
    """Structural contract for anything exposing a market value."""

    market_value: float


T = TypeVar("T", bound=Valuable)
P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class Deal:
    """An immutable real estate deal record."""

    name: str
    market_value: float


class DealRepository(Generic[T]):
    """A generic, type-safe container for Valuable items."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        """Add an item, validating it satisfies the Valuable protocol."""
        if not isinstance(item, Valuable):
            raise TypeError("item must satisfy the Valuable protocol")
        self._items.append(item)

    def total_value(self) -> float:
        """Return the summed market value of all items."""
        return sum(item.market_value for item in self._items)

    def top(self, n: int) -> list[T]:
        """Return the n highest-value items, descending."""
        return sorted(self._items, key=lambda i: i.market_value, reverse=True)[:n]


def logged(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs a call while preserving the wrapped signature."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@logged
def summarise_portfolio(repo: DealRepository[Deal]) -> float:
    """Return the total value of a deal repository."""
    return repo.total_value()


if __name__ == "__main__":
    repository: DealRepository[Deal] = DealRepository()
    repository.add(Deal("Riverside JV", 12_500_000.0))
    repository.add(Deal("Logistics Portfolio", 34_200_000.0))
    print(summarise_portfolio(repository))
    print(repository.top(1))