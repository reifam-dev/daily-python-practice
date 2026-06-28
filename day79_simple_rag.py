"""
Day 79 – RAG Systems: embeddings, cosine similarity, vector retrieval, LLM augmentation.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install anthropic numpy
"""

import numpy as np
from anthropic import Anthropic


class SimpleRAG:
    """
    Minimal Retrieval-Augmented Generation system using bag-of-words
    embeddings and cosine similarity for document retrieval.
    """

    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
        """Initialise the RAG system.

        Args:
            model: Anthropic model string for generation.
        """
        self._client: Anthropic = Anthropic()
        self._model: str = model
        self._documents: list[str] = []
        self._embeddings: list[np.ndarray] = []

    def add_document(self, text: str) -> None:
        """Add a document to the knowledge base and store its embedding.

        Args:
            text: Document text to embed and store.
        """
        self._documents.append(text)
        self._embeddings.append(self._embed(text))

    def _embed(self, text: str) -> np.ndarray:
        """Produce a normalised bag-of-words length vector for a text.

        Args:
            text: Input text to embed.

        Returns:
            Normalised numpy array of length 100.
        """
        words = text.lower().split()
        vec = np.zeros(100)
        for i, word in enumerate(words[:100]):
            vec[i] = len(word)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors.

        Args:
            a: First normalised vector.
            b: Second normalised vector.

        Returns:
            Cosine similarity as a float in [-1, 1].
        """
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def retrieve(self, query: str, k: int = 2) -> list[str]:
        """Retrieve the top-k most relevant documents for a query.

        Args:
            query: User query string.
            k:     Number of documents to retrieve; defaults to 2.

        Returns:
            List of the k most relevant document strings.
        """
        if not self._documents:
            return []
        query_vec = self._embed(query)
        scores = [self._cosine_similarity(query_vec, e) for e in self._embeddings]
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self._documents[i] for i in top_k_indices]

    def answer(self, query: str, k: int = 2) -> str:
        """Generate an answer to a query using retrieved context.

        Args:
            query: User question string.
            k:     Number of context documents to retrieve.

        Returns:
            LLM-generated answer string.
        """
        context_docs = self.retrieve(query, k=k)
        context_str = "\n".join(f"- {doc}" for doc in context_docs)
        prompt = (
            f"You are a RICS-qualified property analyst. "
            f"Answer the question using only the context provided. "
            f"Respond in British English.\n\n"
            f"Context:\n{context_str}\n\n"
            f"Question: {query}"
        )
        response = self._client.messages.create(
            model=self._model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def __len__(self) -> int:
        """Return the number of documents in the knowledge base.

        Returns:
            Integer count of stored documents.
        """
        return len(self._documents)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this RAG instance.
        """
        return f"SimpleRAG(documents={len(self)}, model='{self._model}')"


if __name__ == "__main__":
    rag = SimpleRAG()
    rag.add_document("Prime office yields in London City are circa 4.25–4.75%.")
    rag.add_document("Industrial logistics assets in the Midlands trade at 5.0–5.5% NIY.")
    rag.add_document("Retail warehousing has seen yield compression to below 5% in prime locations.")
    rag.add_document("West End London offices command sub-4% yields for long-let trophy assets.")

    print(repr(rag))
    print(f"\nDocuments stored: {len(rag)}")

    context = rag.retrieve("What are London office yields?", k=2)
    print("\nRetrieved context:")
    for doc in context:
        print(f"  - {doc}")

    print("\nGenerating answer...")
    answer = rag.answer("What are current London office yields?")
    print(answer)