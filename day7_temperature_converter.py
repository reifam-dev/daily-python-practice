# Day 7 - Clean TemperatureConverter class (PEP 8 + exceptions)

from typing import Union

class TemperatureConverter:
    """Handles temperature conversions between Celsius and Fahrenheit."""

    def celsius_to_fahrenheit(self, celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return celsius * 9 / 5 + 32

    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5 / 9


if __name__ == "__main__":
    try:
        conv = TemperatureConverter()
        print(f"0°C = {conv.celsius_to_fahrenheit(0):.1f}°F")
        print(f"32°F = {conv.fahrenheit_to_celsius(32):.1f}°C")
    except Exception as e:
        print(f"Error: {e}")