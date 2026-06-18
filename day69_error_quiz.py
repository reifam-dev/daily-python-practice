# Day 69 - Error Finding Quiz

import unittest

class Calculator:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertRaises(ValueError, self.calc.divide, 10, 0)  # correct

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_wrong_assertion(self):
        self.assertEqual(self.calc.add(2, 2), 5)  # Bug 1 - 2+2=4 not 5, test will fail

    def test_type_check(self):
        result = self.calc.add(1.5, 2.5)
        self.assertIsInstance(result, int)  # Bug 2 - result is float not int

    def not_a_test(self):       # Bug 3 - not discovered, method name must start with test_
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)