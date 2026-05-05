# Day 25 - Clean StockInventory class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict, List


class StockInventory:
    """Manages a stock inventory with quantities and low stock detection."""

    LOW_STOCK_THRESHOLD: int = 5

    def __init__(self) -> None:
        self._stock: Dict[str, int] = {}

    def add_item(self, name: str, quantity: int) -> None:
        """Add a new item to inventory. Raises ValueError if already exists or invalid."""
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if name.strip() in self._stock:
            raise ValueError(f"'{name}' already exists. Use restock_item() to add stock.")
        self._stock[name.strip()] = quantity

    def sell_item(self, name: str, quantity: int) -> None:
        """Sell a quantity of an item. Raises KeyError if not found, ValueError if insufficient stock."""
        if name not in self._stock:
            raise KeyError(f"'{name}' is not in inventory.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if self._stock[name] < quantity:
            raise ValueError(f"Insufficient stock for '{name}'. Available: {self._stock[name]}.")
        self._stock[name] -= quantity

    def restock_item(self, name: str, quantity: int) -> None:
        """Add stock to an existing item. Raises KeyError if item not found."""
        if name not in self._stock:
            raise KeyError(f"'{name}' is not in inventory.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        self._stock[name] += quantity

    def is_low_stock(self, name: str) -> bool:
        """Return True if item stock is below the low stock threshold."""
        return self._stock.get(name, 0) < self.LOW_STOCK_THRESHOLD

    def get_low_stock_items(self) -> List[str]:
        """Return a list of all items currently below the low stock threshold."""
        return [name for name, qty in self._stock.items()
                if qty < self.LOW_STOCK_THRESHOLD]

    def get_quantity(self, name: str) -> int:
        """Return the current quantity of an item."""
        return self._stock.get(name, 0)


if __name__ == "__main__":
    try:
        inventory = StockInventory()
        inventory.add_item("Apples", 20)
        inventory.add_item("Bananas", 3)
        inventory.add_item("Oranges", 8)

        print(f"Apples quantity  : {inventory.get_quantity('Apples')}")
        print(f"Low stock items  : {inventory.get_low_stock_items()}")

        inventory.sell_item("Apples", 17)
        print(f"After selling 17 Apples : {inventory.get_quantity('Apples')} left")
        print(f"Low stock items         : {inventory.get_low_stock_items()}")

        inventory.restock_item("Bananas", 10)
        print(f"After restocking Bananas: {inventory.get_quantity('Bananas')} total")
        print(f"Low stock items         : {inventory.get_low_stock_items()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")