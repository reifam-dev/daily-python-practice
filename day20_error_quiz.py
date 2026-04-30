# Day 20 - Error Finding Quiz

class Library:

    def __init__(self):
        self.books = {}

    def add_book(self, title, copies):
        books[title] = copies   # Bug 1

    def borrow_book(self, title):
        if self.books[title] > 0:   # Bug 2 - no check if title exists
            self.books[title] -= 1

    def return_book(self, title):
        if title in self.books:
            self.books[title] =+ 1   # Bug 3 - wrong operator

    def is_available(self, title):
        return self.books.get(title, 0) > 0

library = Library()
library.add_book("1984", 3)
library.borrow_book("1984")
print(library.is_available("1984"))