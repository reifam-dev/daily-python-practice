# Day 52 - Clean @dataclass examples
# New concepts: @dataclass, field(), __post_init__, frozen=True, order=True
# PEP 8, docstrings, type hints, exceptions throughout

from dataclasses import dataclass, field
from typing import List, ClassVar


@dataclass
class Student:
    """A student with name, age and a list of grades.

    @dataclass auto-generates __init__, __repr__ and __eq__.
    The grades field uses field(default_factory=list) to avoid
    the mutable default argument trap.
    """

    name: str
    age: int
    grades: List[float] = field(default_factory=list)

    # ClassVar is not included as a dataclass field
    PASS_MARK: ClassVar[float] = 50.0

    def add_grade(self, grade: float) -> None:
        """Add a grade. Raises ValueError if out of range."""
        if not 0 <= grade <= 100:
            raise ValueError(f"Grade {grade} must be between 0 and 100.")
        self.grades.append(grade)

    def average_grade(self) -> float:
        """Return the average grade, or 0.0 if no grades recorded."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def is_passing(self) -> bool:
        """Return True if average grade is at or above the pass mark."""
        return self.average_grade() >= self.PASS_MARK


@dataclass(order=True)
class Product:
    """A product with ordering enabled via a sort_index field.

    order=True generates __lt__, __le__, __gt__, __ge__ from sort_index.
    __post_init__ sets sort_index after normal __init__ runs.
    """

    sort_index: float = field(init=False, repr=False)
    name: str
    price: float
    category: str = "General"

    def __post_init__(self) -> None:
        """Set sort_index to price after initialisation."""
        self.sort_index = self.price

    def apply_discount(self, percent: float) -> None:
        """Apply a percentage discount to the price."""
        if percent <= 0 or percent >= 100:
            raise ValueError("Discount must be between 0 and 100.")
        self.price -= self.price * (percent / 100)
        self.sort_index = self.price


@dataclass(frozen=True)
class Coordinate:
    """An immutable GPS coordinate.

    frozen=True makes all fields read-only after creation.
    Attempting to modify a field raises FrozenInstanceError.
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        """Validate coordinate ranges."""
        if not -90 <= self.latitude <= 90:
            raise ValueError(
                f"Latitude {self.latitude} must be between -90 and 90."
            )
        if not -180 <= self.longitude <= 180:
            raise ValueError(
                f"Longitude {self.longitude} must be between -180 and 180."
            )

    def distance_to(self, other: "Coordinate") -> float:
        """Return approximate distance in degrees to another coordinate."""
        return ((self.latitude - other.latitude) ** 2
                + (self.longitude - other.longitude) ** 2) ** 0.5


if __name__ == "__main__":
    print("=== Student @dataclass ===\n")
    s1 = Student("Alice", 20)
    s2 = Student("Alice", 20)

    print(f"  s1 == s2 (no grades) : {s1 == s2}")
    s1.add_grade(85.0)
    s1.add_grade(92.0)
    s1.add_grade(78.0)
    print(f"  s1 == s2 (with grades): {s1 == s2}")
    print(f"  s1 repr              : {s1}")
    print(f"  Average              : {s1.average_grade():.1f}")
    print(f"  Passing              : {s1.is_passing()}\n")

    print("=== Product @dataclass with order ===\n")
    products = [
        Product("Laptop", 999.99, "Electronics"),
        Product("Apple", 0.50, "Fruit"),
        Product("Book", 12.99, "Education"),
    ]
    products.sort()
    print("  Sorted by price:")
    for p in products:
        print(f"    {p}")

    products[0].apply_discount(10)
    print(f"\n  After 10% discount: {products[0]}\n")

    print("=== Frozen Coordinate @dataclass ===\n")
    try:
        london = Coordinate(51.5074, -0.1278)
        paris = Coordinate(48.8566, 2.3522)
        print(f"  London     : {london}")
        print(f"  Paris      : {paris}")
        print(f"  Distance   : {london.distance_to(paris):.4f}°")

        london.latitude = 52.0   # FrozenInstanceError
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")