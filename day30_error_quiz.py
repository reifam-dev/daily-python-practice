# Day 30 - Error Finding Quiz

class BankAccount:

    def __init__(self, account_id, owner, balance=0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance =- amount         # Bug 1 - wrong operator


class Bank:

    def __init__(self):
        self.accounts = {}

    def create_account(self, account_id, owner):
        if account_id in self.accounts:
            raise ValueError("Account already exists.")
        accounts[account_id] = BankAccount(account_id, owner)  # Bug 2 - missing self

    def transfer(self, from_id, to_id, amount):
        self.accounts[from_id].withdraw(amount)   # Bug 3 - no check if accounts exist
        self.accounts[to_id].deposit(amount)

    def get_balance(self, account_id):
        return self.accounts[account_id].balance

bank = Bank()
bank.create_account(1, "Alice")
bank.create_account(2, "Bob")
bank.accounts[1].deposit(500)
bank.transfer(1, 2, 200)
print(bank.get_balance(1))
print(bank.get_balance(2))