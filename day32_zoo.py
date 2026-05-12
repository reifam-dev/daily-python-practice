# Day 32 - Clean Animal and Zoo classes
# New concepts: __repr__, @staticmethod
# PEP 8, docstrings, type hints, exceptions throughout

from typing import List


class Animal:
    """Represents an animal with a name, species and age."""

    def __init__(self, name: str, species: str, age: int) -> None:
        if not name or not name.strip():
            raise ValueError("Animal name cannot be empty.")
        if age < 0:
            raise ValueError("Age cannot be negative.")
        self._name: str = name.strip()
        self._species: str = species.strip()
        self._age: int = age

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self._name} ({self._species}), age {self._age}"

    def __repr__(self) -> str:
        """Return a developer-facing string representation."""
        return f"Animal(name='{self._name}', species='{self._species}', age={self._age})"

    @property
    def name(self) -> str:
        """Return the animal name."""
        return self._name

    @property
    def species(self) -> str:
        """Return the animal species."""
        return self._species

    @property
    def age(self) -> int:
        """Return the animal age."""
        return self._age

    @staticmethod
    def is_adult(age: int) -> bool:
        """Return True if the age qualifies as an adult (over 3 years)."""
        return age > 3

    def have_birthday(self) -> None:
        """Increment the animal's age by one year."""
        self._age += 1


class Zoo:
    """Manages a collection of Animal objects. Demonstrates composition."""

    def __init__(self, zoo_name: str) -> None:
        self._zoo_name: str = zoo_name
        self._animals: List[Animal] = []

    def add_animal(self, animal: Animal) -> None:
        """Add an animal to the zoo."""
        self._animals.append(animal)

    def remove_animal(self, name: str) -> None:
        """Remove an animal by name. Raises KeyError if not found."""
        for animal in self._animals:
            if animal.name == name:
                self._animals.remove(animal)
                return
        raise KeyError(f"'{name}' not found in the zoo.")

    def get_adults(self) -> List[Animal]:
        """Return a list of all adult animals."""
        return [a for a in self._animals if Animal.is_adult(a.age)]

    def get_count(self) -> int:
        """Return the total number of animals."""
        return len(self._animals)

    def get_zoo_name(self) -> str:
        """Return the zoo name."""
        return self._zoo_name


if __name__ == "__main__":
    try:
        zoo = Zoo("Royal Python Zoo")

        zoo.add_animal(Animal("Leo", "Lion", 5))
        zoo.add_animal(Animal("Nemo", "Clownfish", 1))
        zoo.add_animal(Animal("Ellie", "Elephant", 8))
        zoo.add_animal(Animal("Pip", "Penguin", 2))

        print(f"Zoo              : {zoo.get_zoo_name()}")
        print(f"Total animals    : {zoo.get_count()}")

        print("\nAll animals (str):")
        for animal in zoo._animals:
            print(f"  {animal}")

        print("\nAll animals (repr):")
        for animal in zoo._animals:
            print(f"  {repr(animal)}")

        print(f"\nAdult animals    : {[str(a) for a in zoo.get_adults()]}")

        zoo._animals[1].have_birthday()
        print(f"\nNemo after birthday: {zoo._animals[1]}")

        zoo.remove_animal("Pip")
        print(f"After removing Pip: {zoo.get_count()} animals")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")