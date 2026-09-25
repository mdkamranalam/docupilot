from typing import List, Optional
from pydantic import BaseModel, Field


class SourceItem(BaseModel):
    document_id: str
    filename: str
    page: Optional[int] = None
    chunk_index: int
    excerpt: str
    similarity_score: float = Field(default=0.0)


class RAGAnswerResponse(BaseModel):
    question: str
    answer: str
    confidence: str = Field(description="Confidence rating: high, medium, low, or unanswerable")
    sources: List[SourceItem] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str


class ChatQueryRequest(BaseModel):
    question: str
    document_id: Optional[str] = None
    conversation_history: List[ChatMessage] = Field(default_factory=list)
    top_k: int = 4
