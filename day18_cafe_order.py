# Day 18 - Clean CafeOrder class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict, List


class CafeOrder:
    """Manages a café order with items and prices."""

    def __init__(self) -> None:
        self._orders: Dict[str, float] = {}

    def place_order(self, item: str, price: float) -> None:
        """Add an item to the order. Raises ValueError if item already ordered."""
        if not item or not item.strip():
            raise ValueError("Item name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if item.strip() in self._orders:
            raise ValueError(f"'{item}' is already in the order.")
        self._orders[item.strip()] = price

    def cancel_order(self, item: str) -> None:
        """Remove an item from the order. Raises KeyError if not found."""
        if item not in self._orders:
            raise KeyError(f"'{item}' is not in the order.")
        del self._orders[item]

    def get_total(self) -> float:
        """Return the total price of all ordered items."""
        return sum(self._orders.values())

    def list_orders(self) -> List[str]:
        """Return a list of all ordered item names."""
        return list(self._orders.keys())

    def get_item_count(self) -> int:
        """Return the number of items in the order."""
        return len(self._orders)


if __name__ == "__main__":
    try:
        order = CafeOrder()
        order.place_order("Coffee", 2.50)
        order.place_order("Cake", 3.00)
        order.place_order("Orange Juice", 2.00)

        print(f"Orders     : {order.list_orders()}")
        print(f"Items      : {order.get_item_count()}")
        print(f"Total      : £{order.get_total():.2f}")

        order.cancel_order("Cake")
        print(f"After cancelling Cake: £{order.get_total():.2f}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")