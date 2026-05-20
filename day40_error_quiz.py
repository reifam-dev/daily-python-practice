# Day 40 - Error Finding Quiz

class Temperature:

    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero.")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9   # correct


class Circle:

    def __init__(self, radius):
        self.radius = radius   # Bug 1 - should use property setter for validation

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius   # Bug 2 - should be radius squared

    @property
    def diameter(self):
        return self.radius * 2


t = Temperature(100)
print(t.celsius)
print(t.fahrenheit)
t.celsius = 200
c = Circle(5)
print(c.area)
print(c.diameter)