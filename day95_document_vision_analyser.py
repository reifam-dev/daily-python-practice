"""Day 95 - Multimodal: Document and Image Vision Analyser.

Sends property valuation reports or site photographs to Claude as
base64-encoded content blocks, alongside a text question, and returns
the model's answer - PCPP1 standard.
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_MEDIA_TYPES: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".pdf": "application/pdf",
}


class UnsupportedFileTypeError(Exception):
    """Raised when a file extension has no known media type mapping."""


def _encode_file(path: Path) -> str:
    """Return the base64-encoded contents of a file as a plain string."""
    with open(path, "rb") as file:
        return base64.standard_b64encode(file.read()).decode("utf-8")


def _build_content_block(path: Path) -> dict:
    """Build an Anthropic API content block for an image or document."""
    try:
        media_type = _MEDIA_TYPES[path.suffix.lower()]
    except KeyError as exc:
        raise UnsupportedFileTypeError(f"No media type for {path.suffix}") from exc

    block_type = "image" if media_type.startswith("image") else "document"
    return {
        "type": block_type,
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": _encode_file(path),
        },
    }


def analyse_valuation_document(path: Path, question: str) -> str:
    """Ask a question about a valuation report or site image."""
    content_block = _build_content_block(path)
    response = _client.messages.create(
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