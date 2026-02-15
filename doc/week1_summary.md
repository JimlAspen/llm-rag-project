```markdown
# Week 1 Summary — Ingestion & Chunking

## ✔️ Completed This Week

### 1. Project Structure
A clean, production‑grade folder structure was created, including:

- `src/ingestion/`
- `src/chunking/`
- `configs/`
- `data/raw/`, `data/processed/`, `data/chunks/`

---

### 2. Ingestion Pipeline
Implemented:

- PDF loader (`load_pdf.py`)
- HTML loader (`load_html.py`)
- Text cleaner (`clean_text.py`)
- YAML‑driven ingestion runner (`ingest.py`)
- Graceful skipping of missing files
- Verified ingestion using a simple `test_doc` source

---

### 3. Chunking Pipeline
Implemented:

- Token‑based chunker (`chunk.py`)
- YAML‑driven chunking runner (`run_chunking.py`)
- JSONL output format for embeddings
- Verified chunking using processed test documents

---

### 4. Configuration Files
Created and populated:

- `sources.yaml`
- `chunking.yaml`
- `retrieval.yaml` (scaffolding for Week 2)

---

### 5. Testing
- Confirmed ingestion + chunking run end‑to‑end
- Verified output in `data/processed/` and `data/chunks/`

---

## 📌 What’s Next (Week 2)

- Embedding chunks using SentenceTransformers  
- Building a FAISS index  
- Retrieval logic  
- Retrieval evaluation scaffolding  

Week 1 is fully complete.