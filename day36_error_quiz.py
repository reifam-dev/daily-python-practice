# Day 36 - Error Finding Quiz

class CountDown:

    def __init__(self, start):
        self.start = start
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current =- 1        # Bug 1 - wrong operator, should be -= 1
        return value


class NumberRange:

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = current           # Bug 2 - missing self
        self.current += 1
        return value

    def reset(self):
        current = self.start      # Bug 3 - missing self


cd = CountDown(3)
for n in cd:
    print(n)