# Day 4 - Abstract classes and interfaces using ABC

from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class - forces subclasses to implement area()."""

    @abstractmethod
    def area(self) -> float:
        """Calculate area of the shape."""
        pass

    def describe(self) -> str:
        """Common method available to all shapes."""
        return f"This is a {self.__class__.__name__} with area {self.area():.2f}"


class Circle(Shape):
    """Concrete class implementing the abstract Shape."""

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    """Concrete class implementing the abstract Shape."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


# Main execution - demonstrating abstraction
if __name__ == "__main__":
    shapes = [Circle(5.0), Rectangle(4.0, 6.0)]

    for shape in shapes:
        print(shape.describe())