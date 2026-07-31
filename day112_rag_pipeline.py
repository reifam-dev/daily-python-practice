"""Day 112 - Full RAG Pipeline: Retrieval, Reranking, and Cited Answers.

Combines a Chroma vector store with the Anthropic API to retrieve
relevant document extracts, rerank them by a simple keyword-overlap
score, and generate an answer that cites which extract it drew from -
PCPP1 standard. This closes out Phase 2 (Days 101-112).
"""
from __future__ import annotations

import os

import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_DOCUMENTS: list[str] = [
    "Loan Agreement: Riverside JV facility of GBP 8,500,000 at SONIA plus "
    "2.75 percent, secured by first legal charge, LTV covenant of 65 percent.",
    "Investment Memo: Logistics Portfolio acquisition at a 6.2 percent net "
    "initial yield, targeting a 14 percent unlevered IRR over five years.",
]


class RagPipeline:
    """A minimal retrieval-augmented generation pipeline over Chroma."""

    def __init__(self, persist_path: str = "./chroma_store") -> None:
        self._vector_client = chromadb.PersistentClient(path=persist_path)
        self._collection = self._vector_client.get_or_create_collection(
            name="rag_documents"
        )

    def index_documents(self, documents: list[str]) -> None:
        """Add documents to the vector store with stable ids."""
        self._collection.add(
            documents=documents,
            ids=[f"doc-{i}" for i in range(len(documents))],
        )

    def retrieve_context(self, question: str, n_results: int = 2) -> list[str]:
        """Retrieve the most relevant document extracts for a question."""
        results = self._collection.query(query_texts=[question], n_results=n_results)
        return results["documents"][0]

    def rerank(self, question: str, documents: list[str]) -> list[str]:
        """Rerank retrieved documents by simple keyword overlap with the question."""
        question_words = set(question.lower().split())

        def overlap_score(doc: str) -> int:
            doc_words = set(doc.lower().split())
            return len(question_words & doc_words)

        return sorted(documents, key=overlap_score, reverse=True)

    def answer_with_citations(self, question: str) -> str:
        """Retrieve, rerank, and answer a question with source citations."""
        context = self.retrieve_context(question)
        context = self.rerank(question, context)
        context_block = "\n".join(f"[{i}] {doc}" for i, doc in enumerate(context))

        prompt = (
            f"Context:\n{context_block}\n\n"
            f"Question: {question}\n"
            "Answer using only the context above. Cite sources like [0], [1]."
        )

        response = _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


if __name__ == "__main__":
    pipeline = RagPipeline()
    pipeline.index_documents(_DOCUMENTS)
    print(pipeline.answer_with_citations("What is the LTV covenant on the Riverside JV loan?"))