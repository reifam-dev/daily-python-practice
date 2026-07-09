"""
Day 79 – RAG Systems: embeddings, cosine similarity, vector retrieval, LLM augmentation.
Uses real financial property document extracts as the knowledge corpus.
Includes python-dotenv for API key hygiene — never commit .env to GitHub.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install anthropic numpy python-dotenv

.env file (add to .gitignore):
    ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import numpy as np
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

# Financial document corpus — extracts from loan agreements, valuation reports,
# and investment memoranda typical of UK commercial real estate transactions.
PROPERTY_CORPUS: list[str] = [
    # Loan agreement extract
    "The Loan to Value ratio shall not at any time exceed 65% of the Open Market Value "
    "of the Property as determined by an Independent Valuer appointed by the Lender. "
    "The Borrower shall procure a desktop valuation within 10 Business Days of each "
    "Interest Payment Date if the Lender so requests.",

    # RICS valuation report extract
    "In our opinion the Market Value of the freehold interest in the Property as at the "
    "Valuation Date, assuming the Property is fully let at the Estimated Rental Value "
    "and subject to the assumptions set out herein, is £42,500,000 (Forty-Two Million "
    "Five Hundred Thousand Pounds). The Net Initial Yield reflects at 4.75% capital "
    "value having regard to comparable transactions in the EC2 submarket.",

    # Investment memorandum extract — debt terms
    "Senior debt is available at 55% LTV with an interest rate of SONIA plus 225 basis "
    "points. Mezzanine financing is available for a further 15% of capital stack at "
    "SONIA plus 650 basis points. The all-in blended cost of debt at 70% LTV is "
    "approximately 4.8% per annum on current market rates.",

    # Investment memorandum extract — market context
    "Prime City of London office yields have compressed to 4.25% for long-let Grade A "
    "assets with strong institutional covenants. West End yields remain sub-4.00% for "
    "trophy assets. Reversionary potential is significant where passing rents are below "
    "current ERV of £75-£85 psf in core City locations.",

    # Asset management report extract
    "The WAULT to expiry across the portfolio is 4.2 years and to break 3.1 years. "
    "Three leases representing 28% of income are subject to rent review in the next "
    "12 months. ERV across the portfolio is estimated at £3.85m per annum against "
    "a passing rent of £3.42m per annum, representing a reversionary uplift of 12.6%.",

    # JV agreement extract
    "The Preferred Return shall accrue at a rate of 8% per annum compounded quarterly "
    "on the aggregate amount of Invested Capital. The Promote shall be calculated as "
    "20% of profits above the Preferred Return hurdle, with a 50/50 catch-up mechanism "
    "until the General Partner has received 20% of all distributions.",

    # Risk section extract
    "Key risks to the investment thesis include: (i) lease expiry concentration with "
    "55% of income expiring within three years; (ii) structural shift in demand for "
    "office space driven by hybrid working patterns; (iii) rising base rates increasing "
    "refinancing costs at maturity; (iv) planning risk on proposed extension to provide "
    "an additional 12,000 sq ft of NIA.",
]


class SimpleRAG:
    """
    Retrieval-Augmented Generation system using bag-of-words embeddings
    and cosine similarity, with a real estate financial document corpus.
    """

    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
        """Initialise the RAG system.

        Args:
            model: Anthropic model string for generation.

        Raises:
            EnvironmentError: If ANTHROPIC_API_KEY is not set.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not set. Add it to your .env file."
            )
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

    def load_corpus(self, corpus: list[str]) -> None:
        """Load a list of documents into the knowledge base.

        Args:
            corpus: List of document strings to embed and store.
        """
        for doc in corpus:
            self.add_document(doc)

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
            a: First vector.
            b: Second vector.

        Returns:
            Cosine similarity as a float in [-1, 1].
        """
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def retrieve(self, query: str, k: int = 3) -> list[str]:
        """Retrieve the top-k most relevant documents for a query.

        Args:
            query: User query string.
            k:     Number of documents to retrieve; defaults to 3.

        Returns:
            List of the k most relevant document strings.
        """
        if not self._documents:
            return []
        query_vec = self._embed(query)
        scores = [self._cosine_similarity(query_vec, e) for e in self._embeddings]
        top_k_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:k]
        return [self._documents[i] for i in top_k_indices]

    def answer(self, query: str, k: int = 3) -> str:
        """Generate an answer to a query using retrieved context.

        Args:
            query: User question string.
            k:     Number of context documents to retrieve.

        Returns:
            LLM-generated answer string.
        """
        context_docs = self.retrieve(query, k=k)
        context_str = "\n\n".join(f"[{i+1}] {doc}" for i, doc in enumerate(context_docs))
        prompt = (
            "You are a RICS-qualified property investment analyst and solicitor "
            "with expertise in UK commercial real estate transactions. "
            "Answer the question using only the context provided. "
            "Be precise and use appropriate financial and legal terminology. "
            "Respond in British English.\n\n"
            f"Context:\n{context_str}\n\n"
            f"Question: {query}"
        )
        response = self._client.messages.create(
            model=self._model,
            max_tokens=600,
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
    rag.load_corpus(PROPERTY_CORPUS)

    print(repr(rag))
    print(f"Documents loaded: {len(rag)}\n")

    queries = [
        "What is the maximum LTV permitted under the loan agreement?",
        "What is the market value of the property and at what yield?",
        "What are the debt financing terms available?",
        "What are the key risks to the investment?",
        "What is the WAULT and reversionary potential of the portfolio?",
    ]

    for query in queries:
        print(f"Q: {query}")
        context = rag.retrieve(query, k=2)
        print(f"Retrieved {len(context)} context document(s).")
        answer = rag.answer(query, k=2)
        print(f"A: {answer}\n")
        print("-" * 60 + "\n")