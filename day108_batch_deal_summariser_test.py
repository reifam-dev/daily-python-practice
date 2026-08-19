"""Day 131 (Testing Retrofit — Day 108): pytest tests for
day108_batch_deal_summariser.py.

Tests build_batch_requests() directly - pure logic, no API call
inside it, so no mocking is needed here (unlike Day 106's retrofit).
Covers request count, custom_id sequencing, request structure, and
the empty-input edge case.
"""
import day108_batch_deal_summariser as batch


def test_build_batch_requests_returns_one_per_deal():
    deals = ["Riverside JV, 12.5m", "Westgate Retail, 8.1m"]
    requests = batch.build_batch_requests(deals)
    assert len(requests) == 2


def test_custom_ids_are_sequential():
    deals = ["Deal A", "Deal B", "Deal C"]
    requests = batch.build_batch_requests(deals)
    ids = [r["custom_id"] for r in requests]
    assert ids == ["deal-0", "deal-1", "deal-2"]


def test_each_request_has_correct_params_structure():
    deals = ["Riverside JV, 12.5m"]
    requests = batch.build_batch_requests(deals)
    single_request = requests[0]

    assert single_request["params"]["model"] == "claude-sonnet-4-6"
    assert single_request["params"]["max_tokens"] == 200
    assert "Riverside JV, 12.5m" in single_request["params"]["messages"][0]["content"]


def test_empty_deal_list_returns_empty_requests():
    requests = batch.build_batch_requests([])
    assert requests == []