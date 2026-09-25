# 04 — Document Processing Pipeline

## Document Parser (`app/documents/parser.py`)
Extracts raw text while maintaining pagination and structure:
* **PDF Processing**: Utilizes `pypdf.PdfReader` to extract text page-by-page.
* **Plain Text (`.txt`)**: UTF-8 stream reader with fallback character decoding.
* **Markdown (`.md`)**: Preserves document sections and markdown headers.

## Text Cleaning (`app/documents/cleaner.py`)
Sanitizes raw strings before embedding generation:
1. Strips null bytes (`\x00`).
2. Normalizes Windows (`\r\n`) and old Mac (`\r`) newlines to `\n`.
3. Replaces consecutive tab and space characters with a single space.
4. Trims leading and trailing whitespace on individual lines.
5. Collapses excessive blank lines ($>2$ newlines $\rightarrow 2$).
