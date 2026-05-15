# Day 35 - Error Finding Quiz

from functools import total_ordering

@total_ordering
class Bid:

    def __init__(self, bidder, amount):
        self.bidder = bidder
        self.amount = amount

    def __eq__(self, other):
        if not isinstance(other, Bid):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other):
        if not isinstance(other, Bid):
            return NotImplemented
        return self.amount < other.amount

    def __str__(self):
        return f"Bid({self.bidder}, £{self.amount})"


class Auction:

    def __init__(self, item):
        self.item = item
        self.bids = []

    def place_bid(self, bid):
        bids.append(bid)          # Bug 1 - missing self

    def get_highest_bid(self):
        if not self.bids:
            return None
        return max(bids)           # Bug 2 - missing self

    def get_all_bids_sorted(self):
        return sorted(self.bids, reverse=True)

    def is_valid_bid(self, bid):
        if not self.bids:
            return True
        return bid > max(self.bids)  # Bug 3 - no isinstance check on bid

auction = Auction("Vintage Clock")
b1 = Bid("Alice", 100)
b2 = Bid("Bob", 150)
auction.place_bid(b1)
auction.place_bid(b2)
print(auction.get_highest_bid())