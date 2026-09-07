"""Day 150 - Cursor-Based Pagination: pages advance by slicing from
the cursor for page_size items, and next_cursor is None once the end
of the data is reached, so a client knows when to stop - PCPP1
standard."""
from __future__ import annotations

_DEALS = [{"id": i, "deal_name": f"Deal {i}"} for i in range(1, 26)]


def get_page(cursor: int, page_size: int) -> dict:
    page_items = _DEALS[cursor:cursor + page_size]
    next_cursor = cursor + page_size
    has_more = next_cursor < len(_DEALS)
    return {"items": page_items, "next_cursor": next_cursor if has_more else None}


if __name__ == "__main__":
    cursor = 0
    while True:
        page = get_page(cursor=cursor, page_size=5)
        print(f"cursor={cursor}: {len(page['items'])} items")
        if page["next_cursor"] is None:
            break
        cursor = page["next_cursor"]