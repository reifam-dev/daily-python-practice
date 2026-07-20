# Day 53 - Clean namedtuple and typing.NamedTuple examples
# New concepts: namedtuple, NamedTuple, immutability, tuple compatibility
# PEP 8, docstrings, type hints, exceptions throughout

from collections import namedtuple
from typing import NamedTuple
import math


# ── Basic namedtuple ──────────────────────────────────────────────────────────

Point = namedtuple('Point', ['x', 'y'])
Point.__doc__ = "A 2D point with x and y coordinates."

Colour = namedtuple('Colour', ['red', 'green', 'blue'])


# ── Typed NamedTuple (class-based, modern syntax) ─────────────────────────────

class Employee(NamedTuple):
    """An employee record — immutable, tuple-compatible, type-hinted."""

    name: str
    department: str
    salary: float = 30000.0

    def get_annual_bonus(self, percent: float) -> float:
        """Return the bonus amount based on percentage of salary."""
        if percent <= 0:
            raise ValueError("Bonus percentage must be positive.")
        return self.salary * (percent / 100)

    def with_raise(self, amount: float) -> "Employee":
        """Return a new Employee with an increased salary.

        NamedTuples are immutable — _replace() creates a new instance.
        """
        if amount <= 0:
            raise ValueError("Raise amount must be positive.")
        return self._replace(salary=self.salary + amount)

    def __str__(self) -> str:
        return (f"Employee(name='{self.name}', "
                f"dept='{self.department}', "
                f"salary=£{self.salary:.2f})")


class Coordinate(NamedTuple):
    """An immutable GPS coordinate with optional altitude."""

    latitude: float
    longitude: float
    altitude: float = 0.0

    def is_northern(self) -> bool:
        """Return True if the coordinate is in the northern hemisphere."""
        return self.latitude > 0

    def distance_to(self, other: "Coordinate") -> float:
        """Return approximate Euclidean distance in degrees."""
        return math.sqrt(
            (self.latitude - other.latitude) ** 2
            + (self.longitude - other.longitude) ** 2
        )

    def to_tuple(self) -> tuple:
        """Return as a plain tuple."""
        return (self.latitude, self.longitude, self.altitude)

    def __str__(self) -> str:
        return (f"Coordinate(lat={self.latitude}, "
                f"lon={self.longitude}, "
                f"alt={self.altitude})")


if __name__ == "__main__":
    print("=== Basic namedtuple ===\n")
    p1 = Point(3, 4)
    p2 = Point(3, 4)
    p3 = Point(6, 8)

    print(f"  p1           : {p1}")
    print(f"  p1.x, p1.y   : {p1.x}, {p1.y}")
    print(f"  p1[0], p1[1] : {p1[0]}, {p1[1]}")
    print(f"  p1 == p2     : {p1 == p2}")
    print(f"  p1 == p3     : {p1 == p3}")
    print(f"  isinstance tuple: {isinstance(p1, tuple)}")

    red = Colour(255, 0, 0)
    print(f"  Red colour   : {red}")
    print(f"  As tuple     : {tuple(red)}\n")

    print("=== Employee NamedTuple ===\n")
    emp = Employee("Alice", "Engineering", 45000.0)
    print(f"  {emp}")
    print(f"  Bonus (10%)  : £{emp.get_annual_bonus(10):.2f}")

    emp2 = emp.with_raise(5000)
    print(f"  After raise  : {emp2}")
    print(f"  Original     : {emp}")
    print(f"  emp == emp2  : {emp == emp2}\n")

    print("=== Coordinate NamedTuple ===\n")
    london = Coordinate(51.5074, -0.1278)
    paris = Coordinate(48.8566, 2.3522)
    underground = Coordinate(51.5, -0.1, -30.0)

    print(f"  {london}")
    print(f"  {paris}")
    print(f"  London is northern : {london.is_northern()}")
    print(f"  Distance           : {london.distance_to(paris):.4f}°")
    print(f"  As tuple           : {underground.to_tuple()}")

    print("\n=== Immutability check ===\n")
    try:
        emp.salary = 99999
    except AttributeError as e:
        print(f"  AttributeError: {e}")

    try:
        london.latitude = 90.0
    except AttributeError as e:
        print(f"  AttributeError: {e}")