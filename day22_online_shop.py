# Day 33 - Clean Item and ShoppingCart classes
# New concepts: __len__, __contains__
# PEP 8, docstrings, type hints, exceptions throughout

from typing import List


class Item:
    """Represents a shop item with a name and price."""

    def __init__(self, name: str, price: float) -> None:
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self._name: str = name.strip()
        self._price: float = price

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self._name} £{self._price:.2f}"

    def __repr__(self) -> str:
        """Return a developer-facing string representation."""
        return f"Item(name='{self._name}', price={self._price})"

    @property
    def name(self) -> str:
        """Return the item name."""
        return self._name

    @property
    def price(self) -> float:
        """Return the item price."""
        return self._price


class ShoppingCart:
    """Manages a shopping cart of Item objects.
    Supports len() and the in operator via __len__ and __contains__.
    """

    def __init__(self) -> None:
        self._items: List[Item] = []

    def __len__(self) -> int:
        """Return the number of items in the cart. Enables len(cart)."""
        return len(self._items)

    def __contains__(self, item: Item) -> bool:
        """Return True if the item is in the cart. Enables 'item in cart'."""
        return item in self._items

    def add_item(self, item: Item) -> None:
        """Add an item to the cart."""
        self._items.append(item)

    def remove_item(self, item: Item) -> None:
        """Remove an item from the cart. Raises KeyError if not found."""
        if item not in self._items:
            raise KeyError(f"'{item.name}' is not in the cart.")
        self._items.remove(item)

    def get_total(self) -> float:
        """Return the total price of all items in the cart."""
        return sum(item.price for item in self._items)

    def get_all_items(self) -> List[Item]:
        """Return a copy of all items in the cart."""
        return self._items.copy()


if __name__ == "__main__":
    try:
        cart = ShoppingCart()

        apple = Item("Apple", 0.50)
        bread = Item("Bread", 1.20)
        milk = Item("Milk", 0.90)

        cart.add_item(apple)
        cart.add_item(bread)
        cart.add_item(milk)

        print(f"Items in cart    : {len(cart)}")
        print(f"Apple in cart    : {apple in cart}")
        print(f"Total            : £{cart.get_total():.2f}")

        print("\nAll items:")
        for item in cart.get_all_items():
            print(f"  {item}")

        cart.remove_item(bread)
        print(f"\nAfter removing Bread:")
        print(f"Items in cart    : {len(cart)}")
        print(f"Total            : £{cart.get_total():.2f}")
        print(f"Bread in cart    : {bread in cart}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")