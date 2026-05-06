# Day 26 - Clean AppointmentScheduler class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict


class AppointmentScheduler:
    """Manages appointment bookings by time slot."""

    def __init__(self) -> None:
        self._appointments: Dict[str, str] = {}

    def book_appointment(self, time_slot: str, name: str) -> None:
        """Book an appointment. Raises ValueError if slot taken or inputs invalid."""
        if not time_slot or not time_slot.strip():
            raise ValueError("Time slot cannot be empty.")
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        if time_slot.strip() in self._appointments:
            raise ValueError(f"Slot '{time_slot}' is already booked.")
        self._appointments[time_slot.strip()] = name.strip()

    def cancel_appointment(self, time_slot: str) -> None:
        """Cancel an appointment. Raises KeyError if slot not found."""
        if time_slot not in self._appointments:
            raise KeyError(f"No appointment found at '{time_slot}'.")
        del self._appointments[time_slot]

    def is_slot_taken(self, time_slot: str) -> bool:
        """Return True if the time slot is already booked."""
        return time_slot in self._appointments

    def get_all_appointments(self) -> Dict[str, str]:
        """Return a copy of all booked appointments."""
        return self._appointments.copy()

    def get_appointment_count(self) -> int:
        """Return the total number of booked appointments."""
        return len(self._appointments)


if __name__ == "__main__":
    try:
        scheduler = AppointmentScheduler()
        scheduler.book_appointment("09:00", "Alice")
        scheduler.book_appointment("10:00", "Bob")
        scheduler.book_appointment("11:00", "Charlie")

        print(f"All appointments : {scheduler.get_all_appointments()}")
        print(f"Total booked     : {scheduler.get_appointment_count()}")
        print(f"09:00 taken      : {scheduler.is_slot_taken('09:00')}")
        print(f"14:00 taken      : {scheduler.is_slot_taken('14:00')}")

        scheduler.cancel_appointment("10:00")
        print(f"After cancelling 10:00: {scheduler.get_all_appointments()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")