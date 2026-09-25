from typing import List, Dict, Any


class TextChunker:
    """
    Splits text into chunks of specified maximum character size with overlap.
    Uses paragraph/sentence/word boundary awareness to avoid breaking words mid-sentence.
    """

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            if end >= text_length:
                chunks.append(text[start:].strip())
                break

            # Look for suitable split point: paragraph -> sentence -> space
            split_at = -1
            sub_slice = text[start:end]

            # 1. Paragraph boundary
            nl_pos = sub_slice.rfind("\n\n")
            if nl_pos > int(self.chunk_size * 0.4):
                split_at = start + nl_pos + 2
            else:
                # 2. Sentence boundary
                for punct in [". ", "? ", "! "]:
                    punct_pos = sub_slice.rfind(punct)
                    if punct_pos > int(self.chunk_size * 0.4):
                        split_at = max(split_at, start + punct_pos + len(punct))

                # 3. Fall back to word boundary (space)
                if split_at == -1:
                    space_pos = sub_slice.rfind(" ")
                    if space_pos > int(self.chunk_size * 0.4):
                        split_at = start + space_pos + 1
                    else:
                        split_at = end

            chunk_text = text[start:split_at].strip()
            if chunk_text:
                chunks.append(chunk_text)

            # Move forward taking overlap into account
            start = max(start + 1, split_at - self.chunk_overlap)

        return chunks

    def chunk_document_pages(
        self, pages_data: List[Dict[str, Any]], document_id: str, filename: str
    ) -> List[Dict[str, Any]]:
        """
        Takes raw page objects ({text, page}) and produces chunks with full metadata.
        """
        all_chunks = []
        global_chunk_index = 0

        for page_item in pages_data:
            page_num = page_item.get("page", 1)
            raw_text = page_item.get("text", "")
            page_chunks = self.split_text(raw_text)

            for chunk_str in page_chunks:
                all_chunks.append({
                    "document_id": document_id,
                    "content": chunk_str,
                    "chunk_index": global_chunk_index,
                    "page": page_num,
                    "metadata": {
                        "filename": filename,
                        "page": page_num,
                        "chunk_index": global_chunk_index,
                        "char_count": len(chunk_str)
                    }
                })
                global_chunk_index += 1

        return all_chunks
