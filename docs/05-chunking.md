# 05 — Chunking Strategies & Decisions

## Chunking Algorithm (`app/documents/chunker.py`)
DocuPilot uses a boundary-aware recursive sliding window approach rather than arbitrary character slicing:

1. **Target Chunk Size**: Defaults to `800` characters.
2. **Chunk Overlap**: Defaults to `150` characters. Overlap prevents critical context from being split across chunk boundaries.
3. **Boundary Priority**:
   * **Paragraph Boundary (`\n\n`)**: Splits at paragraph breaks when available in the search window.
   * **Sentence Boundary (`. `, `? `, `! `)**: Falls back to sentence terminators.
   * **Word Boundary (` `)**: Falls back to spaces to prevent truncating words in half.

## Preserved Chunk Metadata
Every chunk persists:
* `document_id`: UUID of parent document.
* `page`: Source page number (for PDFs).
* `chunk_index`: Monotonically increasing index across the document.
* `char_count`: Total character length.
