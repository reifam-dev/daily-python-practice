# Day 31 - Clean Product and ProductCatalogue classes
# New concepts: __str__, @classmethod as alternative constructor
# PEP 8, docstrings, type hints, exceptions throughout

from typing import Dict, Optional


class Product:
    """Represents a product with a name, price and category."""

    def __init__(self, name: str, price: float, category: str) -> None:
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self._name: str = name.strip()
        self._price: float = price
        self._category: str = category.strip()

    def __str__(self) -> str:
        """Return a readable string representation of the product."""
        return f"Product(name='{self._name}', price=£{self._price:.2f}, category='{self._category}')"

    @classmethod
    def from_string(cls, product_string: str) -> "Product":
        """Alternative constructor. Creates a Product from a 'name,price,category' string."""
        parts = product_string.split(",")
        if len(parts) != 3:
            raise ValueError("String must be in format 'name,price,category'.")
        return cls(parts[0].strip(), float(parts[1].strip()), parts[2].strip())

    @property
    def name(self) -> str:
        """Return the product name."""
        return self._name

    @property
    def price(self) -> float:
        """Return the product price."""
        return self._price

    @property
    def category(self) -> str:
        """Return the product category."""
        return self._category

    def apply_discount(self, percentage: float) -> None:
        """Apply a percentage discount to the price."""
        if percentage <= 0 or percentage >= 100:
            raise ValueError("Discount must be between 0 and 100.")
        self._price -= self._price * (percentage / 100)


class ProductCatalogue:
    """Manages a catalogue of Product objects. Demonstrates composition."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """Add a product. Raises ValueError if product name already exists."""
        if product.name in self._products:
            raise ValueError(f"'{product.name}' is already in the catalogue.")
        self._products[product.name] = product

    def get_product(self, name: str) -> Optional[Product]:
        """Return a product by name, or None if not found."""
        return self._products.get(name)

    def remove_product(self, name: str) -> None:
        """Remove a product. Raises KeyError if not found."""
        if name not in self._products:
            raise KeyError(f"'{name}' not found in catalogue.")
        del self._products[name]

    def get_count(self) -> int:
        """Return the total number of products."""
        return len(self._products)


if __name__ == "__main__":
    try:
        catalogue = ProductCatalogue()

        p1 = Product("Apple", 0.50, "Fruit")
        p2 = Product.from_string("Banana,0.30,Fruit")
        p3 = Product.from_string("Laptop,999.99,Electronics")

        catalogue.add_product(p1)
        catalogue.add_product(p2)
        catalogue.add_product(p3)

        print(f"Catalogue count  : {catalogue.get_count()}")
        print(catalogue.get_product("Apple"))
        print(catalogue.get_product("Laptop"))

        p1.apply_discount(10)
        print(f"Apple after 10% discount: {catalogue.get_product('Apple')}")

        catalogue.remove_product("Banana")
        print(f"After removing Banana: {catalogue.get_count()} products")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")