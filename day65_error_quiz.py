# Day 65 - Error Finding Quiz

import copy

class Address:
    def __init__(self, street, city):
        self.street = street
        self.city = city

    def __repr__(self):
        return f"Address('{self.street}', '{self.city}')"


class Person:
    def __init__(self, name, address, hobbies):
        self.name = name
        self.address = address
        self.hobbies = hobbies

    def __repr__(self):
        return f"Person('{self.name}', {self.address}, {self.hobbies})"


original = Person("Alice", Address("123 Main St", "London"), ["reading", "coding"])

# shallow copy
shallow = copy.copy(original)
shallow.name = "Bob"           # correct - primitive, does not affect original
shallow.hobbies.append("golf") # Bug 1 - list is shared, modifies original.hobbies too
shallow.address.city = "Manchester"  # Bug 1b - address object shared

# deep copy
deep = copy.deepcopy(original)
deep.name = "Charlie"
deep.hobbies.append("tennis")  # correct - independent copy
deep.address.city = "Edinburgh"

print(f"original hobbies : {original.hobbies}")  # Bug 1 visible here
print(f"original city    : {original.address.city}")  # Bug 1b visible here

# Bug 2 - copying without import
class Config:
    def __init__(self, settings):
        self.settings = settings

c1 = Config({"theme": "dark"})
c2 = c1   # Bug 2 - this is assignment not copy, same object
c2.settings["theme"] = "light"
print(c1.settings)   # Bug 2 - c1 also changed

# Bug 3
numbers = [1, 2, [3, 4, 5]]
shallow_list = numbers.copy()
shallow_list[2].append(6)  # Bug 3 - nested list is shared, modifies numbers[2]
print(numbers)