# Day 14 - Error Finding Quiz

class BookTracker:

    def __init__(self)
        self.books = {}

    def add_book(self, title, author):
        books[title] = {"author": author, "read": False}   # Bug

    def mark_as_read(self, title):
        if title in self.books:
            self.books[title]["read"] = True

    def get_unread(self):
        return [t for t, b in self.books.items() if b["read"] == False]

tracker = BookTracker()
tracker.add_book("1984", "Orwell")
tracker.mark_as_read("1984")
print(tracker.get_unread())