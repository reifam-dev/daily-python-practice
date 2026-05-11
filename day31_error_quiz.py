# Day 31 - Error Finding Quiz

class Product:

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Product({self.name}, £{self.price}, {self.category})"

    @classmethod
    def from_string(cls, product_string):
        # Expects format: "name,price,category"
        parts = product_string.split(",")
        return cls(parts[0], parts[1], parts[2])  # Bug 1 - price not converted to float

    def apply_discount(self, percentage):
        if percentage <= 0 or percentage >= 100:
            raise ValueError("Discount must be between 0 and 100.")
        self.price =- self.price * (percentage / 100)  # Bug 2 - wrong operator

class ProductCatalogue:

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.name] = product

    def get_product(self, name):
        return self.products[name]         # Bug 3 - no check, no .copy()

    def get_count(self):
        return len(self.products)

catalogue = ProductCatalogue()
p = Product.from_string("Apple,0.50,Fruit")
catalogue.add_product(p)
print(catalogue.get_product("Apple"))