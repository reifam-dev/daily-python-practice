"""Day 94 - Vector Databases: Error Quiz.

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
    "2.75 percent, maturing 36 months from drawdown, secured by first "
    "legal charge over the property.",
    "Investment Memo: Logistics Portfolio acquisition at a 6.2 percent "
    "net initial yield, targeting a 14 percent unlevered IRR over a "
    "five-year hold, with rental reversion potential of 18 percent.",
    "Loan Agreement: Westgate Retail Park facility of GBP 5,000,000 with "
    "a loan-to-value covenant of 65 percent, tested quarterly.",
]

METADATAS = [
    {"category": "loan_agreement"},
    {"category": "investment_memo"},
    {"category": "loan_agreement"},
]

DOC_IDS = "doc"

vector_client = chromadb.PersistentClient(path="./chroma_store")
collection = vector_client.get_or_create_collection(name="deal_documents")

collection.add(documents=DOCUMENTS, metadatas=METADATAS, ids=DOC_IDS)


def retrieve_top_match(query: str, category: str) -> str:
    results = collection.query(
        query_texts=[query],
        n_results=1,
        where="category=" + category,
    )
    return results["documents"][0]


def summarise(text: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Summarise in one sentence: {text}"}],
    )
    return response.content[0].text


if __name__ == "__main__":
    match = retrieve_top_match("what is the loan-to-value covenant?", "loan_agreement")
    print(summarise(match))