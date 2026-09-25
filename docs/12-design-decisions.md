# 12 — Architectural & Engineering Design Decisions

## 1. PostgreSQL + `pgvector` vs. Dedicated Vector DBs (Pinecone/Chroma)
* **Rationale**: PostgreSQL provides a single production-grade ACID database for both relational metadata (`documents`) and vector embeddings (`chunks`), eliminating dual-database synchronization complexity.

## 2. FastEmbed for Local Embeddings vs. Cloud API Embeddings
* **Rationale**: FastEmbed runs ONNX-quantized models (`bge-small-en-v1.5`) directly on CPU with near-zero latency, zero API costs, and no rate limiting.

## 3. Groq Cloud API for LLMs
* **Rationale**: Groq provides ultra-fast inference speeds with an OpenAI-compatible API format and generous free-tier limits.

## 4. FastAPI + Streamlit
* **Rationale**: Clean separation of concerns between backend API microservice (`FastAPI`) and rapid interactive frontend prototyping (`Streamlit`).
