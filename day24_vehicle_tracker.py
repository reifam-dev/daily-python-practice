# Day 24 - Clean VehicleTracker class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class VehicleTracker:
    """Tracks registered vehicles by registration plate."""

    def __init__(self) -> None:
        self._vehicles: List[str] = []

    def add_vehicle(self, registration: str) -> None:
        """Register a vehicle. Raises ValueError if already registered or invalid."""
        if not registration or not registration.strip():
            raise ValueError("Registration cannot be empty.")
        if registration.strip() in self._vehicles:
            raise ValueError(f"'{registration}' is already registered.")
        self._vehicles.append(registration.strip())

    def remove_vehicle(self, registration: str) -> None:
        """Remove a vehicle. Raises KeyError if registration not found."""
        if registration not in self._vehicles:
            raise KeyError(f"'{registration}' is not registered.")
        self._vehicles.remove(registration)

    def is_registered(self, registration: str) -> bool:
        """Return True if the vehicle is currently registered."""
        return registration in self._vehicles

    def get_vehicle_count(self) -> int:
        """Return the total number of registered vehicles."""
        return len(self._vehicles)

    def get_all_vehicles(self) -> List[str]:
        """Return a copy of all registered vehicles."""
        return self._vehicles.copy()


if __name__ == "__main__":
    try:
        tracker = VehicleTracker()
        tracker.add_vehicle("AB12 CDE")
        tracker.add_vehicle("XY99 ZZZ")
        tracker.add_vehicle("LM55 PQR")

        print(f"Registered       : {tracker.get_all_vehicles()}")
        print(f"Total            : {tracker.get_vehicle_count()}")
        print(f"AB12 CDE found   : {tracker.is_registered('AB12 CDE')}")
        print(f"ZZ00 ZZZ found   : {tracker.is_registered('ZZ00 ZZZ')}")

        tracker.remove_vehicle("XY99 ZZZ")
        print(f"After removal    : {tracker.get_all_vehicles()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")