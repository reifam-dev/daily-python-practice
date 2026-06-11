# Day 62 - Error Finding Quiz

from abc import ABC, abstractmethod

class Vehicle(ABC):

    @property
    @abstractmethod
    def max_speed(self) -> float:
        pass

    @classmethod
    @abstractmethod
    def vehicle_type(cls) -> str:
        pass

    @staticmethod
    @abstractmethod
    def fuel_type() -> str:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class Car(Vehicle):

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
        return f"{self.vehicle_type()} | {self.fuel_type()} | {self.max_speed} km/h"


class Bicycle(Vehicle):

    @property
    def max_speed(self) -> float:
        return 40.0

    @classmethod
    def vehicle_type(cls) -> str:
        return "Bicycle"

    # Bug 1 - missing fuel_type() static method implementation

    def describe(self) -> str:
        return f"{self.vehicle_type()} | {self.fuel_type()} | {self.max_speed} km/h"


class ElectricCar(Vehicle):

    def __init__(self, range_km: float):
        range_km = range_km    # Bug 2 - missing self

    @property
    def max_speed(self) -> float:
        return 250.0

    @classmethod
    def vehicle_type(cls) -> str:
        return "Electric Car"

    @staticmethod
    def fuel_type() -> str:
        return "Electric"

    def describe(self) -> str:
        return f"{self.vehicle_type()} | {self.fuel_type()} | range: {self.range_km} km"


car = Car()
print(car.describe())
v = Vehicle()    # Bug 3 - cannot instantiate abstract class