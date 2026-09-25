# DocuPilot — AI-Powered Document Intelligence & Knowledge Assistant

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791.svg)](https://github.com/pgvector/pgvector)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**DocuPilot** is an end-to-end Generative AI and Retrieval-Augmented Generation (RAG) system that transforms unstructured documents (PDF, TXT, Markdown) into a searchable knowledge assistant with grounded answers and precise source citations.

---

## 🚀 Key Features

* **Multi-Format Ingestion**: Seamlessly upload and process `.pdf`, `.txt`, and `.md` files.
* **Intelligent Chunking**: Boundary-aware recursive splitting (paragraph $\rightarrow$ sentence $\rightarrow$ word) with sliding window overlap.
* **Vector Storage with `pgvector`**: Native PostgreSQL vector search using cosine distance (`<=>` operator).
* **100% Free Stack Support**:
  * **LLM**: Powered by [Groq](https://console.groq.com/) (`openai/gpt-oss-120b`, `llama-3.1-8b-instant`, `qwen3.8-27b`).
  * **Embeddings**: Local, CPU-based embeddings using [FastEmbed](https://github.com/qdrant/fastembed) (`BAAI/bge-small-en-v1.5`, 384 dimensions) — zero API key required.
* **Groundedness & Anti-Hallucination**: Answers are strictly grounded in retrieved passages with explicit page-level citations.
* **Interactive UI**: Clean Streamlit dashboard with document vault management, chat history, and source inspection accordions.
* **Automated Test Suite**: Full unit and integration test coverage with `pytest`.

---

## 🏛️ Architecture Overview

```text
User / Browser
      │
      ▼
Streamlit UI (Port 8501)
      │
      ▼ (REST API)
FastAPI Backend (Port 8000)
      │
      ├── Ingestion ──► Parser ──► Cleaner ──► Chunker ──► FastEmbed ──► PostgreSQL (pgvector)
      │
      └── Query ──────► FastEmbed ──► Cosine Retrieval ──► Context Builder ──► Groq LLM ──► Answer + Sources
```

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend API** | FastAPI / Pydantic | High-performance RESTful API with typed schemas |
| **Database** | PostgreSQL 16 + pgvector | Unified relational metadata and vector storage |
| **LLM Provider** | Groq Cloud API | High-speed, free-tier LLM inference |
| **Embeddings** | FastEmbed (ONNX) | Free, CPU-optimized local dense embeddings |
| **Frontend** | Streamlit | Responsive conversational UI with source cards |
| **Testing** | pytest & httpx | Unit testing and end-to-end integration testing |

---

## 🏁 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/mdkamranalam/docupilot.git
cd docupilot
```

### 2. Set Up Environment & Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` and add your free **Groq API Key** ([Get free key here](https://console.groq.com/keys)):
```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here
LLM_MODEL=openai/gpt-oss-120b

EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DIMENSION=384

POSTGRES_SERVER=localhost
POSTGRES_PORT=5433
POSTGRES_USER=docupilot
POSTGRES_PASSWORD=docupilot_password
POSTGRES_DB=docupilot_db
```

### 4. Start the Database
```bash
docker compose up -d
```

### 5. Start the Backend API
```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
* Interactive API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Start the Frontend UI
In a separate terminal:
```bash
source .venv/bin/activate
streamlit run frontend/streamlit_app.py
```
* Streamlit Web Application: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Running Tests

Execute the automated test suite:
```bash
source .venv/bin/activate
PYTHONPATH=. pytest tests/
```

---

## 📚 Project Documentation

Detailed architecture specifications and engineering reasoning can be found in the [`docs/`](docs/) directory:

* [`docs/01-problem.md`](docs/01-problem.md) — Problem Statement & Solution Overview
* [`docs/02-requirements.md`](docs/02-requirements.md) — Functional & Non-Functional Requirements
* [`docs/03-architecture.md`](docs/03-architecture.md) — High-Level & Component Architecture
* [`docs/04-document-processing.md`](docs/04-document-processing.md) — Parsing & Text Cleaning Pipeline
* [`docs/05-chunking.md`](docs/05-chunking.md) — Boundary-Aware Chunking Strategies
* [`docs/06-embeddings.md`](docs/06-embeddings.md) — Embedding Providers & Vector Dimensions
* [`docs/07-retrieval.md`](docs/07-retrieval.md) — Semantic Search & pgvector SQL Queries
* [`docs/08-rag.md`](docs/08-rag.md) — End-to-End RAG Execution Lifecycle
* [`docs/09-prompt-design.md`](docs/09-prompt-design.md) — Prompt Templates & Anti-Hallucination Controls
* [`docs/10-evaluation.md`](docs/10-evaluation.md) — Evaluation Dimensions & Test Suite
* [`docs/11-failure-modes.md`](docs/11-failure-modes.md) — Failure Mode Analysis & Mitigations
* [`docs/12-design-decisions.md`](docs/12-design-decisions.md) — Architectural Trade-Offs & Decisions

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.