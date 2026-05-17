# Day 37 - Clean Inventory class with generator methods
# New concepts: yield, generator functions, yield from
# PEP 8, docstrings, type hints, exceptions throughout

from typing import Dict, Generator


class Inventory:
    """Manages a stock inventory. Uses generator methods to lazily yield items.

    Generator methods use yield instead of return — they produce values
    one at a time without building a full list in memory.
    """

    LOW_STOCK_THRESHOLD: int = 5

    def __init__(self) -> None:
        self._items: Dict[str, int] = {}

    def add_item(self, name: str, quantity: int) -> None:
        """Add an item to inventory. Raises ValueError if invalid."""
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self._items[name.strip()] = quantity

    def get_low_stock(
        self, threshold: int = LOW_STOCK_THRESHOLD
    ) -> Generator[str, None, None]:
        """Yield item names where quantity is below the threshold.

        This is a generator function — it yields one item at a time
        rather than building and returning a full list.
        """
        for name, qty in self._items.items():
            if qty < threshold:
                yield name

    def get_all_items(self) -> Generator[str, None, None]:
        """Yield all item names using yield from.

        yield from delegates iteration to self._items directly.
        """
        yield from self._items

    def get_all_with_quantities(self) -> Generator[tuple, None, None]:
        """Yield (name, quantity) tuples for all items."""
        for name, qty in self._items.items():
            yield name, qty

    def get_count(self) -> int:
        """Return the total number of items in inventory."""
        return len(self._items)


if __name__ == "__main__":
    try:
        inventory = Inventory()
        inventory.add_item("Apple", 3)
        inventory.add_item("Banana", 10)
        inventory.add_item("Mango", 2)
        inventory.add_item("Orange", 7)
        inventory.add_item("Grape", 1)

        print("All items (via yield from):")
        for item in inventory.get_all_items():
            print(f"  {item}")

        print(f"\nLow stock items (below {Inventory.LOW_STOCK_THRESHOLD}):")
        for item in inventory.get_low_stock():
            print(f"  {item}")

        print("\nAll items with quantities:")
        for name, qty in inventory.get_all_with_quantities():
            print(f"  {name}: {qty}")

        print("\nUsing next() on generator manually:")
        gen = inventory.get_low_stock()
        print(f"  First low stock item: {next(gen)}")
        print(f"  Second low stock item: {next(gen)}")

        print("\nUsing list() to collect all low stock at once:")
        print(f"  {list(inventory.get_low_stock())}")

    except (ValueError, StopIteration) as e:
        print(f"Error: {e}")