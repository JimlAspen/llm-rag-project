"""
Basic tests for the chunking pipeline.

These tests verify:
- chunk_text() produces non-empty output
- chunks have required fields
- chunk boundaries are consistent
"""

from pathlib import Path

from src.chunking.chunk import chunk_text


def test_chunk_text_basic():
    """Chunk a simple string and verify structure."""
    text = "This is a simple test document. " * 20

    chunks = chunk_text(
        text=text,
        chunk_size=50,
        chunk_overlap=10,
        tokenizer_name="cl100k_base",
        source_name="test_source",
    )

    assert len(chunks) > 0

    first = chunks[0]
    required_keys = {
        "id",
        "text",
        "source",
        "char_start",
        "char_end",
        "token_start",
        "token_end",
    }

    assert required_keys.issubset(first.keys())
    assert first["source"] == "test_source"
    assert first["char_start"] == 0
    assert first["char_end"] > first["char_start"]
    assert first["token_end"] > first["token_start"]
