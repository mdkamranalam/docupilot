import os
import re
from typing import List, Dict, Any
from pypdf import PdfReader


class DocumentParser:
    """Extracts raw text and metadata from PDF, TXT, and Markdown files."""

    @staticmethod
    def parse_txt(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return [{"text": text, "page": 1}]

    @staticmethod
    def parse_markdown(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return [{"text": text, "page": 1}]

    @staticmethod
    def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
        reader = PdfReader(file_path)
        pages_data = []
        for index, page in enumerate(reader.pages):
            extracted = page.extract_text() or ""
            pages_data.append({
                "text": extracted,
                "page": index + 1
            })
        return pages_data

    @classmethod
    def parse(cls, file_path: str) -> List[Dict[str, Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return cls.parse_pdf(file_path)
        elif ext in [".txt"]:
            return cls.parse_txt(file_path)
        elif ext in [".md", ".markdown"]:
            return cls.parse_markdown(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported: .pdf, .txt, .md")
