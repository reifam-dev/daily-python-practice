# Day 33 - Error Finding Quiz

class ShoppingCart:

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)    # Bug 1 - no check

    def __len__(self):
        return len(items)          # Bug 2 - missing self

    def __contains__(self, item):
        return item in self.items

    def get_total(self):
        return sum(i.price for i in self.items)


class Item:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} £{self.price:.2f}"

    def __repr__(self):
        return f"Item('{self.name}', {self.price})"


cart = ShoppingCart()
apple = Item("Apple", 0.50)
bread = Item("Bread", 1.20)
cart.add_item(apple)
cart.add_item(bread)
print(len(cart))               # Uses __len__
print(apple in cart)           # Uses __contains__ - Bug 3 - will fail as items are objects