# Day 53 - Error Finding Quiz

from collections import namedtuple
from typing import NamedTuple

# Basic namedtuple
Point = namedtuple('Point', ['x', 'y'])

# Typed NamedTuple
class Employee(NamedTuple):
    name: str
    department: str
    salary: float = 30000.0

    def get_annual_bonus(self, percent):
        return self.salary * (percent / 100)


class Coordinate(NamedTuple):
    latitude: float
    longitude: float
    altitude: float = 0.0

    def is_northern(self):
        return latitude > 0   # Bug 1 - missing self

    def to_tuple(self):
        return (self.latitude, self.longitude, self.altitude)


p1 = Point(3, 4)
p2 = Point(3, 4)

print(p1 == p2)        # True - tuples compare by value
print(p1.x, p1.y)
print(p1[0], p1[1])    # Tuple access still works

emp = Employee("Alice", "Engineering", 45000.0)
print(emp.name)
print(emp.get_annual_bonus(10))

emp.salary = 50000.0   # Bug 2 - NamedTuple is immutable

coord = Coordinate(51.5, -0.1)
print(coord.is_northern())

p1.z = 5               # Bug 3 - namedtuple is immutable, z not a field