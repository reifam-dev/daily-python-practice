# Day 7 - Error Finding Quiz

class TemperatureConverter:
    def celsius_to_fahrenheit(self, celsius)
        return celsius * 9 / 5 + 32

    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5 / 9   # Missing validation

conv = TemperatureConverter()
print(conv.celsius_to_fahrenheit(0))
print(conv.fahrenheit_to_celsius(32))