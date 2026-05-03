# Day 23 - Error Finding Quiz

class ScoreTracker:

    def __init__(self):
        self.scores = []

    def add_score(self, score):
        if score < 0:
            print("Score cannot be negative.")
        self.scores.append(score)   # Bug 1 - missing else

    def get_highest(self):
        return max(scores)          # Bug 2 - missing self

    def get_lowest(self):
        return min(self.scores)

    def get_average(self):
        return sum(self.scores) / len(self.scores)  # Bug 3 - no empty list check

    def reset(self):
        self.scores = []

tracker = ScoreTracker()
tracker.add_score(85)
tracker.add_score(92)
tracker.add_score(78)
print(tracker.get_highest())
print(tracker.get_average())