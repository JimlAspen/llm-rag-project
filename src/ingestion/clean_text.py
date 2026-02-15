"""
Text cleaning utilities.

This module normalizes whitespace, removes repeated blank lines,
and prepares text for chunking and embedding.
"""

from __future__ import annotations

import re


def clean_text(text: str) -> str:
    """
    Clean and normalize raw extracted text.

    Parameters
    ----------
    text : str
        Raw extracted text.

    Returns
    -------
    str
        Cleaned and normalized text.
    """
    # Normalize Windows/Mac line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip trailing spaces
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Collapse multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Trim leading/trailing whitespace
    return text.strip()
