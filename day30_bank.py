# Day 30 - Clean Bank and BankAccount classes (PEP 8, docstrings, type hints, exceptions)
# Demonstrates composition - a Bank managing multiple BankAccount objects.

from typing import Dict


class BankAccount:
    """Represents a single bank account with deposit and withdrawal functionality."""

    def __init__(self, account_id: int, owner: str, balance: float = 0.0) -> None:
        self._account_id: int = account_id
        self._owner: str = owner
        self._balance: float = balance

    @property
    def account_id(self) -> int:
        """Return the account ID."""
        return self._account_id

    @property
    def owner(self) -> str:
        """Return the account owner name."""
        return self._owner

    @property
    def balance(self) -> float:
        """Return the current balance."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Deposit funds. Raises ValueError if amount is not positive."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw funds. Raises ValueError if amount invalid or insufficient funds."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Balance: £{self._balance:.2f}, "
                f"Requested: £{amount:.2f}."
            )
        self._balance -= amount


class Bank:
    """Manages multiple BankAccount objects. Demonstrates composition."""

    def __init__(self, bank_name: str) -> None:
        self._bank_name: str = bank_name
        self._accounts: Dict[int, BankAccount] = {}

    def create_account(self, account_id: int, owner: str) -> None:
        """Create a new account. Raises ValueError if ID already exists."""
        if account_id in self._accounts:
            raise ValueError(f"Account ID {account_id} already exists.")
        self._accounts[account_id] = BankAccount(account_id, owner)

    def get_balance(self, account_id: int) -> float:
        """Return the balance of an account. Raises KeyError if not found."""
        if account_id not in self._accounts:
            raise KeyError(f"Account ID {account_id} not found.")
        return self._accounts[account_id].balance

    def deposit(self, account_id: int, amount: float) -> None:
        """Deposit into an account. Raises KeyError if account not found."""
        if account_id not in self._accounts:
            raise KeyError(f"Account ID {account_id} not found.")
        self._accounts[account_id].deposit(amount)

    def withdraw(self, account_id: int, amount: float) -> None:
        """Withdraw from an account. Raises KeyError if account not found."""
        if account_id not in self._accounts:
            raise KeyError(f"Account ID {account_id} not found.")
        self._accounts[account_id].withdraw(amount)

    def transfer(self, from_id: int, to_id: int, amount: float) -> None:
        """Transfer funds between two accounts. Raises KeyError if either not found."""
        if from_id not in self._accounts:
            raise KeyError(f"Source account ID {from_id} not found.")
        if to_id not in self._accounts:
            raise KeyError(f"Destination account ID {to_id} not found.")
        self._accounts[from_id].withdraw(amount)
        self._accounts[to_id].deposit(amount)

    def get_account_count(self) -> int:
        """Return the total number of accounts."""
        return len(self._accounts)


if __name__ == "__main__":
    try:
        bank = Bank("Royal Python Bank")

        bank.create_account(1, "Alice")
        bank.create_account(2, "Bob")
        bank.create_account(3, "Charlie")

        bank.deposit(1, 1000)
        bank.deposit(2, 500)
        bank.deposit(3, 750)

        print(f"Accounts         : {bank.get_account_count()}")
        print(f"Alice balance    : £{bank.get_balance(1):.2f}")
        print(f"Bob balance      : £{bank.get_balance(2):.2f}")

        bank.transfer(1, 2, 300)
        print("After transfer of £300 from Alice to Bob:")
        print(f"Alice balance    : £{bank.get_balance(1):.2f}")
        print(f"Bob balance      : £{bank.get_balance(2):.2f}")

        bank.withdraw(3, 200)
        print(f"Charlie balance  : £{bank.get_balance(3):.2f}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")