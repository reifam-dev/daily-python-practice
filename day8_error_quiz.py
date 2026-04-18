# Day 8 - Error Finding Quiz

class NumberProcessor:
    def __init__(self, numbers)
        self.numbers = numbers

    def get_max(self):
        return max(numbers)   # Bug

    def get_min(self):
        return min(self.numbers)

    def get_sum(self):
        total = 0
        for n in self.numbers
            total += n
        return total

processor = NumberProcessor([10, 5, 8, 12, 3])
print(processor.get_max())
print(processor.get_min())
print(processor.get_sum())