# 07 — Semantic Retrieval & pgvector Integration

## Vector Database Architecture (`app/retrieval/vector_store.py`)
DocuPilot stores embeddings directly in PostgreSQL using the `pgvector` extension.

### Schema Definition
```sql
CREATE TABLE chunks (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(384),
    chunk_index INTEGER NOT NULL,
    page INTEGER,
    metadata JSON
);
```

### Cosine Distance Similarity Query
Retrieval uses PostgreSQL's native cosine distance operator `<=>`:
```sql
SELECT 
    c.id,
    c.document_id,
    d.filename,
    c.content,
    c.page,
    c.chunk_index,
    1 - (c.embedding <=> :query_embedding) AS similarity_score
FROM chunks c
JOIN documents d ON c.document_id = d.id
WHERE (:doc_id IS NULL OR c.document_id = :doc_id)
ORDER BY c.embedding <=> :query_embedding ASC
LIMIT :top_k;
```
* **Similarity Calculation**: `Similarity = 1 - Cosine Distance`.
