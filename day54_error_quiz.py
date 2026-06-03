# Day 54 - Error Finding Quiz

import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative.")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)


def multiply(x, y):
    return x * y

numbers = [1, 2, 3, 4, 5]
product = functools.reduce(multiply, numbers)


class MathHelper:

    @functools.lru_cache(maxsize=None)
    def factorial(self, n):       # Bug 1 - lru_cache on instance method is problematic
        if n <= 1:                #         should be @staticmethod
            return 1
        return n * self.factorial(n - 1)


print(fibonacci(10))
print(fibonacci.cache_info())
print(square(5))
print(cube(3))
print(product)

bad_result = functools.reduce(lambda acc, x: acc + x, [])  # Bug 2 - no initial value on empty list raises TypeError
print(bad_result)

total = functools.reduce(lambda acc, x: acc =+ x, numbers, 0)  # Bug 3 - wrong operator
print(total)