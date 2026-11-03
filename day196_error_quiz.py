"""Day 196 - Percentiles (p50, p95, p99): Error Quiz. Find and fix three bugs."""


def percentile(values: list, p: float) -> float:
    values.sort()
    index = int(len(values) * p / 100)
    return values[index]


if __name__ == "__main__":
    latencies_ms = [120, 95, 180, 110, 3000, 105, 130, 99, 101, 115]
    print(percentile(latencies_ms, 50))
    print(latencies_ms)
    print(percentile(latencies_ms, 95))
    print(percentile(latencies_ms, 100))