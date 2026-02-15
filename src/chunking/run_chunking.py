"""
Run the chunking pipeline.

This module loads cleaned text files from ``data/processed/``,
applies token-based chunking using the configuration in
``configs/chunking.yaml``, and writes JSONL chunk files to
``data/chunks/``.

It is the second stage of the ingestion → chunking → embedding pipeline.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Any

import yaml

from src.chunking.chunk import chunk_text


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_config(path: Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    path : Path
        Path to the YAML configuration file.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_text_file(path: Path) -> str:
    """
    Load a UTF-8 encoded text file.

    Parameters
    ----------
    path : Path
        Path to the text file.

    Returns
    -------
    str
        File contents as a string.
    """
    return path.read_text(encoding="utf-8")


def run_chunking() -> None:
    """
    Execute the chunking pipeline.

    This function:
    - Loads chunking configuration
    - Iterates over processed text files
    - Applies token-based chunking
    - Writes chunked output to JSONL files
    """
    logging.info("RUN_CHUNKING: starting")

    project_root = Path(__file__).resolve().parents[2]
    processed_dir = project_root / "data" / "processed"
    chunks_dir = project_root / "data" / "chunks"
    config_path = project_root / "configs" / "chunking.yaml"

    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Load chunking configuration
    config = load_config(config_path)
    chunk_size = config["chunk_size"]
    chunk_overlap = config["chunk_overlap"]
    tokenizer_name = config.get("tokenizer_name", "cl100k_base")

    logging.info(
        "Loaded chunking config: size=%s, overlap=%s, tokenizer=%s",
        chunk_size,
        chunk_overlap,
        tokenizer_name,
    )

    # Find processed text files
    text_files = list(processed_dir.glob("*.txt"))
    if not text_files:
        logging.warning("No processed text files found in %s", processed_dir)
        return

    # Process each file
    for text_file in text_files:
        source_name = text_file.stem
        logging.info("Chunking file: %s", source_name)

        text = load_text_file(text_file)

        chunks = chunk_text(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            tokenizer_name=tokenizer_name,
            source_name=source_name,
        )

        # Write JSONL output
        output_path = chunks_dir / f"{source_name}.jsonl"
        with output_path.open("w", encoding="utf-8") as file:
            for chunk in chunks:
                file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

        logging.info("Wrote %s chunks → %s", len(chunks), output_path)


if __name__ == "__main__":
    run_chunking()
