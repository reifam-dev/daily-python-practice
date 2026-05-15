# Day 35 - Clean Bid and Auction classes
# New concepts: __ge__, __le__, @functools.total_ordering
# PEP 8, docstrings, type hints, exceptions throughout

from __future__ import annotations
from functools import total_ordering
from typing import List, Optional


@total_ordering
class Bid:
    """Represents a single auction bid with a bidder name and amount.

    Uses @total_ordering to generate all comparison methods from
    __eq__ and __lt__ only.
    """

    def __init__(self, bidder: str, amount: float) -> None:
        if not bidder or not bidder.strip():
            raise ValueError("Bidder name cannot be empty.")
        if amount <= 0:
            raise ValueError("Bid amount must be positive.")
        self._bidder: str = bidder.strip()
        self._amount: float = amount

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"Bid(bidder='{self._bidder}', amount=£{self._amount:.2f})"

    def __repr__(self) -> str:
        """Return a developer-facing string representation."""
        return f"Bid('{self._bidder}', {self._amount})"

    def __eq__(self, other: object) -> bool:
        """Return True if both bids have the same amount."""
        if not isinstance(other, Bid):
            return NotImplemented
        return self._amount == other._amount

    def __lt__(self, other: Bid) -> bool:
        """Return True if this bid is lower than other."""
        if not isinstance(other, Bid):
            return NotImplemented
        return self._amount < other._amount

    @property
    def bidder(self) -> str:
        """Return the bidder name."""
        return self._bidder

    @property
    def amount(self) -> float:
        """Return the bid amount."""
        return self._amount


class Auction:
    """Manages an auction for a single item with multiple bids."""

    def __init__(self, item: str) -> None:
        if not item or not item.strip():
            raise ValueError("Item name cannot be empty.")
        self._item: str = item.strip()
        self._bids: List[Bid] = []

    def place_bid(self, bid: Bid) -> None:
        """Place a bid. Raises ValueError if bid is not higher than current highest."""
        if not isinstance(bid, Bid):
            raise TypeError("bid must be a Bid object.")
        if self._bids and bid <= max(self._bids):
            raise ValueError(
                f"Bid of £{bid.amount:.2f} must exceed current highest "
                f"bid of £{max(self._bids).amount:.2f}."
            )
        self._bids.append(bid)

    def get_highest_bid(self) -> Optional[Bid]:
        """Return the highest bid, or None if no bids placed."""
        if not self._bids:
            return None
        return max(self._bids)

    def get_all_bids_sorted(self) -> List[Bid]:
        """Return all bids sorted highest first."""
        return sorted(self._bids, reverse=True)

    def get_bid_count(self) -> int:
        """Return the total number of bids placed."""
        return len(self._bids)

    def get_item(self) -> str:
        """Return the auction item name."""
        return self._item


if __name__ == "__main__":
    try:
        auction = Auction("Vintage Clock")

        b1 = Bid("Alice", 100)
        b2 = Bid("Bob", 150)
        b3 = Bid("Charlie", 200)
        b4 = Bid("Diana", 175)

        auction.place_bid(b1)
        auction.place_bid(b2)
        auction.place_bid(b3)

        print(f"Item             : {auction.get_item()}")
        print(f"Total bids       : {auction.get_bid_count()}")
        print(f"Highest bid      : {auction.get_highest_bid()}")

        print(f"\nAll comparison methods from @total_ordering:")
        print(f"b1 == b2         : {b1 == b2}")    # False
        print(f"b1 < b2          : {b1 < b2}")     # True  — __lt__
        print(f"b1 <= b2         : {b1 <= b2}")    # True  — __le__ generated
        print(f"b2 > b1          : {b2 > b1}")     # True  — __gt__ generated
        print(f"b2 >= b1         : {b2 >= b1}")    # True  — __ge__ generated

        print(f"\nAll bids sorted highest first:")
        for bid in auction.get_all_bids_sorted():
            print(f"  {bid}")

        print(f"\nAttempting invalid bid:")
        auction.place_bid(b4)   # £175 < £200 — should raise ValueError

    except (ValueError, TypeError, KeyError) as e:
        print(f"Error: {e}")