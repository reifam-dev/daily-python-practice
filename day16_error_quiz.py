# Day 16 - Error Finding Quiz

class CinemaBooking:

    def __init__(self, total_seats):
        self.total_seats = total_seats
        self.booked = []

    def book_seat(self, seat_number):
        if seat_number in self.booked:
            print("Already booked.")
        self.booked.append(seat_number)   # Bug - missing else

    def cancel_booking(self, seat_number):
        self.booked.remove(seat_number)   # Bug - no check

    def is_available(self, seat_number):
        return seat_number not in booked   # Bug

cinema = CinemaBooking(100)
cinema.book_seat(5)
cinema.book_seat(10)
print(cinema.is_available(5))