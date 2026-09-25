# 03 — Architecture & Component Design

```
+-------------------------------------------------------------+
|                        Streamlit UI                         |
|  - Document Management Vault   - Chat & Source Accordion   |
+------------------------------+------------------------------+
                               | REST (HTTP)
                               v
+-------------------------------------------------------------+
|                     FastAPI Application                     |
|  - POST /api/v1/documents/upload                            |
|  - GET  /api/v1/documents                                   |
|  - DELETE /api/v1/documents/{id}                            |
|  - POST /api/v1/chat/query                                  |
+------------------------------+------------------------------+
                               |
         +---------------------+---------------------+
         |                                           |
         v                                           v
+---------------------+                     +------------------+
| Ingestion Pipeline  |                     |  RAG QA Service  |
| - DocumentParser    |                     | - Retriever      |
| - TextCleaner       |                     | - ContextBuilder |
| - TextChunker       |                     | - LLM Client     |
+----------+----------+                     +--------+---------+
           |                                         |
           v                                         v
+-------------------------------------------------------------+
|                     PostgreSQL + pgvector                   |
|  - documents (id, filename, file_type, metadata)            |
|  - chunks    (id, doc_id, content, embedding vector(384))   |
+-------------------------------------------------------------+
```

## Data Flow
1. **Ingestion**: File $\rightarrow$ `DocumentParser` $\rightarrow$ `TextCleaner` $\rightarrow$ `TextChunker` $\rightarrow$ `FastEmbed` $\rightarrow$ `pgvector`.
2. **Query**: User Question $\rightarrow$ `FastEmbed` $\rightarrow$ `VectorStore` (Cosine Search) $\rightarrow$ Top-$K$ Chunks $\rightarrow$ `ContextBuilder` $\rightarrow$ `Groq LLM Client` $\rightarrow$ Grounded Answer + Citations.
