# Day 47 - Error Finding Quiz

from abc import ABC, abstractmethod

class FileSystemItem(ABC):
    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def display(self, indent=0):
        pass

class File(FileSystemItem):

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

    def display(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self.size} KB)")


class Folder(FileSystemItem):

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, item):
        children.append(item)    # Bug 1 - missing self

    def remove(self, item):
        self.children.remove(item)

    def get_size(self):
        return sum(child.get_size for child in self.children)  # Bug 2 - missing ()

    def display(self, indent=0):
        print(" " * indent + f"📁 {self.name}")
        for child in children:   # Bug 3 - missing self
            child.display(indent + 2)


root = Folder("root")
docs = Folder("documents")
file1 = File("report.pdf", 500)
file2 = File("photo.jpg", 2000)
docs.add(file1)
root.add(docs)
root.add(file2)
root.display()
print(root.get_size())