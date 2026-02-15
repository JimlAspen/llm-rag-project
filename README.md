# LLM‑RAG Project

A production‑minded Retrieval‑Augmented Generation (RAG) system designed with
clean architecture, reproducibility, and governance in mind.  
This project follows a structured 6‑week roadmap, with Week 1 focused on
ingestion and chunking.

---

## 📁 Project Structure

llm-rag-project/
├── configs/
│   ├── sources.yaml
│   ├── chunking.yaml
│   └── retrieval.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── chunks/
├── src/
│   ├── ingestion/
│   │   ├── ingest.py
│   │   ├── load_pdf.py
│   │   ├── load_html.py
│   │   └── clean_text.py
│   └── chunking/
│       ├── chunk.py
│       └── run_chunking.py
└── tests/
---
## 🚀 Week 1: Ingestion & Chunking

### Ingestion Pipeline

The ingestion pipeline:

- Loads PDF, HTML, and plain text files  
- Cleans and normalizes text  
- Writes output to `data/processed/`  
- Uses `configs/sources.yaml` for reproducibility  

Run ingestion:

```bash
python -m src.ingestion.ingest
```


### Chunking Pipeline

The chunking pipeline:

- Performs token-based chunking using tiktoken
- Uses configurable chunk size and overlap
- Writes JSONL chunks to data/chunks/
- Uses configs/chunking.yaml for parameters

Run chunking:

```bash
python -m src.chunking.run_chunking
```

### Testing the Pipeline

Add a simple test source to configs/sources.yaml:

sources:

- name: test_doc
  type: text
  path: data/raw/test_doc.txt

Create the file:

data/raw/test_doc.txt

Then run:

python -m src.ingestion.ingest
python -m src.chunking.run_chunking

You should see:

data/processed/test_doc.txt

data/chunks/test_doc.jsonl

### Roadmap

Week 1 (Completed):

- Folder structure
- Ingestion pipeline
- Chunking pipeline
- YAML configs
- Basic documentation

Week 2 (Next):

- Embedding chunks
- Building FAISS index
- Retrieval logic

### Notes

This project emphasizes:

- Deterministic pipelines
- YAML-driven configuration
- Clean separation of concerns
- Production-grade engineering discipline