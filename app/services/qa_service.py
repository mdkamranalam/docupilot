from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.retrieval.retriever import Retriever
from app.llm.client import get_llm_client, BaseLLMClient
from app.llm.prompts import RAG_SYSTEM_PROMPT, build_rag_context, build_user_prompt
from app.llm.schemas import RAGAnswerResponse, SourceItem, ChatMessage


class QAService:
    """Orchestrates end-to-end RAG query flow."""

    def __init__(self, db: Session, llm_client: Optional[BaseLLMClient] = None):
        self.retriever = Retriever(db)
        self.llm_client = llm_client or get_llm_client()

    def answer_question(
        self,
        question: str,
        document_id: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        top_k: int = 4
    ) -> RAGAnswerResponse:
        # 1. Retrieve top-k relevant chunks
        chunks = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            document_id=document_id
        )

        # 2. Build context
        context_str = build_rag_context(chunks)

        # 3. Format user prompt
        user_prompt = build_user_prompt(question, context_str)

        # 4. Format chat history
        history_list = []
        if conversation_history:
            history_list = [{"role": m.role, "content": m.content} for m in conversation_history]

        # 5. Generate answer from LLM
        answer = self.llm_client.generate_answer(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            chat_history=history_list
        )

        # 6. Format source citations
        sources = []
        for c in chunks:
            sources.append(
                SourceItem(
                    document_id=c["document_id"],
                    filename=c["filename"],
                    page=c.get("page"),
                    chunk_index=c["chunk_index"],
                    excerpt=c["content"][:200] + "..." if len(c["content"]) > 200 else c["content"],
                    similarity_score=round(c.get("similarity_score", 0.0), 4)
                )
            )

        # 7. Evaluate confidence rating
        confidence = "high" if len(chunks) > 0 and "not contain enough information" not in answer.lower() else "unanswerable"

        return RAGAnswerResponse(
            question=question,
            answer=answer,
            confidence=confidence,
            sources=sources
        )
