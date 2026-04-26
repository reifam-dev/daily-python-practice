# Day 16 - Clean CinemaBooking class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class CinemaBooking:
    """Manages seat bookings for a cinema with a fixed number of seats."""

    def __init__(self, total_seats: int) -> None:
        if total_seats <= 0:
            raise ValueError("Total seats must be a positive integer.")
        self._total_seats: int = total_seats
        self._booked: List[int] = []

    def book_seat(self, seat_number: int) -> None:
        """Book a seat. Raises ValueError if already booked or invalid."""
        if not 1 <= seat_number <= self._total_seats:
            raise ValueError(f"Seat {seat_number} is out of range.")
        if seat_number in self._booked:
            raise ValueError(f"Seat {seat_number} is already booked.")
        self._booked.append(seat_number)

    def cancel_booking(self, seat_number: int) -> None:
        """Cancel a booking. Raises KeyError if seat was not booked."""
        if seat_number not in self._booked:
            raise KeyError(f"Seat {seat_number} is not currently booked.")
        self._booked.remove(seat_number)

    def is_available(self, seat_number: int) -> bool:
        """Return True if the seat is available."""
        return seat_number not in self._booked

    def get_available_count(self) -> int:
        """Return the number of available seats."""
        return self._total_seats - len(self._booked)

    def get_booked_seats(self) -> List[int]:
        """Return a sorted list of all booked seat numbers."""
        return sorted(self._booked)


if __name__ == "__main__":
    try:
        cinema = CinemaBooking(100)
        cinema.book_seat(5)
        cinema.book_seat(10)
        cinema.book_seat(42)

        print(f"Booked seats     : {cinema.get_booked_seats()}")
        print(f"Seat 5 available : {cinema.is_available(5)}")
        print(f"Seat 7 available : {cinema.is_available(7)}")
        print(f"Available seats  : {cinema.get_available_count()}")

        cinema.cancel_booking(10)
        print(f"After cancelling seat 10: {cinema.get_booked_seats()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")