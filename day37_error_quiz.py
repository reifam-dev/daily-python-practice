# Day 37 - Error Finding Quiz

class Inventory:

    def __init__(self):
        self.items = {}

    def add_item(self, name, quantity):
        items[name] = quantity         # Bug 1 - missing self

    def get_low_stock(self, threshold=5):
        for name, qty in self.items.items():
            if qty < threshold
                yield name             # Bug 2 - missing colon on if

    def get_all_items(self):
        yield from items               # Bug 3 - missing self.items


inventory = Inventory()
inventory.add_item("Apple", 3)
inventory.add_item("Banana", 10)
inventory.add_item("Mango", 2)

for item in inventory.get_low_stock():
    print(item)