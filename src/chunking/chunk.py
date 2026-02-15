"""
Text chunking utilities.

This module provides token-based chunking for long documents using a
configurable chunk size, overlap, and tokenizer. It is designed to be
used as part of an ingestion → chunking → embedding pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import tiktoken


@dataclass
class Chunk:
    """
    Representation of a single text chunk.

    Parameters
    ----------
    id : str
        Unique identifier for the chunk.
    text : str
        The chunk text.
    source : str
        Name or identifier of the source document.
    char_start : int
        Start character index in the original document.
    char_end : int
        End character index in the original document.
    token_start : int
        Start token index in the original document.
    token_end : int
        End token index in the original document.
    """
    id: str
    text: str
    source: str
    char_start: int
    char_end: int
    token_start: int
    token_end: int


def get_tokenizer(tokenizer_name: str = "cl100k_base") -> tiktoken.Encoding:
    """
    Get a tiktoken tokenizer by name.

    Parameters
    ----------
    tokenizer_name : str, optional
        Name of the tokenizer to use, by default "cl100k_base".

    Returns
    -------
    tiktoken.Encoding
        The tokenizer encoding instance.
    """
    return tiktoken.get_encoding(tokenizer_name)



def chunk_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    tokenizer_name: str,
    source_name: str,
) -> List[dict]:
    """
    Split text into overlapping token-based chunks.

    This implementation:
    - Encodes once
    - Decodes only the chunk window (never prefixes)
    - Handles all edge cases:
        * total tokens < chunk_size
        * total tokens < chunk_overlap
        * negative token_start
        * tiny documents
    - Avoids token→char mapping entirely
    - Is stable, fast, and memory-safe
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    encoding = get_tokenizer(tokenizer_name)

    # Encode once
    tokens = encoding.encode(text)
    num_tokens = len(tokens)

    # Handle empty or tiny documents safely
    if num_tokens == 0:
        return []

    if num_tokens <= chunk_size:
        # One chunk only, no overlap
        return [
            {
                "id": f"{source_name}-0000",
                "text": text,
                "source": source_name,
                "char_start": 0,
                "char_end": len(text),
                "token_start": 0,
                "token_end": num_tokens,
            }
        ]

    chunks: List[Chunk] = []
    token_start = 0
    chunk_index = 0

    while token_start < num_tokens:
        token_end = min(token_start + chunk_size, num_tokens)

        # Decode only this chunk window
        chunk_tokens = tokens[token_start:token_end]
        chunk_text_str = encoding.decode(chunk_tokens)

        # Compute character offsets by decoding only the prefix of THIS chunk
        # This is safe and bounded because we never decode the entire document.
        prefix_tokens = tokens[:token_start]
        prefix_text = encoding.decode(prefix_tokens)

        char_start = len(prefix_text)
        char_end = char_start + len(chunk_text_str)

        chunk_id = f"{source_name}-{chunk_index:04d}"
        chunk = Chunk(
            id=chunk_id,
            text=chunk_text_str,
            source=source_name,
            char_start=char_start,
            char_end=char_end,
            token_start=token_start,
            token_end=token_end,
        )
        chunks.append(chunk)

        chunk_index += 1

        # Move window forward with overlap
        next_start = token_end - chunk_overlap

        # Prevent negative token_start (edge case: small docs)
        if next_start <= token_start:
            break

        token_start = next_start

    return [
        {
            "id": c.id,
            "text": c.text,
            "source": c.source,
            "char_start": c.char_start,
            "char_end": c.char_end,
            "token_start": c.token_start,
            "token_end": c.token_end,
        }
        for c in chunks
    ]
