# This file contains 3 deliberate bugs. Find and fix them.
import numpy as np
from anthropic import Anthropic


class SimpleRAG:

    def __init__(self) -> None:
        self._client = Anthropic()
        self._documents: list[str] = []
        self._embeddings: list[np.ndarray] = []

    def add_document(self, text: str) -> None:
        self._documents.append(text)
        embedding = self._embed(text)
        self._embeddings.append(embedding)

    def _embed(self, text: str) -> np.ndarray:
        words = text.lower().split()
        vec = np.zeros(100)
        for i, word in enumerate(words[:100]):
            vec[i] = len(word)
        return vec / (np.linalg.norm(vec) or 1)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b))              # Bug 1: cosine similarity needs / (norm(a) * norm(b)) — vecs not normalised at query time

    def retrieve(self, query: str, k: int = 2) -> list[str]:
        query_vec = self._embed(query)
        scores = [self._cosine_similarity(query_vec, e) for e in self._embeddings]
        top_k = sorted(range(len(scores)), key=lambda i: scores[i])[:k]  # Bug 2: should be reverse=True (highest first)
        return [self._documents[i] for i in top_k]

    def answer(self, query: str) -> str:
        context = self.retrieve(query)
        context_str = "\n".join(context)
        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Context:\n{context_str}\n\nQuestion: {query}"
            }]
        )
        return response.content[0].text

    def __len__(self) -> int:
        return len(self._documents) + 1         # Bug 3: should not add 1


if __name__ == "__main__":
    rag = SimpleRAG()
    rag.add_document("Office yields in London are circa 4.5% for prime assets.")
    rag.add_document("Industrial assets in the Midlands trade at 5-6% NIY.")
    rag.add_document("Retail warehousing has seen yield compression to below 5%.")
    print(f"Documents stored: {len(rag)}")
    context = rag.retrieve("What are London office yields?")
    print("Retrieved:", context)