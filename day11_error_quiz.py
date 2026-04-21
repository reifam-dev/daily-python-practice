# Day 11 - Error Finding Quiz

class ListManager:
    def __init__(self)
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)   # No check if item exists

    def contains(self, item):
        return item in items   # Bug

    def size(self):
        return len(self.items)

manager = ListManager()
manager.add_item("apple")
manager.add_item("banana")
print(manager.contains("apple"))
print(manager.size())