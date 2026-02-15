# 🧠 RAG + Grounded AI Pipeline (Multi‑Week Build)

A governed, reproducible Retrieval‑Augmented Generation (RAG) and Grounded AI pipeline built from scratch.  
This project is developed week‑by‑week to demonstrate production‑grade LLM system design, including ingestion, token‑based chunking, deterministic configs, and end‑to‑end testing.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/Week-1%20Complete-blueviolet)

---

## 🚀 Overview

This repository contains a modular, testable, and fully reproducible RAG pipeline designed with modern ML engineering practices.  
Each week adds a new subsystem, building toward a complete, governed RAG + Grounded AI stack.

The project emphasizes:

- Deterministic, config‑driven pipelines  
- Explicit governance and safety alignment  
- Reproducible ML workflows  
- Modular architecture for ingestion, chunking, embeddings, retrieval, and evaluation  
- Production‑grade engineering practices (tests, Makefile, structure, docs)

---

## 📂 Project Structure

```text
llm-rag-project/
│
├── configs/
│   ├── ingestion.yaml          # Source governance + ingestion settings
│   └── chunking.yaml           # Chunk size, overlap, tokenizer config
│
├── data/
│   ├── raw/                    # Original unprocessed documents
│   ├── processed/              # Cleaned text after ingestion
│   └── chunks/                 # Token-based chunks (deterministic)
│
├── src/
│   ├── ingestion/
│   │   ├── ingest.py           # Main ingestion pipeline
│   │   └── loaders.py          # Fallback loaders for robustness
│   │
│   ├── chunking/
│   │   ├── chunk_text.py       # Token-based chunking logic
│   │   └── tokenizer.py        # Tokenizer wrapper + utilities
│   │
│   └── utils/
│       └── io.py               # File I/O helpers
│
├── tests/
│   ├── test_ingestion.py       # Ingestion unit tests
│   └── test_chunking.py        # Chunking unit tests
│
├── notebooks/                  # Exploratory analysis (optional)
│
├── Makefile                    # make ingest / make chunk / make test
├── README.md                   # Project documentation
├── week1_summary.md            # Week 1 deliverables summary
└── pyproject.toml              # (Optional) Project metadata + deps
```
This layout supports modular development and clean orchestration across weeks.

---

## 🧩 Week 1 — Ingestion + Chunking (Complete)

### ✔ Ingestion Pipeline
- Loads documents from disk  
- Supports fallback loaders for robustness  
- Normalizes and stores processed text  
- Fully configurable via `configs/ingestion.yaml`  

### ✔ Chunking Pipeline
- Token‑based chunking with safe overlap  
- Deterministic output for reproducibility  
- Guards for edge cases (tiny docs, negative indices, etc.)  
- Configurable via `configs/chunking.yaml`  

### ✔ Tests
- Pytest suite for ingestion and chunking  
- Deterministic test fixtures  
- Ensures correctness and stability  

### ✔ Makefile
Convenience commands:
- make ingest
- make chunk
- make test
---

## 🗺️ Roadmap

### **Week 1 — Ingestion + Chunking ✔**
- Ingestion pipeline  
- Token-based chunking  
- YAML configs  
- Tests  
- Makefile  
- Documentation  

### **Week 2 — Embeddings + Vector Store**
- Embedding pipeline  
- Vector DB integration  
- Deterministic indexing  
- Tests  

### **Week 3 — Retrieval + Grounded QA**
- Retriever module  
- Grounded answer generation  
- Evaluation harness  

### **Week 4 — RAG Orchestration**
- Config-driven execution  
- Logging + tracing  
- Modular pipeline runner  

### **Week 5 — Evaluation + Guardrails**
- Hallucination detection  
- Groundedness scoring  
- Safety checks  

### **Week 6 — Packaging + Deployment**
- CLI  
- Dockerfile  
- Final documentation  

---

## 🛠️ Installation

```bash
git clone https://github.com/<your-username>/llm-rag-project.git
cd llm-rag-project
pip install -r requirements.txt
```
