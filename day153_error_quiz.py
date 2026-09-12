"""Day 153 - Binary Search: Error Quiz. Find and fix three bugs."""
def binary_search(sorted_list: list, target) -> int:
    low, high = 0, len(sorted_list)

    while low < high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            low = mid
        else:
            high = mid

    return -1


if __name__ == "__main__":
    deals = [10, 20, 30, 40, 50, 60, 70]
    print(binary_search(deals, 40))
    print(binary_search(deals, 25))