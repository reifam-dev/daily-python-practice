# Day 17 - Clean ParkingLot class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class ParkingLot:
    """Manages a parking lot with a fixed number of spaces."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self._capacity: int = capacity
        self._parked_cars: List[str] = []

    def park_car(self, registration: str) -> None:
        """Park a car by registration. Raises ValueError if full or already parked."""
        if not registration or not registration.strip():
            raise ValueError("Registration cannot be empty.")
        if registration in self._parked_cars:
            raise ValueError(f"'{registration}' is already parked.")
        if len(self._parked_cars) >= self._capacity:
            raise ValueError("Parking lot is full.")
        self._parked_cars.append(registration.strip())

    def remove_car(self, registration: str) -> None:
        """Remove a car by registration. Raises KeyError if not found."""
        if registration not in self._parked_cars:
            raise KeyError(f"'{registration}' is not in the parking lot.")
        self._parked_cars.remove(registration)

    def is_space_available(self) -> bool:
        """Return True if at least one space is available."""
        return len(self._parked_cars) < self._capacity

    def get_occupied_spaces(self) -> int:
        """Return the number of occupied spaces."""
        return len(self._parked_cars)

    def get_available_spaces(self) -> int:
        """Return the number of available spaces."""
        return self._capacity - len(self._parked_cars)

    def get_parked_cars(self) -> List[str]:
        """Return a copy of all currently parked registrations."""
        return self._parked_cars.copy()


if __name__ == "__main__":
    try:
        lot = ParkingLot(3)
        lot.park_car("AB12 CDE")
        lot.park_car("XY99 ZZZ")

        print(f"Parked cars      : {lot.get_parked_cars()}")
        print(f"Occupied spaces  : {lot.get_occupied_spaces()}")
        print(f"Available spaces : {lot.get_available_spaces()}")
        print(f"Space available  : {lot.is_space_available()}")

        lot.remove_car("AB12 CDE")
        print(f"After removing AB12 CDE: {lot.get_parked_cars()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")