# Makefile for LLM-RAG project

PYTHON=python

.PHONY: ingest chunk test all

ingest:
	$(PYTHON) -m src.ingestion.ingest

chunk:
	$(PYTHON) -m src.chunking.run_chunking

test:
	pytest -q

all: ingest chunk
