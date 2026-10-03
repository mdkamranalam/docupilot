# Course 1 Student Learning Guide: Building DocuPilot

Welcome to **DocuPilot** — the reference implementation for **Course 1: Generative AI Application Development (90 hours)**.

This guide walks you module-by-module through how every concept taught in class translates into real-world, working Python code inside this codebase.

---

## 🗺️ Module-by-Module Code Map

```text
Course 1 Modules                              DocuPilot Codebase Architecture
─────────────────────────────────────────────────────────────────────────────
M1: Python Fundamentals       ──►  Clean project structure, file handling, requirements.txt
M2: Intermediate Python       ──►  app/services/, app/db/, OOP patterns, FastAPI REST APIs
M3: Prompt Engineering        ──►  app/llm/prompts.py (System Prompts, Delimiters, Few-Shot)
M4: GenAI Application Dev     ──►  app/retrieval/, app/embeddings/, PostgreSQL pgvector, Streamlit
M5: Agentic AI & Tools        ──►  app/tools/calculator.py, Multi-turn Query Reformulation
M6: Capstone Integration      ──►  End-to-End System, Golden Evaluation Dataset & Pytest Suite
```

---

## 📘 Module 1: Python Fundamentals & Environment Setup

### 1. What You Learned:
* Running Python, managing virtual environments (`.venv`), and installing dependencies with `pip`.
* Basic data structures (`str`, `dict`, `list`) and reading text files using `open()` with context managers.

### 2. Where It Lives in DocuPilot:
* **[`.gitignore`](file:///Users/md.kamranalam/Programming/projects/docupilot/.gitignore)** & **[`requirements.txt`](file:///Users/md.kamranalam/Programming/projects/docupilot/requirements.txt)**: Isolating production dependencies from environment secrets (`.env`).
* **[`app/documents/parser.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/documents/parser.py)**: Demonstrates safe, native file reading and string manipulation across PDF, TXT, and Markdown documents using context managers (`with open(...) as f`).

```python
# From app/documents/parser.py (Module 1 in practice)
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()
```

---

## 📗 Module 2: Intermediate Python, OOP & APIs

### 1. What You Learned:
* Object-Oriented Programming (Classes, Methods, Encapsulation, Composition).
* REST APIs, HTTP methods (`GET`, `POST`, `DELETE`), status codes, JSON serialization.
* Asynchronous execution (`async` / `await`).

### 2. Where It Lives in DocuPilot:
* **OOP Services**:
  * [`app/llm/client.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/llm/client.py): An abstract base class `BaseLLMClient` with concrete implementations (`GroqLLMClient`, `OpenAILLMClient`, `MockLLMClient`) showing polymorphism and clean separation of concerns.
* **REST APIs**:
  * [`app/api/routes.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/api/routes.py): FastAPI endpoints handling document uploads, listing vector documents, deletion, and question querying.

---

## 📙 Module 3: Prompt Engineering in Practice

### 1. What You Learned:
* Structuring prompts using **Roles**, **Tasks**, **Context**, and **Constraints**.
* Using explicit delimiters (e.g. `[Source 1: ...]` or `<context>`) to separate instructions from retrieved data.
* Writing anti-hallucination instructions for unanswerable questions.

### 2. Where It Lives in DocuPilot:
Look at **[`app/llm/prompts.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/llm/prompts.py)**:

```python
RAG_SYSTEM_PROMPT = """You are DocuPilot, an accurate and grounded AI Document Assistant.
Your goal is to answer the user's questions based EXCLUSIVELY on the provided document excerpts below.

Follow these strict guidelines:
1. Groundedness: Rely strictly on facts directly mentioned in the Context.
2. Unanswerable Questions: If the context does not contain sufficient information, state:
   "The uploaded documents do not contain enough information to answer this question."
3. Source References: Explicitly reference document names and page numbers.
"""
```

---

## 📕 Module 4: Generative AI & RAG Application Development

### 1. What You Learned:
* **Embeddings**: Converting text into dense semantic vectors.
* **Vector Search**: Calculating cosine similarity to retrieve relevant text chunks.
* **RAG Pipeline**: Chunking $\to$ Embedding $\to$ Retrieval $\to$ Context Injection $\to$ Grounded LLM Generation.
* **User Interface**: Exposing the application via Streamlit.

### 2. Where It Lives in DocuPilot:
1. **Document Ingestion & Chunking**: [`app/documents/chunker.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/documents/chunker.py) uses a boundary-aware recursive sliding window.
2. **Local Embeddings**: [`app/embeddings/fastembed_service.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/embeddings/fastembed_service.py) uses CPU-optimized local FastEmbed models (no API key needed).
3. **Vector Database**: [`app/retrieval/vector_store.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/retrieval/vector_store.py) stores vectors in PostgreSQL using the `pgvector` `<=>` cosine distance operator.
4. **Interactive UI**: [`frontend/streamlit_app.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/frontend/streamlit_app.py) provides real-time token streaming with `st.write_stream` and expandable source citation cards.

---

## 📓 Module 5: Agentic AI, Tool Calling & State

### 1. What You Learned:
* Distinguishing between simple LLM calls, deterministic workflows, and dynamic agentic tools.
* Function/tool calling and execution loops.
* Managing conversation state across multi-turn sessions.

### 2. Where It Lives in DocuPilot:
1. **Safe Arithmetic Tool**: [`app/tools/calculator.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/tools/calculator.py) provides safe AST math evaluation when users ask for calculations over report data.
2. **Multi-Turn Query Reformulation**: [`app/services/qa_service.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/app/services/qa_service.py) automatically condenses multi-turn user follow-ups into standalone search queries before hitting the vector database.

```text
Turn 1: "What is the reimbursement period in the policy?"  ──► (Retrieves 45 days)
Turn 2: "Does it apply to activated software licenses?"
  ↓
Reformulated Query: "Does the 45-day reimbursement period apply to activated software licenses?"
```

---

## 🎓 Module 6: Capstone Evaluation & Benchmarking

### 1. What You Learned:
* System architecture planning and requirements definition.
* Testing your RAG system beyond simple manual "it worked once" checks.
* Benchmarking with golden evaluation datasets.

### 2. Where It Lives in DocuPilot:
* **Golden Evaluation Dataset**: [`tests/data/golden_dataset.json`](file:///Users/md.kamranalam/Programming/projects/docupilot/tests/data/golden_dataset.json).
* **Automated Evaluation Benchmark**: [`tests/integration/test_evaluation_benchmark.py`](file:///Users/md.kamranalam/Programming/projects/docupilot/tests/integration/test_evaluation_benchmark.py).
* **Running the test suite**:
```bash
pytest tests/
```

---

## 🚀 How to Run DocuPilot Locally

1. **Start the Database**:
   ```bash
   docker compose up -d
   ```
2. **Start the FastAPI Backend**:
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```
3. **Start the Streamlit Frontend**:
   ```bash
   source .venv/bin/activate
   streamlit run frontend/streamlit_app.py
   ```
