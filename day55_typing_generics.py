# Day 55 - Clean typing module with TypeVar, Generic and Protocol
# New concepts: TypeVar, Generic[T], Protocol, structural typing
# PEP 8, docstrings, type hints, exceptions throughout

from __future__ import annotations
from typing import TypeVar, Generic, List, Protocol, Optional

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class Stack(Generic[T]):
    """A generic LIFO stack that works with any type T.

    Usage:
        stack: Stack[int] = Stack()
        stack.push(1)
        value: int = stack.pop()
    """

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """Push an item onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item. Raises IndexError if empty."""
        if not self._items:
            raise IndexError("Stack is empty.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it. Raises IndexError if empty."""
        if not self._items:
            raise IndexError("Stack is empty.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no items."""
        return len(self._items) == 0

    def __len__(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"


class KeyValueStore(Generic[K, V]):
    """A generic key-value store parameterised by key type K and value type V."""

    def __init__(self) -> None:
        self._store: dict = {}

    def put(self, key: K, value: V) -> None:
        """Store a key-value pair."""
        self._store[key] = value

    def get(self, key: K) -> Optional[V]:
        """Return the value for the key, or None if not found."""
        return self._store.get(key)

    def contains(self, key: K) -> bool:
        """Return True if the key exists."""
        return key in self._store

    def __len__(self) -> int:
        return len(self._store)

    def __repr__(self) -> str:
        return f"KeyValueStore({self._store})"


class Printable(Protocol):
    """Protocol defining the interface for printable documents.

    Any class with a display() -> str method satisfies this Protocol
    regardless of inheritance — structural typing.
    """

    def display(self) -> str:
        """Return a string representation of the document."""
        ...


class Report:
    """A report document — satisfies Printable Protocol."""

    def __init__(self, title: str, content: str) -> None:
        self._title = title
        self._content = content

    def display(self) -> str:
        return f"Report: {self._title}\n{self._content}"

    def __repr__(self) -> str:
        return f"Report('{self._title}')"


class Invoice:
    """An invoice document — satisfies Printable Protocol."""

    def __init__(self, number: int, amount: float) -> None:
        self._number = number
        self._amount = amount

    def display(self) -> str:
        return f"Invoice #{self._number}: £{self._amount:.2f}"

    def __repr__(self) -> str:
        return f"Invoice(#{self._number})"


def print_document(doc: Printable) -> None:
    """Print any object that satisfies the Printable Protocol."""
    print(f"  {doc.display()}")


def print_all(documents: List[Printable]) -> None:
    """Print all documents in a list."""
    for doc in documents:
        print_document(doc)


if __name__ == "__main__":
    print("=== Generic Stack[int] ===\n")
    int_stack: Stack[int] = Stack()
    int_stack.push(10)
    int_stack.push(20)
    int_stack.push(30)
    print(f"  Stack     : {int_stack}")
    print(f"  Length    : {len(int_stack)}")
    print(f"  Peek      : {int_stack.peek()}")
    print(f"  Pop       : {int_stack.pop()}")
    print(f"  After pop : {int_stack}\n")

    print("=== Generic Stack[str] ===\n")
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"  Stack : {str_stack}")
    print(f"  Pop   : {str_stack.pop()}\n")

    print("=== Generic KeyValueStore[str, int] ===\n")
    store: KeyValueStore[str, int] = KeyValueStore()
    store.put("apples", 5)
    store.put("bananas", 3)
    print(f"  Store    : {store}")
    print(f"  apples   : {store.get('apples')}")
    print(f"  contains : {store.contains('bananas')}\n")

    print("=== Protocol — structural typing ===\n")
    documents: List[Printable] = [
        Report("Q1 Results", "Revenue up 12% YoY."),
        Invoice(1042, 450.00),
        Report("Risk Assessment", "Low risk profile confirmed."),
    ]
    print_all(documents)

    print("\n=== Stack empty guard ===\n")
    try:
        empty: Stack[int] = Stack()
        empty.pop()
    except IndexError as e:
        print(f"  IndexError: {e}")