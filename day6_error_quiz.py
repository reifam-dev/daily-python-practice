# Day 6 - Error Finding Quiz (PEP 8 + exceptions)

class StringAnalyzer:
    def __init__(self, text)
        self.text = text

    def count_words(self):
        words = self.text.split()
        return len(words)

    def count_vowels(self):
        vowels = "aeiouAEIOU"
        count = 0
        for char in text:          # Bug
            if char in vowels:
                count += 1
        return count

analyzer = StringAnalyzer("Hello World")
print(analyzer.count_words())
print(analyzer.count_vowels())