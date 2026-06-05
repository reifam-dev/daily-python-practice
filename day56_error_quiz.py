# Day 56 - Error Finding Quiz

from collections import defaultdict, Counter, deque

# defaultdict
word_count = defaultdict(int)
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
for word in words:
    word_count[word] =+ 1    # Bug 1 - wrong operator, should be +=

# Counter
letters = Counter("mississippi")
print(letters.most_common(3))
print(letters["z"])           # correct - returns 0 for missing key

# deque
queue = deque(maxlen=3)
queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)               # correct - maxlen pushes out oldest
print(queue)

history = deque()
history.appendleft("page1")
history.appendleft("page2")
history.appendleft("page3")
print(history.pop)            # Bug 2 - missing ()

inventory = defaultdict(list)
inventory["fruits"].append("apple")
inventory["fruits"].append("banana")
inventory["vegs"].append("carrot")
print(inventory["dairy"])     # Bug 3 - not a bug, returns [] — but is this expected?
print(inventory["dairy"])     # This silently creates the key — worth knowing