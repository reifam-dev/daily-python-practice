# Day 41 - Clean Shape hierarchy with ABC and Factory pattern
# New concepts: ABC at PCPP1 depth, abstract properties, Factory pattern
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base class for all shapes.

    Any subclass must implement area() and perimeter().
    Cannot be instantiated directly.
    """

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the shape."""
        pass

    def describe(self) -> str:
        """Return a description including area and perimeter."""
        return (f"{self.name}: "
                f"area={self.area():.2f}, "
                f"perimeter={self.perimeter():.2f}")

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Rectangle(Shape):
    """A rectangle defined by width and height."""

    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self._width = width
        self._height = height

    @property
    def name(self) -> str:
        return "Rectangle"

    def area(self) -> float:
        """Return width × height."""
        return self._width * self._height

    def perimeter(self) -> float:
        """Return 2 × (width + height)."""
        return 2 * (self._width + self._height)


class Circle(Shape):
    """A circle defined by radius."""

    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("Radius must be positive.")
        self._radius = radius

    @property
    def name(self) -> str:
        return "Circle"

    def area(self) -> float:
        """Return π × radius²."""
        return math.pi * self._radius ** 2

    def perimeter(self) -> float:
        """Return 2 × π × radius (circumference)."""
        return 2 * math.pi * self._radius


class Triangle(Shape):
    """A triangle defined by three side lengths."""

    def __init__(self, a: float, b: float, c: float) -> None:
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("All sides must be positive.")
        if not (a + b > c and b + c > a and a + c > b):
            raise ValueError("Sides do not form a valid triangle.")
        self._a = a
        self._b = b
        self._c = c

    @property
    def name(self) -> str:
        return "Triangle"

    def area(self) -> float:
        """Return area using Heron's formula."""
        s = (self._a + self._b + self._c) / 2
        return math.sqrt(s * (s - self._a) * (s - self._b) * (s - self._c))

    def perimeter(self) -> float:
        """Return sum of all three sides."""
        return self._a + self._b + self._c


class ShapeFactory:
    """Factory class that creates Shape objects by type name.

    Demonstrates the Factory pattern — creates objects without
    exposing instantiation logic to the caller.
    """

    @staticmethod
    def create(shape_type: str, *args: float) -> Shape:
        """Create and return a Shape object.

        Args:
            shape_type: 'rectangle', 'circle' or 'triangle'
            *args: dimensions required by the shape

        Raises:
            ValueError if shape_type is not recognised.
        """
        shape_type = shape_type.lower().strip()
        if shape_type == "rectangle":
            return Rectangle(*args)
        elif shape_type == "circle":
            return Circle(*args)
        elif shape_type == "triangle":
            return Triangle(*args)
        else:
            raise ValueError(f"Unknown shape type: '{shape_type}'.")


if __name__ == "__main__":
    try:
        shapes = [
            ShapeFactory.create("rectangle", 4, 6),
            ShapeFactory.create("circle", 5),
            ShapeFactory.create("triangle", 3, 4, 5),
        ]

        print("=== All shapes ===\n")
        for shape in shapes:
            print(f"  {shape}")

        print("\n=== isinstance checks ===\n")
        for shape in shapes:
            print(f"  {shape.name} is Shape: {isinstance(shape, Shape)}")

        print("\n=== Factory with unknown type ===\n")
        ShapeFactory.create("hexagon", 5)

    except (ValueError, TypeError) as e:
        print(f"  Error: {e}")

    try:
        print("\n=== Cannot instantiate abstract class ===\n")
        s = Shape()
    except TypeError as e:
        print(f"  Error: {e}")