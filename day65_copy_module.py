# Day 65 - Clean copy module — copy() vs deepcopy()
# New concepts: shallow copy, deep copy, copy module, shared references
# PEP 8, docstrings, type hints, exceptions throughout

import copy
from typing import List


class Address:
    """A mutable address object — used to demonstrate shared reference issues."""

    def __init__(self, street: str, city: str) -> None:
        self.street = street
        self.city = city

    def __repr__(self) -> str:
        return f"Address('{self.street}', '{self.city}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return NotImplemented
        return self.street == other.street and self.city == other.city


class Person:
    """A person with a mutable address and list of hobbies.

    Used to demonstrate the difference between shallow and deep copy:
    - Shallow copy: new Person object but SAME address and hobbies objects
    - Deep copy: new Person object with NEW copies of address and hobbies
    """

    def __init__(self, name: str, address: Address, hobbies: List[str]) -> None:
        self.name = name
        self.address = address
        self.hobbies = hobbies

    def __repr__(self) -> str:
        return (f"Person(name='{self.name}', "
                f"address={self.address}, "
                f"hobbies={self.hobbies})")

    def __copy__(self) -> "Person":
        """Custom __copy__ for shallow copy behaviour."""
        return Person(self.name, self.address, self.hobbies)

    def __deepcopy__(self, memo: dict) -> "Person":
        """Custom __deepcopy__ for deep copy behaviour."""
        return Person(
            copy.deepcopy(self.name, memo),
            copy.deepcopy(self.address, memo),
            copy.deepcopy(self.hobbies, memo)
        )


if __name__ == "__main__":
    original = Person(
        "Alice",
        Address("123 Main St", "London"),
        ["reading", "coding"]
    )

    print("=== Shallow copy ===\n")
    shallow = copy.copy(original)
    shallow.name = "Bob"
    shallow.hobbies.append("golf")
    shallow.address.city = "Manchester"

    print(f"  Original : {original}")
    print(f"  Shallow  : {shallow}")
    print(f"  Same address object  : {original.address is shallow.address}")
    print(f"  Same hobbies object  : {original.hobbies is shallow.hobbies}\n")

    original2 = Person(
        "Alice",
        Address("123 Main St", "London"),
        ["reading", "coding"]
    )

    print("=== Deep copy ===\n")
    deep = copy.deepcopy(original2)
    deep.name = "Charlie"
    deep.hobbies.append("tennis")
    deep.address.city = "Edinburgh"

    print(f"  Original : {original2}")
    print(f"  Deep     : {deep}")
    print(f"  Same address object  : {original2.address is deep.address}")
    print(f"  Same hobbies object  : {original2.hobbies is deep.hobbies}\n")

    print("=== Nested list — shallow vs deep ===\n")
    nested = [1, 2, [3, 4, 5]]
    shallow_list = copy.copy(nested)
    deep_list = copy.deepcopy(nested)

    shallow_list[2].append(6)
    deep_list[2].append(99)

    print(f"  Original     : {nested}")
    print(f"  Shallow copy : {shallow_list}")
    print(f"  Deep copy    : {deep_list}")
    print(f"  nested[2] affected by shallow: {nested[2]}\n")

    print("=== Assignment is NOT a copy ===\n")
    a = {"theme": "dark"}
    b = a           # assignment — same object
    c = copy.copy(a)
    b["theme"] = "light"
    print(f"  a (after b change) : {a}")
    print(f"  c (independent)    : {c}")