# Day 34 - Clean Notification and NotificationSystem classes
# New concepts: __eq__, __lt__, rich comparison, sorted() on custom objects
# PEP 8, docstrings, type hints, exceptions throughout

from typing import List


class Notification:
    """Represents a notification with a title and numeric priority."""

    def __init__(self, title: str, priority: int) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        if not isinstance(priority, int) or priority < 1:
            raise ValueError("Priority must be a positive integer.")
        self._title: str = title.strip()
        self._priority: int = priority

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"Notification(title='{self._title}', priority={self._priority})"

    def __repr__(self) -> str:
        """Return a developer-facing string representation."""
        return f"Notification('{self._title}', {self._priority})"

    def __eq__(self, other: object) -> bool:
        """Return True if both title and priority are equal.
        Always check type before comparing attributes.
        """
        if not isinstance(other, Notification):
            return NotImplemented
        return self._title == other._title and self._priority == other._priority

    def __lt__(self, other: "Notification") -> bool:
        """Return True if this notification has lower priority than other.
        Enables sorted() and < comparisons on Notification objects.
        """
        if not isinstance(other, Notification):
            return NotImplemented
        return self._priority < other._priority

    @property
    def title(self) -> str:
        """Return the notification title."""
        return self._title

    @property
    def priority(self) -> int:
        """Return the notification priority."""
        return self._priority


class NotificationSystem:
    """Manages a collection of Notification objects."""

    def __init__(self) -> None:
        self._notifications: List[Notification] = []

    def add_notification(self, notification: Notification) -> None:
        """Add a notification. Raises ValueError if already present."""
        if notification in self._notifications:
            raise ValueError(f"Notification '{notification.title}' already exists.")
        self._notifications.append(notification)

    def remove_notification(self, notification: Notification) -> None:
        """Remove a notification. Raises KeyError if not found."""
        if notification not in self._notifications:
            raise KeyError(f"Notification '{notification.title}' not found.")
        self._notifications.remove(notification)

    def get_sorted(self) -> List[Notification]:
        """Return notifications sorted by priority (lowest number first)."""
        return sorted(self._notifications)

    def get_count(self) -> int:
        """Return the total number of notifications."""
        return len(self._notifications)


if __name__ == "__main__":
    try:
        system = NotificationSystem()

        n1 = Notification("Email", 3)
        n2 = Notification("SMS", 1)
        n3 = Notification("Push Alert", 2)
        n4 = Notification("Email", 3)

        system.add_notification(n1)
        system.add_notification(n2)
        system.add_notification(n3)

        print(f"Count            : {system.get_count()}")

        print(f"\n__eq__ checks:")
        print(f"n1 == n4         : {n1 == n4}")    # True — same title and priority
        print(f"n1 == n2         : {n1 == n2}")    # False
        print(f"n1 is n4         : {n1 is n4}")    # False — different objects

        print(f"\nSorted by priority:")
        for n in system.get_sorted():
            print(f"  {n}")

        system.remove_notification(n2)
        print(f"\nAfter removing SMS: {system.get_count()} notifications")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")