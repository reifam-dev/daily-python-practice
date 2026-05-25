# Day 45 - Error Finding Quiz

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class DepositCommand(Command):

    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def execute(self):
        account.deposit(self.amount)   # Bug 1 - missing self

    def undo(self):
        self.account.withdraw(self.amount)


class WithdrawCommand(Command):

    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def execute(self):
        self.account.withdraw(self.amount)

    def undo(self):
        self.account.deposit(self.amount)


class CommandProcessor:

    def __init__(self):
        self.history = []

    def execute(self, command):
        command.execute()
        history.append(command)        # Bug 2 - missing self

    def undo_last(self):
        if not self.history:
            print("Nothing to undo.")
            return
        command = self.history.pop
        command.undo()                 # Bug 3 - missing () on pop


class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        self.balance -= amount

acc = BankAccount(100)
processor = CommandProcessor()
processor.execute(DepositCommand(acc, 50))
print(acc.balance)
processor.undo_last()
print(acc.balance)