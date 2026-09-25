# 02 — Requirements & System Specifications

## Functional Requirements
1. **Multi-Format Ingestion**: Support `.pdf`, `.txt`, and `.md` files with page-level tracking.
2. **Text Normalization**: Strip null bytes, normalize whitespace, and remove encoding artifacts.
3. **Semantic Chunking**: Split text into configurable character chunks (e.g. 800 chars) with sliding-window overlap (150 chars) while respecting sentence/paragraph boundaries.
4. **Vector Storage**: Persist dense vector embeddings with metadata in PostgreSQL via `pgvector`.
5. **Semantic Retrieval**: Top-$K$ similarity search with cosine distance scoring and document-level filtering.
6. **Strict Grounding**: Provide deterministic answers citing document names and page numbers, admitting when context is absent.
7. **Conversational Memory**: Maintain multi-turn context across consecutive user queries.
8. **User Interface**: Streamlit dashboard for document upload, vault management, and conversational Q&A.

## Non-Functional Requirements
1. **Low Latency**: Sub-second retrieval with pgvector indexing and fast inference providers (Groq / FastEmbed).
2. **Zero-Cost Operation**: Native support for free-tier LLMs (Groq) and local CPU-based embedding generation (`fastembed`).
3. **Security & Isolation**: Dockerized database, parameter validation with Pydantic, and automatic cleanup of temporary upload files.
