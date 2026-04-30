# Day 20 - Clean Library class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict


class Library:
    """Manages a library catalogue with borrowing and returning of books."""

    def __init__(self) -> None:
        self._books: Dict[str, int] = {}

    def add_book(self, title: str, copies: int) -> None:
        """Add a book with a number of copies. Raises ValueError if invalid."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        if copies <= 0:
            raise ValueError("Copies must be a positive integer.")
        if title.strip() in self._books:
            self._books[title.strip()] += copies
        else:
            self._books[title.strip()] = copies

    def borrow_book(self, title: str) -> None:
        """Borrow a copy. Raises KeyError if not found, ValueError if unavailable."""
        if title not in self._books:
            raise KeyError(f"'{title}' is not in the library.")
        if self._books[title] == 0:
            raise ValueError(f"No copies of '{title}' are available.")
        self._books[title] -= 1

    def return_book(self, title: str) -> None:
        """Return a copy. Raises KeyError if title not recognised."""
        if title not in self._books:
            raise KeyError(f"'{title}' is not recognised in this library.")
        self._books[title] += 1

    def is_available(self, title: str) -> bool:
        """Return True if at least one copy is available."""
        return self._books.get(title, 0) > 0

    def get_copies(self, title: str) -> int:
        """Return the number of available copies."""
        return self._books.get(title, 0)


if __name__ == "__main__":
    try:
        library = Library()
        library.add_book("1984", 3)
        library.add_book("Clean Code", 2)
        library.add_book("The Pragmatic Programmer", 1)

        print(f"1984 available      : {library.is_available('1984')}")
        print(f"1984 copies         : {library.get_copies('1984')}")

        library.borrow_book("1984")
        library.borrow_book("1984")
        print(f"After 2 borrows     : {library.get_copies('1984')} copies left")

        library.return_book("1984")
        print(f"After 1 return      : {library.get_copies('1984')} copies left")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")