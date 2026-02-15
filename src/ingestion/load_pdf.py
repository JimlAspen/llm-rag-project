"""
PDF loading utilities.

This module extracts text from PDF files using PyPDF2. It is designed
to be used as part of the ingestion pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from PyPDF2 import PdfReader


def load_pdf_text(path: Path) -> str:
    """
    Extract text from a PDF file.

    Parameters
    ----------
    path : Path
        Path to the PDF file.

    Returns
    -------
    str
        Extracted text from all pages.
    """
    reader = PdfReader(str(path))
    pages: List[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)
