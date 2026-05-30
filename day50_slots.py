# Day 50 - Clean __slots__ demonstration
# New concepts: __slots__, memory optimisation, attribute restriction
# PEP 8, docstrings, type hints, exceptions throughout

import sys
from typing import Tuple


class PointWithSlots:
    """A 2D point using __slots__ for memory efficiency.

    __slots__ replaces __dict__ with a fixed-size array.
    Prevents adding undefined attributes at runtime.
    """

    __slots__ = ('_x', '_y')

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def distance_from_origin(self) -> float:
        """Return the Euclidean distance from the origin."""
        return (self._x ** 2 + self._y ** 2) ** 0.5

    def translate(self, dx: float, dy: float) -> "PointWithSlots":
        """Return a new point translated by dx, dy."""
        return PointWithSlots(self._x + dx, self._y + dy)

    def __str__(self) -> str:
        return f"Point({self._x}, {self._y})"

    def __repr__(self) -> str:
        return f"PointWithSlots({self._x}, {self._y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PointWithSlots):
            return NotImplemented
        return self._x == other._x and self._y == other._y


class PointWithoutSlots:
    """A 2D point without __slots__ — uses __dict__ for attributes."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"PointWithoutSlots({self.x}, {self.y})"


class Colour:
    """An RGB colour value using __slots__."""

    __slots__ = ('_red', '_green', '_blue')

    def __init__(self, red: int, green: int, blue: int) -> None:
        for val in (red, green, blue):
            if not 0 <= val <= 255:
                raise ValueError(f"Colour value {val} must be between 0 and 255.")
        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self) -> int:
        return self._red

    @property
    def green(self) -> int:
        return self._green

    @property
    def blue(self) -> int:
        return self._blue

    def to_hex(self) -> str:
        """Return the colour as a hex string e.g. #ff5733."""
        return f"#{self._red:02x}{self._green:02x}{self._blue:02x}"

    def to_tuple(self) -> Tuple[int, int, int]:
        """Return the colour as an (r, g, b) tuple."""
        return (self._red, self._green, self._blue)

    def __repr__(self) -> str:
        return f"Colour({self._red}, {self._green}, {self._blue})"

    def __str__(self) -> str:
        return self.to_hex()


if __name__ == "__main__":
    print("=== __slots__ vs no __slots__ ===\n")

    with_slots = PointWithSlots(3.0, 4.0)
    without_slots = PointWithoutSlots(3.0, 4.0)

    print(f"  With slots    : {with_slots}")
    print(f"  Without slots : {without_slots}")
    print(f"  Distance      : {with_slots.distance_from_origin():.2f}")

    print(f"\n  Has __dict__ (with slots)    : {hasattr(with_slots, '__dict__')}")
    print(f"  Has __dict__ (without slots) : {hasattr(without_slots, '__dict__')}")

    print(f"\n  Memory (with slots)    : {sys.getsizeof(with_slots)} bytes")
    print(f"  Memory (without slots) : {sys.getsizeof(without_slots)} bytes")

    print("\n  Dynamic attribute on without_slots:")
    without_slots.extra = "allowed"
    print(f"  without_slots.extra = '{without_slots.extra}'")

    print("\n  Dynamic attribute on with_slots:")
    try:
        with_slots.extra = "not allowed"
    except AttributeError as e:
        print(f"  AttributeError: {e}")

    print("\n=== Colour with __slots__ ===\n")
    try:
        c = Colour(255, 87, 51)
        print(f"  {c}")
        print(f"  Hex   : {c.to_hex()}")
        print(f"  Tuple : {c.to_tuple()}")

        bad = Colour(300, 0, 0)
    except ValueError as e:
        print(f"  ValueError: {e}")