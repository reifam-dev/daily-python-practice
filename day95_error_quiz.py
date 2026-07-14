"""Day 95 - Multimodal: Error Quiz.

Find and fix three bugs. No location hints.
"""
import base64
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".pdf": "application/pdf",
}


def encode_file(path: Path) -> str:
    with open(path, "rb") as file:
        return base64.encodebytes(file.read())


def build_content_block(path: Path) -> dict:
    media_type = MEDIA_TYPES[path.suffix]
    block_type = "image" if media_type.startswith("image") else "document"
    return {
        "type": block_type,
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": encode_file(path),
        },
    }


def analyse_valuation_document(path: Path, question: str) -> str:
    content_block = build_content_block(path)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": [content_block, {"type": "text", "text": question}],
            }
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    valuation_report = Path("riverside_jv_valuation.pdf")
    answer = analyse_valuation_document(
        valuation_report, "What is the reported market value?"
    )
    print(answer)