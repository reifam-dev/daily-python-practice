# Day 18 - Error Finding Quiz

class CafeOrder:

    def __init__(self):
        self.orders = {}

    def place_order(self, item, price):
        orders[item] = price   # Bug

    def cancel_order(self, item):
        del self.orders[item]   # Bug - no check

    def get_total(self):
        return sum(self.orders.values)   # Bug

    def list_orders(self):
        return list(self.orders.keys())

order = CafeOrder()
order.place_order("Coffee", 2.50)
order.place_order("Cake", 3.00)
print(order.get_total())
print(order.list_orders())