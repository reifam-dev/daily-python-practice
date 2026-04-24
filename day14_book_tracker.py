# Day 14 - Clean BookTracker class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict, List


class BookTracker:
    """Tracks books and their read/unread status."""

    def __init__(self) -> None:
        self._books: Dict[str, Dict] = {}

    def add_book(self, title: str, author: str) -> None:
        """Add a new book. Raises ValueError if title already exists."""
        if not title or not author:
            raise ValueError("Title and author cannot be empty.")
        if title in self._books:
            raise ValueError(f"'{title}' is already in the tracker.")
        self._books[title] = {"author": author, "read": False}

    def mark_as_read(self, title: str) -> None:
        """Mark a book as read. Raises KeyError if title not found."""
        if title not in self._books:
            raise KeyError(f"'{title}' not found in tracker.")
        self._books[title]["read"] = True

    def get_unread(self) -> List[str]:
        """Return a list of unread book titles."""
        return [t for t, b in self._books.items() if not b["read"]]

    def get_all(self) -> Dict[str, Dict]:
        """Return a copy of all tracked books."""
        return self._books.copy()


if __name__ == "__main__":
    try:
        tracker = BookTracker()
        tracker.add_book("1984", "George Orwell")
        tracker.add_book("Clean Code", "Robert Martin")
        tracker.add_book("The Pragmatic Programmer", "Hunt & Thomas")

        tracker.mark_as_read("1984")

        print(f"All books : {list(tracker.get_all().keys())}")
        print(f"Unread    : {tracker.get_unread()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")
