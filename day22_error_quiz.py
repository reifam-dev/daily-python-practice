# Day 22 - Error Finding Quiz

class HotelBooking:

    def __init__(self, total_rooms):
        self.total_rooms = total_rooms
        self.booked_rooms = []

    def book_room(self, room_number):
        if room_number in self.booked_rooms:
            print("Room already booked.")
        self.booked_rooms.append(room_number)   # Bug 1 - missing else

    def check_out(self, room_number):
        self.booked_rooms.remove(room_number)   # Bug 2 - no check

    def is_available(self, room_number):
        return room_number not in booked_rooms  # Bug 3 - missing self

    def get_booked_count(self):
        return len(self.booked_rooms)

hotel = HotelBooking(10)
hotel.book_room(101)
hotel.book_room(102)
print(hotel.is_available(101))
print(hotel.get_booked_count())