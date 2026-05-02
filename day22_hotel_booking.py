# Day 22 - Clean HotelBooking class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class HotelBooking:
    """Manages hotel room bookings with a fixed number of rooms."""

    def __init__(self, total_rooms: int) -> None:
        if total_rooms <= 0:
            raise ValueError("Total rooms must be a positive integer.")
        self._total_rooms: int = total_rooms
        self._booked_rooms: List[int] = []

    def book_room(self, room_number: int) -> None:
        """Book a room. Raises ValueError if already booked or out of range."""
        if not 1 <= room_number <= self._total_rooms:
            raise ValueError(f"Room {room_number} is out of range.")
        if room_number in self._booked_rooms:
            raise ValueError(f"Room {room_number} is already booked.")
        self._booked_rooms.append(room_number)

    def check_out(self, room_number: int) -> None:
        """Check out of a room. Raises KeyError if room was not booked."""
        if room_number not in self._booked_rooms:
            raise KeyError(f"Room {room_number} is not currently booked.")
        self._booked_rooms.remove(room_number)

    def is_available(self, room_number: int) -> bool:
        """Return True if the room is available."""
        return room_number not in self._booked_rooms

    def get_booked_count(self) -> int:
        """Return the number of currently booked rooms."""
        return len(self._booked_rooms)

    def get_available_count(self) -> int:
        """Return the number of available rooms."""
        return self._total_rooms - len(self._booked_rooms)

    def get_booked_rooms(self) -> List[int]:
        """Return a sorted list of all booked room numbers."""
        return sorted(self._booked_rooms)


if __name__ == "__main__":
    try:
        hotel = HotelBooking(10)
        hotel.book_room(101)
        hotel.book_room(102)
        hotel.book_room(105)

        print(f"Booked rooms     : {hotel.get_booked_rooms()}")
        print(f"Booked count     : {hotel.get_booked_count()}")
        print(f"Available count  : {hotel.get_available_count()}")
        print(f"Room 101 free    : {hotel.is_available(101)}")
        print(f"Room 103 free    : {hotel.is_available(103)}")

        hotel.check_out(102)
        print(f"After checkout 102: {hotel.get_booked_rooms()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")