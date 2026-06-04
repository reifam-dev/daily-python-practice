# Day 55 - Error Finding Quiz

from typing import TypeVar, Generic, List, Protocol

T = TypeVar('T')

class Stack(Generic[T]):

    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty.")
        return self._items.pop   # Bug 1 - missing ()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty.")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(items) == 0   # Bug 2 - missing self

    def __len__(self) -> int:
        return len(self._items)


class Printable(Protocol):
    def display(self) -> str:
        ...


class Report:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def display(self) -> str:
        return f"Report: {self.title}\n{self.content}"


class Invoice:
    def __init__(self, number, amount):
        self.number = number
        self.amount = amount

    def display(self) -> str:
        return f"Invoice #{self.number}: £{self.amount:.2f}"


def print_document(doc: Printable) -> None:
    print(doc.display)           # Bug 3 - missing ()