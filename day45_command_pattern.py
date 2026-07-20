# Day 45 - Clean Command pattern
# New concepts: Command design pattern, undo/redo, command history
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """Abstract base class for all commands.

    Every command must implement execute() and undo().
    """

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""
        pass


class BankAccount:
    """A simple bank account used as the receiver in the Command pattern."""

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self._owner = owner
        self._balance = balance

    def deposit(self, amount: float) -> None:
        """Deposit funds."""
        self._balance += amount
        print(f"  Deposited £{amount:.2f} — balance: £{self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        """Withdraw funds. Raises ValueError if insufficient."""
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Balance: £{self._balance:.2f}."
            )
        self._balance -= amount
        print(f"  Withdrew £{amount:.2f} — balance: £{self._balance:.2f}")

    @property
    def balance(self) -> float:
        """Return the current balance."""
        return self._balance

    def __str__(self) -> str:
        return f"BankAccount('{self._owner}', £{self._balance:.2f})"


class DepositCommand(Command):
    """Command to deposit funds into an account."""

    def __init__(self, account: BankAccount, amount: float) -> None:
        self._account = account
        self._amount = amount

    def execute(self) -> None:
        self._account.deposit(self._amount)

    def undo(self) -> None:
        self._account.withdraw(self._amount)


class WithdrawCommand(Command):
    """Command to withdraw funds from an account."""

    def __init__(self, account: BankAccount, amount: float) -> None:
        self._account = account
        self._amount = amount

    def execute(self) -> None:
        self._account.withdraw(self._amount)

    def undo(self) -> None:
        self._account.deposit(self._amount)


class CommandProcessor:
    """Executes commands and maintains a history for undo support.

    Demonstrates the Command pattern — requests are objects
    that can be stored, queued and reversed.
    """

    def __init__(self) -> None:
        self._history: List[Command] = []

    def execute(self, command: Command) -> None:
        """Execute a command and add it to history."""
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        """Undo the most recent command."""
        if not self._history:
            print("  Nothing to undo.")
            return
        command = self._history.pop()
        command.undo()

    def get_history_count(self) -> int:
        """Return the number of commands in history."""
        return len(self._history)


if __name__ == "__main__":
    try:
        acc = BankAccount("Alice", 100.0)
        processor = CommandProcessor()

        print(f"Initial: {acc}\n")

        print("=== Executing commands ===\n")
        processor.execute(DepositCommand(acc, 50))
        processor.execute(DepositCommand(acc, 25))
        processor.execute(WithdrawCommand(acc, 30))

        print(f"\nBalance after commands : £{acc.balance:.2f}")
        print(f"Commands in history   : {processor.get_history_count()}\n")

        print("=== Undoing last command ===\n")
        processor.undo_last()
        print(f"\nBalance after undo    : £{acc.balance:.2f}")

        print("\n=== Undoing all remaining ===\n")
        processor.undo_last()
        processor.undo_last()
        processor.undo_last()   # Nothing to undo

        print(f"\nFinal balance         : £{acc.balance:.2f}")

    except ValueError as e:
        print(f"Error: {e}")