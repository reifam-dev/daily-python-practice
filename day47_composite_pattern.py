# Day 47 - Clean Composite pattern — file system tree
# New concepts: Composite pattern, recursive tree structures, uniform interface
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List


class FileSystemItem(ABC):
    """Abstract component — both File (leaf) and Folder (composite) implement this.

    Treating leaves and composites uniformly is the core of the Composite pattern.
    """

    @abstractmethod
    def get_size(self) -> int:
        """Return the size of this item in KB."""
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        """Display this item with indentation."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this item."""
        pass


class File(FileSystemItem):
    """Leaf node — has no children. Represents a single file."""

    def __init__(self, name: str, size: int) -> None:
        if not name or not name.strip():
            raise ValueError("File name cannot be empty.")
        if size < 0:
            raise ValueError("File size cannot be negative.")
        self._name = name.strip()
        self._size = size

    @property
    def name(self) -> str:
        return self._name

    def get_size(self) -> int:
        """Return the file size in KB."""
        return self._size

    def display(self, indent: int = 0) -> None:
        """Display the file with indentation."""
        print(" " * indent + f"File: {self._name} ({self._size} KB)")


class Folder(FileSystemItem):
    """Composite node — can contain Files and other Folders recursively."""

    def __init__(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("Folder name cannot be empty.")
        self._name = name.strip()
        self._children: List[FileSystemItem] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, item: FileSystemItem) -> None:
        """Add a child item to this folder."""
        self._children.append(item)

    def remove(self, item: FileSystemItem) -> None:
        """Remove a child item. Raises KeyError if not found."""
        if item not in self._children:
            raise KeyError(f"'{item.name}' not found in '{self._name}'.")
        self._children.remove(item)

    def get_size(self) -> int:
        """Return total size by recursively summing all children."""
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> None:
        """Display folder and all children recursively."""
        print(" " * indent + f"Folder: {self._name}/ ({self.get_size()} KB)")
        for child in self._children:
            child.display(indent + 4)

    def get_child_count(self) -> int:
        """Return the number of direct children."""
        return len(self._children)


if __name__ == "__main__":
    try:
        root = Folder("root")
        docs = Folder("documents")
        images = Folder("images")

        docs.add(File("report.pdf", 500))
        docs.add(File("notes.txt", 20))
        images.add(File("photo.jpg", 2000))
        images.add(File("logo.png", 150))
        root.add(docs)
        root.add(images)
        root.add(File("readme.txt", 5))

        print("=== File System Tree ===\n")
        root.display()

        print(f"\nTotal size       : {root.get_size()} KB")
        print(f"Root children    : {root.get_child_count()}")
        print(f"Docs size        : {docs.get_size()} KB")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")