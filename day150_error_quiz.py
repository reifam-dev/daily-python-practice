"""Day 150 - Cursor-Based Pagination: Error Quiz. Find and fix three bugs."""
_DEALS = [{"id": i, "deal_name": f"Deal {i}"} for i in range(1, 26)]


def get_page(cursor: int, page_size: int) -> dict:
    page_items = _DEALS[cursor:page_size]
    next_cursor = cursor + page_size
    return {"items": page_items, "next_cursor": next_cursor}


if __name__ == "__main__":
    page1 = get_page(cursor=0, page_size=5)
    print(page1)
    page2 = get_page(cursor=page1["next_cursor"], page_size=5)
    print(page2)