# Day 1 - Clean BankAccount class with proper encapsulation

class BankAccount:
    """Simple bank account with encapsulation and validation."""

    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance   # protected attribute

    def deposit(self, amount: float) -> None:
        """Deposit money. Amount must be positive."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw money. Check for sufficient funds."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self) -> float:
        """Return current balance."""
        return self._balance


# Main execution
if __name__ == "__main__":
    try:
        account = BankAccount(100.0)
        account.deposit(50.0)
        account.withdraw(30.0)
        print(f"Final balance: ${account.get_balance():.2f}")
    except ValueError as e:
        print(f"Error: {e}")