# Day 26 - Error Finding Quiz

class AppointmentScheduler:

    def __init__(self):
        self.appointments = {}

    def book_appointment(self, time_slot, name):
        if time_slot in self.appointments:
            print("Slot already taken.")
        appointments[time_slot] = name    # Bug 1 - missing self, missing else

    def cancel_appointment(self, time_slot):
        del self.appointments[time_slot]  # Bug 2 - no check

    def is_slot_taken(self, time_slot):
        return time_slot in self.appointments

    def get_all_appointments(self):
        return self.appointments          # Bug 3 - returns internal dict directly

scheduler = AppointmentScheduler()
scheduler.book_appointment("09:00", "Alice")
scheduler.book_appointment("10:00", "Bob")
print(scheduler.is_slot_taken("09:00"))