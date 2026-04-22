Day 12 - Clean ShoppingBasket class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict


class ShoppingBasket:
    """Manages a simple shopping basket with item prices."""

    def __init__(self) -> None:
        self._items: Dict[str, float] = {}

    def add_item(self, name: str, price: float) -> None:
        """Add an item with its price. Overwrites if item already exists."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Item name must be a non-empty string.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self._items[name.strip()] = price

    def remove_item(self, name: str) -> bool:
        """Remove an item by name. Returns True if removed, False if not found."""
        if name in self._items:
            del self._items[name]
            return True
        return False

    def get_total(self) -> float:
        """Return the total price of all items in the basket."""
        return sum(self._items.values())

    def list_items(self) -> Dict[str, float]:
        """Return a copy of all items and their prices."""
        return self._items.copy()


if __name__ == "__main__":
    try:
        basket = ShoppingBasket()
        basket.add_item("apple", 0.50)
        basket.add_item("bread", 1.20)
        basket.add_item("milk", 0.90)

        print(f"Items  : {basket.list_items()}")
        print(f"Total  : £{basket.get_total():.2f}")

        basket.remove_item("bread")
        print(f"After removing bread: £{basket.get_total():.2f}")

    except (ValueError, TypeError) as e:
        print(f"Error: {e}")