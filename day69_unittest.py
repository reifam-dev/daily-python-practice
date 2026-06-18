# Day 69 - Clean unittest examples
# New concepts: TestCase, setUp, tearDown, assertions, test discovery
# PEP 8, docstrings, type hints, exceptions throughout

import unittest
from typing import List


class BankAccount:
    """Simple bank account used as the system under test."""

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self._owner = owner
        self._balance = balance
        self._transactions: List[float] = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self._balance += amount
        self._transactions.append(amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._transactions.append(-amount)

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def owner(self) -> str:
        return self._owner

    def get_transactions(self) -> List[float]:
        return self._transactions.copy()


class TestBankAccount(unittest.TestCase):
    """Test suite for BankAccount.

    setUp runs before EACH test method.
    tearDown runs after EACH test method.
    """

    def setUp(self) -> None:
        """Create a fresh account before each test."""
        self.account = BankAccount("Alice", 100.0)

    def tearDown(self) -> None:
        """Called after each test — useful for cleanup."""
        pass

    def test_initial_balance(self) -> None:
        """Account starts with correct balance."""
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.owner, "Alice")

    def test_deposit_increases_balance(self) -> None:
        """Deposit adds to balance correctly."""
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)

    def test_withdraw_decreases_balance(self) -> None:
        """Withdrawal reduces balance correctly."""
        self.account.withdraw(30.0)
        self.assertEqual(self.account.balance, 70.0)

    def test_deposit_invalid_raises(self) -> None:
        """Deposit of zero or negative raises ValueError."""
        with self.assertRaises(ValueError):
            self.account.deposit(0)
        with self.assertRaises(ValueError):
            self.account.deposit(-10)

    def test_withdraw_insufficient_raises(self) -> None:
        """Withdrawal exceeding balance raises ValueError."""
        with self.assertRaises(ValueError):
            self.account.withdraw(200.0)

    def test_transactions_recorded(self) -> None:
        """Deposits and withdrawals appear in transaction history."""
        self.account.deposit(50.0)
        self.account.withdraw(20.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertIn(50.0, transactions)
        self.assertIn(-20.0, transactions)

    def test_balance_is_float(self) -> None:
        """Balance is always a float."""
        self.assertIsInstance(self.account.balance, float)

    def test_multiple_operations(self) -> None:
        """Multiple operations produce correct running balance."""
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.account.deposit(25.0)
        self.assertAlmostEqual(self.account.balance, 175.0, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)