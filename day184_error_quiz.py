"""Day 184 - Interval Merging: Error Quiz. Find and fix three bugs."""


def merge_intervals(intervals: list) -> list:
    merged = []
    for start, end in intervals:
        if merged and start < merged[-1][1]:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged


if __name__ == "__main__":
    leases = [(24, 36), (0, 12), (6, 18), (36, 48), (30, 32)]
    merged = merge_intervals(leases)
    print(merged)
    print(sum(end - start for start, end in merged))