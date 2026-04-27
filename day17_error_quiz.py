# Day 17 - Error Finding Quiz

class ParkingLot:

    def __init__(self, capacity):
        self.capacity = capacity
        self.parked_cars = []

    def park_car(self, registration):
        if len(self.parked_cars) >= self.capacity:
            print("Parking lot is full.")
        self.parked_cars.append(registration)   # Bug - missing else

    def remove_car(self, registration):
        self.parked_cars.remove(registration)   # Bug - no check

    def is_space_available(self):
        return len(self.parked_cars) < capacity   # Bug

    def get_occupied_spaces(self):
        return len(self.parked_cars)

lot = ParkingLot(3)
lot.park_car("AB12 CDE")
lot.park_car("XY99 ZZZ")
print(lot.is_space_available())
print(lot.get_occupied_spaces())