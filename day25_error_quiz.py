# Day 25 - Error Finding Quiz

class StockInventory:

    def __init__(self):
        self.stock = {}

    def add_item(self, name, quantity):
        stock[name] = quantity      # Bug 1 - missing self

    def sell_item(self, name, quantity):
        if name in self.stock:
            self.stock[name] =- quantity   # Bug 2 - wrong operator
        else:
            print("Item not found.")

    def restock_item(self, name, quantity):
        if name in self.stock:
            self.stock[name] += quantity

    def is_low_stock(self, name, threshold=5):
        return self.stock.get(name, 0) < threshold

inventory = StockInventory()
inventory.add_item("Apples", 20)
inventory.sell_item("Apples", 5)
print(inventory.is_low_stock("Apples"))