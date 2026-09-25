import pytest
from app.documents.cleaner import TextCleaner
from app.documents.chunker import TextChunker


def test_text_cleaner():
    dirty_text = "Hello\x00 world!\r\n\n\nThis is   a   test.  \n\n\n\nNew paragraph."
    cleaned = TextCleaner.clean(dirty_text)
    assert "\x00" not in cleaned
    assert "\r" not in cleaned
    assert "   " not in cleaned
    assert "Hello world!\n\nThis is a test.\n\nNew paragraph." == cleaned


def test_text_chunker_basic():
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)
    text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
    chunks = chunker.split_text(text)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 60


def test_text_chunker_metadata():
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    pages = [
        {"page": 1, "text": "Page one text content that should be split into chunks."},
        {"page": 2, "text": "Page two text content that also gets processed."}
    ]
    chunks = chunker.chunk_document_pages(pages, document_id="doc_123", filename="test.pdf")
    assert len(chunks) >= 2
    assert chunks[0]["document_id"] == "doc_123"
    assert chunks[0]["page"] == 1
    assert chunks[0]["metadata"]["filename"] == "test.pdf"
    assert chunks[1]["document_id"] == "doc_123"
