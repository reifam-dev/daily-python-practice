# Day 28 - Error Finding Quiz

class TicketBooking:

    def __init__(self, total_tickets):
        self.total_tickets = total_tickets
        self.booked = []

    def book_ticket(self, name):
        if len(self.booked) >= self.total_tickets:
            print("No tickets available.")
        self.booked.append(name)       # Bug 1 - missing else

    def cancel_ticket(self, name):
        self.booked.remove(name)       # Bug 2 - no check

    def is_available(self):
        return len(booked) < self.total_tickets  # Bug 3 - missing self

    def get_booked_count(self):
        return len(self.booked)

booking = TicketBooking(3)
booking.book_ticket("Alice")
booking.book_ticket("Bob")
print(booking.is_available())
print(booking.get_booked_count())