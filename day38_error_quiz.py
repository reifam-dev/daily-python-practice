# Day 38 - Error Finding Quiz

import functools

def log_call(func):
    def wrapper(*args, **kwargs):    # Bug 1 - missing @functools.wraps(func)
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

def validate_positive(func):
    @functools.wraps(func)
    def wrapper(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        return func(self, amount)
    return wrapper

class Account:

    def __init__(self, balance):
        self.balance = balance

    @log_call
    @validate_positive
    def deposit(self, amount):
        """Deposit funds into the account."""
        self.balance += amount

    def get_balance(self):
        return self.balance

acc = Account(100)
acc.deposit(50)
print(acc.deposit.__name__)   # Bug 2 - prints 'wrapper' not 'deposit'
print(acc.get_balance())