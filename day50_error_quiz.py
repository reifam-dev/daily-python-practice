# Day 50 - Error Finding Quiz

class PointWithSlots:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0   # Bug 1 - z not in __slots__, will raise AttributeError

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class PointWithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


class Colour:
    __slots__ = ('red', 'green', 'blue')

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def to_hex(self):
        return f"#{self.red:02x}{green:02x}{self.blue:02x}"  # Bug 2 - missing self

    def __repr__(self):
        return f"Colour({self.red}, {self.green}, {self.blue})"


p1 = PointWithSlots(3, 4)
p2 = PointWithoutSlots(3, 4)

print(hasattr(p2, '__dict__'))   # True  - has __dict__
print(hasattr(p1, '__dict__'))   # False - slots removes __dict__

p2.extra = "allowed"             # OK    - dynamic attribute
p1.extra = "not allowed"         # Bug 3 - AttributeError, extra not in __slots__