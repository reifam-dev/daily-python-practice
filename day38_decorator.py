# Day 38 - Clean decorator examples with functools.wraps
# New concepts: @decorator syntax, functools.wraps, decorator factory
# PEP 8, docstrings, type hints, exceptions throughout

import functools
from typing import Callable, Any


def log_call(func: Callable) -> Callable:
    """Decorator that logs when a function is called and when it finishes."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"  --> Calling {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"  <-- Finished {func.__name__}()")
        return result
    return wrapper


def validate_positive(func: Callable) -> Callable:
    """Decorator that raises ValueError if the amount argument is not positive."""
    @functools.wraps(func)
    def wrapper(self: Any, amount: float) -> Any:
        if amount <= 0:
            raise ValueError(f"Amount must be positive. Got {amount}.")
        return func(self, amount)
    return wrapper


def repeat(times: int) -> Callable:
    """Decorator factory — returns a decorator that calls the function `times` times."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


class BankAccount:
    """A simple bank account demonstrating decorator usage."""

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self._owner = owner
        self._balance = balance

    @log_call
    @validate_positive
    def deposit(self, amount: float) -> None:
        """Deposit funds into the account."""
        self._balance += amount

    @log_call
    @validate_positive
    def withdraw(self, amount: float) -> None:
        """Withdraw funds from the account."""
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Balance: £{self._balance:.2f}."
            )
        self._balance -= amount

    def get_balance(self) -> float:
        """Return the current balance."""
        return self._balance

    def __str__(self) -> str:
        return f"BankAccount(owner='{self._owner}', balance=£{self._balance:.2f})"


@repeat(3)
def greet(name: str) -> None:
    """Greet a person by name."""
    print(f"  Hello, {name}!")


if __name__ == "__main__":
    try:
        print("=== BankAccount with decorators ===\n")
        acc = BankAccount("Alice", 100.0)

        acc.deposit(50)
        print(f"Balance after deposit    : £{acc.get_balance():.2f}\n")

        acc.withdraw(30)
        print(f"Balance after withdrawal : £{acc.get_balance():.2f}\n")

        print(f"Function name preserved  : {acc.deposit.__name__}")
        print(f"Docstring preserved      : {acc.deposit.__doc__}\n")

        print("=== Decorator factory — @repeat(3) ===\n")
        greet("Bob")

        print("\n=== Invalid amount — @validate_positive ===\n")
        acc.deposit(-10)

    except ValueError as e:
        print(f"Error: {e}")