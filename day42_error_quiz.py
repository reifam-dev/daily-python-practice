# Day 42 - Error Finding Quiz

from abc import ABC, abstractmethod

class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass

class Swimmable(ABC):
    @abstractmethod
    def swim(self):
        pass

class Walkable(ABC):
    @abstractmethod
    def walk(self):
        pass

class Duck(Flyable, Swimmable, Walkable):

    def __init__(self, name):
        self.name = name

    def fly(self):
        return f"{self.name} is flying."

    def swim(self):
        return f"{self.name} is swimming."

    # Bug 1 - missing walk() implementation


class Fish(Swimmable):

    def __init__(self, name):
        self.name = name

    def swim(self):
        return f"{name} is swimming."   # Bug 2 - missing self


class Eagle(Flyable, Walkable):

    def __init__(self, name):
        self.name = name

    def fly(self):
        return f"{self.name} is flying."

    def walk(self):
        return f"{self.name} is walking."


duck = Duck("Donald")   # Bug 3 - Duck cannot be instantiated without walk()
fish = Fish("Nemo")
print(fish.swim())