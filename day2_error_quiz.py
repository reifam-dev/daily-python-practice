# Day 2 - Error Finding Quiz (Fix inheritance issues)

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

class SavingsAccount(BankAccount):
    def __init__(self, balance, interest_rate):
        self.interest_rate = interest_rate   # Missing super()

    def add_interest(self):
        self.balance += self.balance * interest_rate   # NameError + logic issue

acc = SavingsAccount(100, 0.05)
acc.deposit(50)
acc.add_interest()
print(acc.balance)