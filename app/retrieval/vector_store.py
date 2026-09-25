from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.document import Chunk, Document
from app.embeddings.service import BaseEmbeddingProvider, get_embedding_provider


class VectorStore:
    """Handles storage and cosine similarity retrieval for chunks in PostgreSQL + pgvector."""

    def __init__(self, db: Session, embedding_provider: Optional[BaseEmbeddingProvider] = None):
        self.db = db
        self.embedding_provider = embedding_provider or get_embedding_provider()

    def store_chunks(self, chunks_data: List[Dict[str, Any]]) -> None:
        """Embeds and persists chunks into PostgreSQL."""
        if not chunks_data:
            return

        texts_to_embed = [c["content"] for c in chunks_data]
        embeddings = self.embedding_provider.embed_batch(texts_to_embed)

        for chunk_info, emb in zip(chunks_data, embeddings):
            chunk_obj = Chunk(
                document_id=chunk_info["document_id"],
                content=chunk_info["content"],
                embedding=emb,
                chunk_index=chunk_info["chunk_index"],
                page=chunk_info.get("page"),
                chunk_metadata=chunk_info.get("metadata", {})
            )
            self.db.add(chunk_obj)

        self.db.commit()

    def similarity_search(
        self,
        query: str,
        top_k: int = 4,
        document_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculates cosine distance (<=> operator in pgvector) against chunk embeddings.
        Returns top-k most relevant chunks with similarity scores.
        """
        query_embedding = self.embedding_provider.embed_text(query)
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        # SQL query using pgvector cosine distance operator (<=>)
        # Cosine Similarity = 1 - Cosine Distance
        sql_query = """
            SELECT 
                c.id,
                c.document_id,
                d.filename,
                c.content,
                c.page,
                c.chunk_index,
                c.metadata,
                1 - (c.embedding <=> :query_embedding) AS similarity_score
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
        """

        params = {"query_embedding": embedding_str, "top_k": top_k}

        if document_id:
            sql_query += " WHERE c.document_id = :doc_id"
            params["doc_id"] = document_id

        sql_query += " ORDER BY c.embedding <=> :query_embedding ASC LIMIT :top_k"

        results = self.db.execute(text(sql_query), params).mappings().all()

        formatted_results = []
        for row in results:
            formatted_results.append({
                "chunk_id": row["id"],
                "document_id": row["document_id"],
                "filename": row["filename"],
                "content": row["content"],
                "page": row["page"],
                "chunk_index": row["chunk_index"],
                "similarity_score": float(row["similarity_score"]) if row["similarity_score"] is not None else 0.0,
                "metadata": row["metadata"] or {}
            })

        return formatted_results
