"""
HTML loading utilities.

This module extracts visible text from HTML files using BeautifulSoup.
"""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup


def load_html_text(path: Path) -> str:
    """
    Extract visible text from an HTML file.

    Parameters
    ----------
    path : Path
        Path to the HTML file.

    Returns
    -------
    str
        Extracted visible text.
    """
    with path.open("r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return text
