# Day 57 - Error Finding Quiz

import itertools

# chain — flattens multiple iterables
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list(itertools.chain(list1, list2))
print(combined)

# product — cartesian product
colours = ["red", "blue"]
sizes = ["S", "M", "L"]
variants = list(itertools.product(colours, sizes))
print(len(variants))

# combinations — no repetition, order does not matter
items = ["A", "B", "C", "D"]
combos = list(itertools.combinations(items, 2))
print(len(combos))

# permutations — order matters
perms = list(itertools.permutations(items, 2))
print(len(perms))

# accumulate
import itertools
totals = list(itertools.accumulate([1, 2, 3, 4, 5]))  # correct
print(totals)

# Bug 1 - islice used incorrectly
first_five = list(itertools.islice(range(100), 5, 0))  # Bug 1 - start=5, stop=0 gives empty

# Bug 2
grouped = itertools.groupby([1, 1, 2, 2, 3], key=lambda x: x)
for key, group in grouped:
    print(key, list(group))
    print(key, list(group))   # Bug 2 - group iterator already exhausted

# Bug 3
cycle_iter = itertools.cycle([1, 2, 3])
first_ten = list(cycle_iter)   # Bug 3 - infinite iterator, never terminates