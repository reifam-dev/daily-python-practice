# Day 4 - Error Finding Quiz (Fix abstract class/interface issues)

class Shape:
    def area(self):
        pass   # Should be abstract

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

s1 = Circle(5)
s2 = Rectangle(4, 6)
print(s1.area(), s2.area())