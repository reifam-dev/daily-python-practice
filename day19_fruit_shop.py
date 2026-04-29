# Day 19 - Clean FruitShop class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict, Optional


class FruitShop:
    """Manages a fruit shop stock with names and prices."""

    def __init__(self) -> None:
        self._stock: Dict[str, float] = {}

    def add_fruit(self, name: str, price: float) -> None:
        """Add a fruit to stock. Raises ValueError if already exists or invalid."""
        if not name or not name.strip():
            raise ValueError("Fruit name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if name.strip() in self._stock:
            raise ValueError(f"'{name}' is already in stock.")
        self._stock[name.strip()] = price

    def remove_fruit(self, name: str) -> None:
        """Remove a fruit from stock. Raises KeyError if not found."""
        if name not in self._stock:
            raise KeyError(f"'{name}' is not in stock.")
        del self._stock[name]

    def get_price(self, name: str) -> Optional[float]:
        """Return the price of a fruit, or None if not found."""
        return self._stock.get(name)

    def is_in_stock(self, name: str) -> bool:
        """Return True if the fruit is in stock."""
        return name in self._stock

    def get_all_stock(self) -> Dict[str, float]:
        """Return a copy of all stock."""
        return self._stock.copy()


if __name__ == "__main__":
    try:
        shop = FruitShop()
        shop.add_fruit("Apple", 0.50)
        shop.add_fruit("Banana", 0.30)
        shop.add_fruit("Mango", 1.20)

        print(f"All stock        : {shop.get_all_stock()}")
        print(f"Apple price      : £{shop.get_price('Apple'):.2f}")
        print(f"Mango in stock   : {shop.is_in_stock('Mango')}")
        print(f"Grape in stock   : {shop.is_in_stock('Grape')}")

        shop.remove_fruit("Banana")
        print(f"After removing Banana: {shop.get_all_stock()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")