# Day 19 - Error Finding Quiz

class FruitShop:

    def __init__(self):
        self.stock = {}

    def add_fruit(self, name, price):
        stock[name] = price   # Bug 1

    def get_price(self, name):
        if name in self.stock:
            return self.stock[name]

    def is_in_stock(self, name):
        return name in self.stock

    def remove_fruit(self, name):
        del self.stock[name]   # Bug 2 - no check

shop = FruitShop()
shop.add_fruit("Apple", 0.50)
shop.add_fruit("Banana", 0.30)
print(shop.get_price("Apple"))
print(shop.is_in_stock("Mango"))