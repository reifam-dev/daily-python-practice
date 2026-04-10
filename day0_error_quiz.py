# Day 0 - Error Finding Quiz (Find and fix the bugs)

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello! My name is {self.name} and I am {self.age} years old."

# Create person
p = Person("Jevgeni", 30)   # Age should be number, not string

print(p.greet())