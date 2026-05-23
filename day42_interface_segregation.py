# Day 42 - Clean multiple interface implementation
# New concepts: multiple inheritance from ABC, interface segregation
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List


class Flyable(ABC):
    """Interface for flying creatures."""

    @abstractmethod
    def fly(self) -> str:
        """Return a description of the flying action."""
        pass


class Swimmable(ABC):
    """Interface for swimming creatures."""

    @abstractmethod
    def swim(self) -> str:
        """Return a description of the swimming action."""
        pass


class Walkable(ABC):
    """Interface for walking creatures."""

    @abstractmethod
    def walk(self) -> str:
        """Return a description of the walking action."""
        pass


class Duck(Flyable, Swimmable, Walkable):
    """A duck that can fly, swim and walk.

    Implements all three interfaces — demonstrates multiple inheritance.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    def fly(self) -> str:
        return f"{self._name} is flying."

    def swim(self) -> str:
        return f"{self._name} is swimming."

    def walk(self) -> str:
        return f"{self._name} is walking."

    def __str__(self) -> str:
        return f"Duck('{self._name}')"


class Fish(Swimmable):
    """A fish that can only swim."""

    def __init__(self, name: str) -> None:
        self._name = name

    def swim(self) -> str:
        return f"{self._name} is swimming."

    def __str__(self) -> str:
        return f"Fish('{self._name}')"


class Eagle(Flyable, Walkable):
    """An eagle that can fly and walk but not swim."""

    def __init__(self, name: str) -> None:
        self._name = name

    def fly(self) -> str:
        return f"{self._name} is soaring."

    def walk(self) -> str:
        return f"{self._name} is walking."

    def __str__(self) -> str:
        return f"Eagle('{self._name}')"


def demonstrate_abilities(creatures: List) -> None:
    """Demonstrate each creature's abilities based on interfaces."""
    for creature in creatures:
        print(f"  {creature}:")
        if isinstance(creature, Flyable):
            print(f"    {creature.fly()}")
        if isinstance(creature, Swimmable):
            print(f"    {creature.swim()}")
        if isinstance(creature, Walkable):
            print(f"    {creature.walk()}")


if __name__ == "__main__":
    duck = Duck("Donald")
    fish = Fish("Nemo")
    eagle = Eagle("Eddie")

    print("=== Creature abilities ===\n")
    demonstrate_abilities([duck, fish, eagle])

    print("\n=== isinstance checks ===\n")
    print(f"  Duck is Flyable   : {isinstance(duck, Flyable)}")
    print(f"  Duck is Swimmable : {isinstance(duck, Swimmable)}")
    print(f"  Duck is Walkable  : {isinstance(duck, Walkable)}")
    print(f"  Fish is Flyable   : {isinstance(fish, Flyable)}")
    print(f"  Eagle is Swimmable: {isinstance(eagle, Swimmable)}")