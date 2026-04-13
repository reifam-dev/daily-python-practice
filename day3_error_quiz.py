# Day 3 - Error Finding Quiz (Fix polymorphism issues)

class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount

class CheckingAccount(Account):
    def withdraw(self, amount):
        self.balance -= amount + 1   # Fee, but missing super() and validation

class SavingsAccount(Account):
    def withdraw(self, amount):
        print("Savings cannot be withdrawn")   # Wrong logic

acc1 = CheckingAccount(100)
acc1.withdraw(30)
acc2 = SavingsAccount(200)
acc2.withdraw(50)
print(acc1.balance, acc2.balance)