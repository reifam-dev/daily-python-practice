# Day 12 - Error Finding Quiz

class ShoppingBasket:

    def __init__(self)
        self.items = {}

    def add_item(self, name, price):
        items[name] = price   # Bug

    def remove_item(self, name):
        del self.items[name]   # No check if item exists

    def get_total(self):
        return sum(self.items.values())

basket = ShoppingBasket()
basket.add_item("apple", 0.50)
basket.add_item("bread", 1.20)
print(basket.get_total())