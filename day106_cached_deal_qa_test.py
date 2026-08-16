"""Day 128 (Testing Retrofit — Day 106): pytest tests for
day106_cached_deal_qa.py.

Covers cache key determinism and normalisation directly, and covers
the actual caching behaviour of ask_with_cache() using pytest's
monkeypatch fixture to replace the real Anthropic API call with a
fake, predictable one - no real API key or network call required.
"""
import day106_cached_deal_qa as qa


def test_cache_key_is_deterministic():
    key1 = qa.cache_key("What is a typical LTV?")
    key2 = qa.cache_key("What is a typical LTV?")
    assert key1 == key2


def test_cache_key_normalises_case_and_whitespace():
    key1 = qa.cache_key("  What is a typical LTV?  ")
    key2 = qa.cache_key("what is a typical ltv?")
    assert key1 == key2


def test_cache_key_differs_for_different_questions():
    key1 = qa.cache_key("Question A")
    key2 = qa.cache_key("Question B")
    assert key1 != key2


def test_ask_with_cache_stores_and_reuses_answer(monkeypatch):
    qa._cache.clear()

    class FakeTextBlock:
        text = "Fake answer from the fake API"

    class FakeResponse:
        content = [FakeTextBlock()]

    def fake_create(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(qa._client.messages, "create", fake_create)

    answer1 = qa.ask_with_cache("What is a typical LTV?")
    assert answer1 == "Fake answer from the fake API"
    assert qa.cache_size() == 1

    answer2 = qa.ask_with_cache("What is a typical LTV?")
    assert answer2 == answer1
    assert qa.cache_size() == 1