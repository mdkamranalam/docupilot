# 10 — Evaluation Framework

## Evaluation Dimensions
1. **Context Recall**: Did the vector search retrieve the actual chunk containing the answer?
2. **Context Precision**: Are the top-$K$ chunks free of noisy and irrelevant passages?
3. **Faithfulness / Groundedness**: Is every statement in the LLM answer directly verifiable in the context?
4. **Answer Relevance**: Does the generated answer address the user's specific question?

## Automated Verification Suite
* **Unit Tests (`tests/unit/`)**: Verifies parser page tracking, cleaner whitespace normalization, and boundary-aware chunk splitting.
* **Integration Tests (`tests/integration/`)**: End-to-end testing of document upload, pgvector indexing, RAG querying with citations, and document deletion.
* **Command**:
  ```bash
  source .venv/bin/activate
  PYTHONPATH=. pytest tests/
  ```
