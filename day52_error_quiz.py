# Day 52 - Error Finding Quiz

from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str
    age: int
    grades: List[float] = field(default_factory=list)

    def average_grade(self):
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


@dataclass(order=True)
class Product:
    sort_index: float = field(init=False, repr=False)
    name: str
    price: float
    category: str = "General"

    def __post_init__(self):
        self.sort_index = self.price  # correct

    def apply_discount(self, percent):
        if percent <= 0 or percent >= 100:
            raise ValueError("Discount must be between 0 and 100.")
        self.price =- self.price * (percent / 100)  # Bug 1 - wrong operator


@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")


s1 = Student("Alice", 20)
s2 = Student("Alice", 20)
print(s1 == s2)    # Bug 2 - will be True (correct) but what if we add grades?

s1.grades.append(85.0)
print(s1 == s2)    # Now False - grades differ

coord = Coordinate(51.5, -0.1)
coord.latitude = 52.0  # Bug 3 - frozen dataclass raises FrozenInstanceError