# 10 — Evaluation Framework

## Evaluation Dimensions
1. **Context Recall**: Did the vector search retrieve the actual chunk containing the answer?
2. **Context Precision**: Are the top-$K$ chunks free of noisy and irrelevant passages?
3. **Faithfulness / Groundedness**: Is every statement in the LLM answer directly verifiable in the context?
4. **Answer Relevance**: Does the generated answer address the user's specific question?
5. **Anti-Hallucination & Tool Accuracy**: Does the system refuse out-of-context queries and correctly invoke arithmetic tools when asked?

## Golden Evaluation Dataset & Verification Suite
* **Golden Evaluation Dataset (`tests/data/golden_dataset.json`)**: Benchmarks direct factual retrieval, numerical tool execution, and out-of-domain unanswerable queries.
* **Unit Tests (`tests/unit/`)**: Verifies parser page tracking, chunk splitting, tool execution, and multi-turn query reformulation.
* **Integration Tests (`tests/integration/`)**: End-to-end testing of document upload, pgvector indexing, streaming, benchmark evaluation, and document deletion.
* **Run Test Suite**:
  ```bash
  source .venv/bin/activate
  PYTHONPATH=. pytest tests/
  ```

