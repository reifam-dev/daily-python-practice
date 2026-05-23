# Day 43 - Error Finding Quiz

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Subject:

    def __init__(self):
        self._observers = []

    def register(self, observer):
        observers.append(observer)   # Bug 1 - missing self

    def unregister(self, observer):
        self._observers.remove(observer)  # Bug 2 - no check

    def notify_all(self, message):
        for observer in self._observers:
            observer.update(message)   # correct

class EmailObserver(Observer):

    def __init__(self, email):
        self.email = email

    def update(self, message):
        print(f"Email to {self.email}: {message}")


class SMSObserver(Observer):

    def __init__(self, phone):
        self.phone = phone

    def update(self, message):
        print(f"SMS to {self.phone}: {message}")   # correct


subject = Subject()
email_obs = EmailObserver("alice@example.com")
sms_obs = SMSObserver("+44123456789")
subject.register(email_obs)
subject.register(sms_obs)
subject.notify_all("System update available")
subject.unregister(email_obs)
subject.notify_all("Maintenance scheduled")   # Bug 3 - unregister had no check