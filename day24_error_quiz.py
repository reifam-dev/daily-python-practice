# Day 24 - Error Finding Quiz

class VehicleTracker:

    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, registration):
        if registration in self.vehicles:
            print("Already registered.")
        self.vehicles.append(registration)   # Bug 1 - missing else

    def remove_vehicle(self, registration):
        self.vehicles.remove(registration)   # Bug 2 - no check

    def is_registered(self, registration):
        return registration in vehicles      # Bug 3 - missing self

    def get_vehicle_count(self):
        return len(self.vehicles)

tracker = VehicleTracker()
tracker.add_vehicle("AB12 CDE")
tracker.add_vehicle("XY99 ZZZ")
print(tracker.is_registered("AB12 CDE"))
print(tracker.get_vehicle_count())