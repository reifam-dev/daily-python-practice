"""Day 112 - Full RAG Pipeline: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os

import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

DOCUMENTS = [
    "Loan Agreement: Riverside JV facility of GBP 8,500,000 at SONIA plus "
    "2.75 percent, secured by first legal charge, LTV covenant of 65 percent.",
    "Investment Memo: Logistics Portfolio acquisition at a 6.2 percent net "
    "initial yield, targeting a 14 percent unlevered IRR over five years.",
]

vector_client = chromadb.PersistentClient(path="./chroma_store")
collection = vector_client.get_or_create_collection(name="rag_documents")
collection.add(
    documents=DOCUMENTS,
    ids=[f"doc-{i}" for i in range(len(DOCUMENTS))],
)


def retrieve_context(question: str, n_results: int = 2) -> list[str]:
    results = collection.query(query_texts=[question], n_results=n_results)
    return results["documents"]


def answer_with_citations(question: str) -> str:
    context = retrieve_context(question)
    context_block = "\n".join(f"[{i}] {doc}" for i, doc in enumerate(context))

    prompt = (
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer using only the context above. Cite sources like [0], [1]."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content


if __name__ == "__main__":
    print(answer_with_citations("What is the LTV covenant on the Riverside JV loan?"))