# Day 3 - Polymorphism with method overriding

class Account:
    """Base class demonstrating polymorphism."""

    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Default withdraw behavior (can be overridden)."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self) -> float:
        return self._balance


class CheckingAccount(Account):
    """Checking account with withdrawal fee (overrides withdraw)."""

    def __init__(self, initial_balance: float = 0.0):
        super().__init__(initial_balance)
        self._fee = 1.0

    def withdraw(self, amount: float) -> None:
        """Override: charge a small fee on every withdrawal."""
        total = amount + self._fee
        super().withdraw(total)   # Reuse base logic


class SavingsAccount(Account):
    """Savings account with withdrawal restrictions (overrides withdraw)."""

    def withdraw(self, amount: float) -> None:
        """Override: block withdrawals (example of restrictive polymorphism)."""
        raise ValueError("Withdrawals not allowed from SavingsAccount. Use transfer instead.")


# Main execution - demonstrating polymorphism
if __name__ == "__main__":
    try:
        checking = CheckingAccount(100.0)
        savings = SavingsAccount(200.0)

        checking.deposit(50.0)
        checking.withdraw(30.0)          # Uses overridden method
        print(f"Checking balance: ${checking.get_balance():.2f}")

        # savings.withdraw(20.0)         # This will raise error (polymorphic behavior)
        print(f"Savings balance: ${savings.get_balance():.2f}")

    except ValueError as e:
        print(f"Error: {e}")