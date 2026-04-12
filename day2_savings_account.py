# Day 2 - Clean SavingsAccount using inheritance

class BankAccount:
    """Base class for all accounts."""

    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def get_balance(self) -> float:
        return self._balance


class SavingsAccount(BankAccount):
    """Savings account with interest (inherits from BankAccount)."""

    def __init__(self, initial_balance: float = 0.0, interest_rate: float = 0.03):
        super().__init__(initial_balance)          # Proper inheritance
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        self._interest_rate = interest_rate

    def add_interest(self) -> None:
        """Add interest to the balance."""
        interest = self._balance * self._interest_rate
        self._balance += interest

    def get_interest_rate(self) -> float:
        return self._interest_rate


# Main execution
if __name__ == "__main__":
    try:
        savings = SavingsAccount(1000.0, 0.05)
        savings.deposit(200.0)
        savings.add_interest()
        print(f"Final balance: ${savings.get_balance():.2f}")
        print(f"Interest rate: {savings.get_interest_rate()*100:.1f}%")
    except ValueError as e:
        print(f"Error: {e}")