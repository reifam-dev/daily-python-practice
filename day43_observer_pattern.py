# Day 43 - Clean Observer pattern
# New concepts: Observer design pattern, Subject-Observer relationship
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Abstract base class for all observers.

    Any class that wants to receive notifications must implement update().
    """

    @abstractmethod
    def update(self, message: str) -> None:
        """Receive and handle a notification message."""
        pass


class Subject:
    """Maintains a list of observers and notifies them of state changes.

    Demonstrates composition — Subject holds a List[Observer].
    """

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def register(self, observer: Observer) -> None:
        """Register an observer. Raises ValueError if already registered."""
        if observer in self._observers:
            raise ValueError("Observer already registered.")
        self._observers.append(observer)

    def unregister(self, observer: Observer) -> None:
        """Unregister an observer. Raises KeyError if not registered."""
        if observer not in self._observers:
            raise KeyError("Observer not registered.")
        self._observers.remove(observer)

    def notify_all(self, message: str) -> None:
        """Notify all registered observers with a message."""
        for observer in self._observers:
            observer.update(message)

    def get_observer_count(self) -> int:
        """Return the number of registered observers."""
        return len(self._observers)


class EmailObserver(Observer):
    """An observer that sends email notifications."""

    def __init__(self, email: str) -> None:
        self._email = email

    def update(self, message: str) -> None:
        print(f"  Email to {self._email}: {message}")

    def __str__(self) -> str:
        return f"EmailObserver('{self._email}')"


class SMSObserver(Observer):
    """An observer that sends SMS notifications."""

    def __init__(self, phone: str) -> None:
        self._phone = phone

    def update(self, message: str) -> None:
        print(f"  SMS to {self._phone}: {message}")

    def __str__(self) -> str:
        return f"SMSObserver('{self._phone}')"


class LogObserver(Observer):
    """An observer that logs notifications to an internal list."""

    def __init__(self) -> None:
        self._log: List[str] = []

    def update(self, message: str) -> None:
        self._log.append(message)
        print(f"  Log: {message}")

    def get_log(self) -> List[str]:
        """Return all logged messages."""
        return self._log.copy()

    def __str__(self) -> str:
        return "LogObserver()"


if __name__ == "__main__":
    try:
        subject = Subject()

        email_obs = EmailObserver("alice@example.com")
        sms_obs = SMSObserver("+44123456789")
        log_obs = LogObserver()

        subject.register(email_obs)
        subject.register(sms_obs)
        subject.register(log_obs)

        print(f"Observers registered: {subject.get_observer_count()}\n")

        print("=== Notification 1 ===")
        subject.notify_all("System update available")

        subject.unregister(sms_obs)
        print(f"\nAfter unregistering SMS — observers: {subject.get_observer_count()}\n")

        print("=== Notification 2 ===")
        subject.notify_all("Maintenance scheduled for tonight")

        print(f"\nLog history: {log_obs.get_log()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")