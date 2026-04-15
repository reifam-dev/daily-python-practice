# Day 5 - Error Finding Quiz (PEP 8 + exceptions)

class NumberStats:
    def __init__(self, numbers)
        self.numbers = numbers

    def get_sum(self):
        total = 0
        for n in self.numbers
            total = total + n
        return total

    def get_average(self):
        return self.get_sum() / len(numbers)   # Bug

stats = NumberStats([10, 20, 30, 40])
print(stats.get_sum())
print(stats.get_average())