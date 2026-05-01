# Day 21 - Error Finding Quiz

class GymMembership:

    def __init__(self):
        self.members = []

    def add_member(self, name):
        if name in self.members:
            print("Already a member.")
        self.members.append(name)   # Bug 1 - missing else

    def cancel_membership(self, name):
        self.members.remove(name)   # Bug 2 - no check

    def is_active(self, name):
        return name in members      # Bug 3 - missing self

    def get_member_count(self):
        return len(self.members)

gym = GymMembership()
gym.add_member("Alice")
gym.add_member("Bob")
print(gym.is_active("Alice"))
print(gym.get_member_count())