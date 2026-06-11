# Day 62 - Clean ABC with abstract property, classmethod and staticmethod
# New concepts: @property @abstractmethod, @classmethod @abstractmethod,
#               @staticmethod @abstractmethod
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List


class Vehicle(ABC):
    """Abstract base class for all vehicle types.

    Demonstrates abstract property, classmethod and staticmethod —
    subclasses must implement all three alongside regular abstract methods.
    """

    @property
    @abstractmethod
    def max_speed(self) -> float:
        """Return the maximum speed in km/h."""
        pass

    @classmethod
    @abstractmethod
    def vehicle_type(cls) -> str:
        """Return the type name of the vehicle."""
        pass

    @staticmethod
    @abstractmethod
    def fuel_type() -> str:
        """Return the fuel type of the vehicle."""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Return a full description of the vehicle."""
        pass

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Car(Vehicle):
    """A petrol-powered car."""

    def __init__(self, model: str) -> None:
        self._model = model

    @property
    def max_speed(self) -> float:
        return 200.0

    @classmethod
    def vehicle_type(cls) -> str:
        return "Car"

    @staticmethod
    def fuel_type() -> str:
        return "Petrol"

    def describe(self) -> str:
        return (f"{self.vehicle_type()} '{self._model}' | "
                f"{self.fuel_type()} | "
                f"max {self.max_speed:.0f} km/h")


class ElectricCar(Vehicle):
    """An electric car with a range in km."""

    def __init__(self, model: str, range_km: float) -> None:
        self._model = model
        self._range_km = range_km

    @property
    def max_speed(self) -> float:
        return 250.0

    @property
    def range_km(self) -> float:
        return self._range_km

    @classmethod
    def vehicle_type(cls) -> str:
        return "Electric Car"

    @staticmethod
    def fuel_type() -> str:
        return "Electric"

    def describe(self) -> str:
        return (f"{self.vehicle_type()} '{self._model}' | "
                f"{self.fuel_type()} | "
                f"max {self.max_speed:.0f} km/h | "
                f"range {self._range_km:.0f} km")


class Bicycle(Vehicle):
    """A human-powered bicycle."""

    def __init__(self, brand: str) -> None:
        self._brand = brand

    @property
    def max_speed(self) -> float:
        return 40.0

    @classmethod
    def vehicle_type(cls) -> str:
        return "Bicycle"

    @staticmethod
    def fuel_type() -> str:
        return "Human-powered"

    def describe(self) -> str:
        return (f"{self.vehicle_type()} '{self._brand}' | "
                f"{self.fuel_type()} | "
                f"max {self.max_speed:.0f} km/h")


def print_fleet(vehicles: List[Vehicle]) -> None:
    """Print all vehicles in a fleet."""
    for v in vehicles:
        print(f"  {v}")


if __name__ == "__main__":
    fleet: List[Vehicle] = [
        Car("Tesla Model 3 Petrol"),
        ElectricCar("Tesla Model S", 600),
        Bicycle("Brompton"),
    ]

    print("=== Fleet ===\n")
    print_fleet(fleet)

    print("\n=== Class and static methods called on class ===\n")
    print(f"  Car.vehicle_type()  : {Car.vehicle_type()}")
    print(f"  Car.fuel_type()     : {Car.fuel_type()}")
    print(f"  ElectricCar type    : {ElectricCar.vehicle_type()}")

    print("\n=== isinstance checks ===\n")
    for v in fleet:
        print(f"  {v.__class__.__name__} is Vehicle: {isinstance(v, Vehicle)}")

    print("\n=== Cannot instantiate abstract class ===\n")
    try:
        bad = Vehicle()
    except TypeError as e:
        print(f"  TypeError: {e}")