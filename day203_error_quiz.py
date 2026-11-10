"""Day 203 - Text Chunking with Overlap: Error Quiz. Find and fix three bugs."""


def chunk_words(text: str, chunk_size: int, overlap: int) -> list:
    words = text.split()
    step = chunk_size
    chunks = []
    for start in range(0, len(words) - chunk_size + 1, step):
        chunks.append(" ".join(words[start:start + chunk_size]))
    return chunks


if __name__ == "__main__":
    text = " ".join(f"w{i}" for i in range(20))
    for chunk in chunk_words(text, chunk_size=8, overlap=2):
        print(chunk)
    print(chunk_words("only five words in this", chunk_size=8, overlap=2))