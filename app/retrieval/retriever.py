from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.retrieval.vector_store import VectorStore


class Retriever:
    """Orchestrates document chunk retrieval with score thresholds and formatting."""

    def __init__(self, db: Session):
        self.vector_store = VectorStore(db)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        score_threshold: float = 0.0,
        document_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = self.vector_store.similarity_search(
            query=query,
            top_k=top_k,
            document_id=document_id
        )
        # Filter by optional threshold
        filtered = [r for r in results if r["similarity_score"] >= score_threshold]
        return filtered
