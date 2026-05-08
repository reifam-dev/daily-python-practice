# Day 28 - Clean TicketBooking class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class TicketBooking:
    """Manages ticket bookings with a fixed number of available tickets."""

    def __init__(self, total_tickets: int) -> None:
        if total_tickets <= 0:
            raise ValueError("Total tickets must be a positive integer.")
        self._total_tickets: int = total_tickets
        self._booked: List[str] = []

    def book_ticket(self, name: str) -> None:
        """Book a ticket. Raises ValueError if sold out, already booked or name invalid."""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        if name.strip() in self._booked:
            raise ValueError(f"'{name}' already has a ticket.")
        if len(self._booked) >= self._total_tickets:
            raise ValueError("No tickets available.")
        self._booked.append(name.strip())

    def cancel_ticket(self, name: str) -> None:
        """Cancel a ticket. Raises KeyError if name not found."""
        if name not in self._booked:
            raise KeyError(f"No ticket found for '{name}'.")
        self._booked.remove(name)

    def is_available(self) -> bool:
        """Return True if at least one ticket is still available."""
        return len(self._booked) < self._total_tickets

    def get_booked_count(self) -> int:
        """Return the number of booked tickets."""
        return len(self._booked)

    def get_remaining_count(self) -> int:
        """Return the number of remaining tickets."""
        return self._total_tickets - len(self._booked)

    def get_all_booked(self) -> List[str]:
        """Return a copy of all names with booked tickets."""
        return self._booked.copy()


if __name__ == "__main__":
    try:
        booking = TicketBooking(3)
        booking.book_ticket("Alice")
        booking.book_ticket("Bob")
        booking.book_ticket("Charlie")

        print(f"Booked           : {booking.get_all_booked()}")
        print(f"Tickets booked   : {booking.get_booked_count()}")
        print(f"Remaining        : {booking.get_remaining_count()}")
        print(f"Available        : {booking.is_available()}")

        booking.cancel_ticket("Bob")
        print(f"After cancelling Bob: {booking.get_all_booked()}")
        print(f"Remaining        : {booking.get_remaining_count()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")