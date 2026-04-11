# Day 1 - Error Finding Quiz (Find and fix at least 6 issues)

class BankAccount:
    """BankAccount class demonstrating basic OOP."""

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        """Print amount deposited."""
        self.balance = self.balance + amount
        print("Deposited", amount)

    def withdraw(self, amount):
        """Print amount withdrawn."""
        if amount > self.balance:
            print("Insufficient funds")
        self.balance = self.balance - amount   # No check + logic error


# Main execution

acc = BankAccount(-100)   # Negative balance allowed
acc.deposit(50)           # Wrong type
acc.withdraw(30)
print(acc.balance)