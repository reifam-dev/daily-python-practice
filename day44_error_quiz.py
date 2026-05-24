# Day 44 - Error Finding Quiz

from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSort(SortStrategy):
    def sort(self, data):
        lst = data.copy()
        n = len(lst)
        for i in range(n):
            for j in range(n - i - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst

class SelectionSort(SortStrategy):
    def sort(self, data):
        lst = data.copy()
        n = len(lst)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lst[j] < lst[min_idx]:
                    min_idx = j
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
        return lst

class Sorter:

    def __init__(self, strategy):
        self.strategy = strategy

    def sort(self, data):
        return strategy.sort(data)   # Bug 1 - missing self

    def set_strategy(self, strategy):
        self.strategy == strategy    # Bug 2 - comparison not assignment

data = [5, 3, 8, 1, 9, 2]
sorter = Sorter(BubbleSort)          # Bug 3 - should be BubbleSort() not BubbleSort
print(sorter.sort(data))