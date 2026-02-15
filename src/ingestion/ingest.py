"""
Ingestion pipeline for loading and cleaning guideline documents.

This script reads the list of data sources from `configs/sources.yaml`,
loads each document (PDF or HTML), applies cleaning rules, and writes
the cleaned text to `data/processed/`.

It is the first stage of the ingestion → chunking → embedding pipeline.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

import yaml

from src.ingestion.load_pdf import load_pdf_text
from src.ingestion.load_html import load_html_text
from src.ingestion.clean_text import clean_text


# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def load_sources_config(path: Path) -> list[dict]:
    """
    Load the YAML configuration listing all data sources.

    Parameters
    ----------
    path : Path
        Path to the `sources.yaml` configuration file.

    Returns
    -------
    list of dict
        List of source definitions.
    """
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Expect structure: { "sources": [ ... ] }
    if "sources" not in config:
        raise ValueError("sources.yaml must contain a top-level 'sources:' key")

    return config["sources"]


def load_document(source: Dict[str, Any]) -> str:
    """
    Load a document based on its type (PDF or HTML).

    Parameters
    ----------
    source : dict
        A dictionary describing the source, including:
        - name: str
        - path: str
        - type: "pdf" or "html"

    Returns
    -------
    str
        Raw extracted text.

    Raises
    ------
    ValueError
        If the source type is unsupported.
    """
    source_type = source["type"].lower()
    source_path = Path(source["path"])

    if not source_path.exists(): 
        raise FileNotFoundError(f"Source file not found: {source_path}")

    if source_type == "pdf":
        return load_pdf_text(source_path)
    if source_type == "html":
        return load_html_text(source_path)
    if source_type == "text":
        return Path(source_path).read_text(encoding="utf-8")


    raise ValueError(f"Unsupported source type: {source_type}")


def write_processed_text(text: str, output_path: Path) -> None:
    """
    Write cleaned text to a UTF-8 file.

    Parameters
    ----------
    text : str
        Cleaned document text.
    output_path : Path
        Destination file path.
    """
    with output_path.open("w", encoding="utf-8") as file:
        file.write(text)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_ingestion() -> None:
    """
    Execute the ingestion pipeline.

    This function:
    - Loads the list of sources from `configs/sources.yaml`
    - Loads each document (PDF or HTML)
    - Applies cleaning rules
    - Writes cleaned text to `data/processed/`
    """
    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "configs" / "sources.yaml"
    processed_dir = project_root / "data" / "processed"

    processed_dir.mkdir(parents=True, exist_ok=True)

    sources = load_sources_config(config_path)
    logging.info("Loaded %s sources from %s", len(sources), config_path)

    for source in sources:
        name = source["name"]
        logging.info("Processing source: %s", name)

        try: 
            raw_text = load_document(source) 
        except FileNotFoundError as exc: 
            logging.warning("Skipping %s: %s", name, exc) 
            continue

        cleaned_text = clean_text(raw_text)

        output_path = processed_dir / f"{name}.txt"
        write_processed_text(cleaned_text, output_path)

        logging.info("Wrote cleaned text → %s", output_path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_ingestion()

