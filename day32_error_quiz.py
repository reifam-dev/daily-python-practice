# Day 32 - Error Finding Quiz

class Animal:

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.species})"

    def __repr__(self):
        return f"Animal({self.name}, {self.species}, {self.age})"  # Bug 1 - missing quotes around string values

    @staticmethod
    def is_adult(age):
        return age > 3

    def have_birthday(self):
        self.age =+ 1    # Bug 2 - wrong operator


class Zoo:

    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def get_adults(self):
        return [a for a in animals if Animal.is_adult(a.age)]  # Bug 3 - missing self

    def get_count(self):
        return len(self.animals)

zoo = Zoo()
zoo.add_animal(Animal("Leo", "Lion", 5))
zoo.add_animal(Animal("Nemo", "Fish", 1))
print(zoo.get_adults())