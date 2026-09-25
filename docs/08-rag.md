# 08 — RAG Pipeline Execution

## End-to-End Execution Flow (`app/services/qa_service.py`)

1. **User Query Ingestion**: The API receives a question along with optional document focus filter and chat history.
2. **Query Vectorization**: The embedding provider generates a dense vector representing the question's semantic intent.
3. **Candidate Retrieval**: `Retriever` fetches the Top-$K$ (default: 4) chunks with the highest cosine similarity.
4. **Context Assembly**: `build_rag_context` formats chunks into delimited source blocks:
   ```text
   [Source 1: refund_policy.pdf (Page: 2)]
   Customers may request reimbursement within 45 days...
   ```
5. **Prompt Injection & LLM Inference**: The system prompt enforces factual grounding and strict adherence to provided passages.
6. **Citation Extraction & Validation**: Returns response payload with answer, confidence rating, and structured source references (filename, page, excerpt, and similarity score).
