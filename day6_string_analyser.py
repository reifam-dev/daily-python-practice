# Day 6 - Clean StringAnalyzer class (PEP 8, docstrings, type hints, exceptions)

from typing import List

class StringAnalyzer:
    """Analyzes basic properties of a string."""

    def __init__(self, text: str):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        self._text = text.strip()

    def count_words(self) -> int:
        """Return the number of words in the text."""
        if not self._text:
            return 0
        return len(self._text.split())

    def count_vowels(self) -> int:
        """Return the number of vowels (a/e/i/o/u) in the text."""
        vowels = set("aeiouAEIOU")
        return sum(1 for char in self._text if char in vowels)

    def get_length(self) -> int:
        """Return the length of the original text."""
        return len(self._text)


if __name__ == "__main__":
    try:
        analyzer = StringAnalyzer("Hello World Python")
        print(f"Words   : {analyzer.count_words()}")
        print(f"Vowels  : {analyzer.count_vowels()}")
        print(f"Length  : {analyzer.get_length()}")
    except Exception as e:
        print(f"Error: {e}")