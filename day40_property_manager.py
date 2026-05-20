# Day 40 - Clean Temperature and Circle classes using @property
# New concepts: @property, @<name>.setter, @<name>.deleter
# PEP 8, docstrings, type hints, exceptions throughout

import math
from typing import Optional


class Temperature:
    """Represents a temperature with Celsius and Fahrenheit properties.

    Uses @property to provide validated access to temperature values.
    Demonstrates computed properties — fahrenheit is derived from celsius.
    """

    ABSOLUTE_ZERO: float = -273.15

    def __init__(self, celsius: float = 0.0) -> None:
        self.celsius = celsius  # uses the setter for validation

    @property
    def celsius(self) -> float:
        """Return the temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set the temperature in Celsius. Raises ValueError below absolute zero."""
        if value < self.ABSOLUTE_ZERO:
            raise ValueError(
                f"Temperature {value}°C is below absolute zero "
                f"({self.ABSOLUTE_ZERO}°C)."
            )
        self._celsius = value

    @celsius.deleter
    def celsius(self) -> None:
        """Reset temperature to 0°C when deleted."""
        print("  Resetting temperature to 0°C.")
        self._celsius = 0.0

    @property
    def fahrenheit(self) -> float:
        """Return the temperature in Fahrenheit (computed from Celsius)."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set temperature via Fahrenheit — converts and validates via celsius setter."""
        self.celsius = (value - 32) * 5 / 9

    def __str__(self) -> str:
        return f"Temperature({self._celsius:.2f}°C / {self.fahrenheit:.2f}°F)"


class Circle:
    """Represents a circle with a validated radius and computed properties.

    Demonstrates read-only computed properties (area, diameter, circumference).
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius  # uses the setter for validation

    @property
    def radius(self) -> float:
        """Return the circle radius."""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """Set the radius. Raises ValueError if negative."""
        if value < 0:
            raise ValueError(f"Radius cannot be negative. Got {value}.")
        self._radius = value

    @property
    def diameter(self) -> float:
        """Return the diameter (computed from radius)."""
        return self._radius * 2

    @property
    def area(self) -> float:
        """Return the area (computed from radius)."""
        return math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        """Return the circumference (computed from radius)."""
        return 2 * math.pi * self._radius

    def __str__(self) -> str:
        return (f"Circle(radius={self._radius:.2f}, "
                f"area={self.area:.2f}, "
                f"circumference={self.circumference:.2f})")


if __name__ == "__main__":
    try:
        print("=== Temperature ===\n")
        t = Temperature(100)
        print(f"  {t}")

        t.celsius = 0
        print(f"  After setting to 0°C: {t}")

        t.fahrenheit = 212
        print(f"  After setting to 212°F: {t}")

        del t.celsius
        print(f"  After del: {t}")

        print("\n=== Circle ===\n")
        c = Circle(5)
        print(f"  {c}")
        print(f"  Diameter      : {c.diameter:.2f}")

        c.radius = 10
        print(f"  After radius=10: {c}")

        print("\n=== Invalid values ===\n")
        t.celsius = -300

    except ValueError as e:
        print(f"  Error: {e}")