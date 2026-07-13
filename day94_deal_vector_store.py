"""Day 94 - Vector Databases: Deal Document Vector Store.

Wraps ChromaDB for storing and retrieving financial document extracts
(loan agreements, investment memos), with metadata filtering and an
optional LLM summarisation step over the retrieved context -
PCPP1 standard.
"""
from __future__ import annotations

import os
import uuid

import chromadb
from anthropic import Anthropic
from chromadb.api.models.Collection import Collection
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_llm_client = Anthropic(api_key=_api_key)


class DealVectorStore:
    """A thin, typed wrapper around a Chroma collection of deal documents."""

    def __init__(self, persist_path: str = "./chroma_store") -> None:
        self._client = chromadb.PersistentClient(path=persist_path)
        self._collection: Collection = self._client.get_or_create_collection(
            name="deal_documents"
        )

    def add_document(self, text: str, category: str) -> str:
        """Add a document with a unique id and category metadata."""
        document_id = str(uuid.uuid4())
        self._collection.add(
            documents=[text],
            metadatas=[{"category": category}],
            ids=[document_id],
        )
        return document_id

    def retrieve_top_match(self, query: str, category: str | None = None) -> str:
        """Return the single closest-matching document, optionally filtered."""
        where_filter = {"category": category} if category else None
        results = self._collection.query(
            query_texts=[query],
            n_results=1,
            where=where_filter,
        )
        return results["documents"][0][0]


def summarise(text: str) -> str:
    """Summarise a retrieved document extract in one sentence via the LLM."""
    response = _llm_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Summarise in one sentence: {text}"}],
    )
    return response.content[0].text


_SAMPLE_DOCUMENTS = [
    (
        "Loan Agreement: Riverside JV facility of GBP 8,500,000 at SONIA "
        "plus 2.75 percent, maturing 36 months from drawdown, secured by "
        "first legal charge over the property.",
        "loan_agreement",
    ),
    (
        "Investment Memo: Logistics Portfolio acquisition at a 6.2 percent "
        "net initial yield, targeting a 14 percent unlevered IRR over a "
        "five-year hold, with rental reversion potential of 18 percent.",
        "investment_memo",
    ),
    (
        "Loan Agreement: Westgate Retail Park facility of GBP 5,000,000 "
        "with a loan-to-value covenant of 65 percent, tested quarterly.",
        "loan_agreement",
    ),
]


if __name__ == "__main__":
    store = DealVectorStore()
    for text, category in _SAMPLE_DOCUMENTS:
        store.add_document(text, category)

    match = store.retrieve_top_match(
        "what is the loan-to-value covenant?", category="loan_agreement"
    )
    print(summarise(match))