# Day 34 - Error Finding Quiz

class Notification:

    def __init__(self, title, priority):
        self.title = title
        self.priority = priority

    def __eq__(self, other):
        return self.title == other.title   # Bug 1 - should also check type

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return f"Notification('{self.title}', priority={self.priority})"


class NotificationSystem:

    def __init__(self):
        self.notifications = []

    def add_notification(self, notification):
        notifications.append(notification)   # Bug 2 - missing self

    def get_sorted(self):
        return sorted(self.notifications)

    def remove_notification(self, notification):
        self.notifications.remove(notification)  # Bug 3 - no check

n1 = Notification("Email", 2)
n2 = Notification("Email", 2)
print(n1 == n2)           # Should be True - uses __eq__
print(n1 is n2)           # Should be False - different objects