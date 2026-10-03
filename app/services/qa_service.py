from typing import List, Dict, Any, Optional, Iterator
import re
from sqlalchemy.orm import Session

from app.retrieval.retriever import Retriever
from app.llm.client import get_llm_client, BaseLLMClient
from app.llm.prompts import (
    RAG_SYSTEM_PROMPT,
    CONDENSE_QUESTION_PROMPT,
    build_rag_context,
    build_user_prompt
)
from app.llm.schemas import RAGAnswerResponse, SourceItem, ChatMessage
from app.tools.calculator import SafeCalculator


class QAService:
    """Orchestrates end-to-end RAG query flow with query condensation, tool handling, and streaming."""

    def __init__(self, db: Session, llm_client: Optional[BaseLLMClient] = None):
        self.retriever = Retriever(db)
        self.llm_client = llm_client or get_llm_client()

    def reformulate_query(
        self,
        question: str,
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> str:
        """Reformulates a follow-up question into a standalone search query if conversational context exists."""
        if not conversation_history or len(conversation_history) == 0:
            return question.strip()

        history_lines = []
        for m in conversation_history[-4:]:
            role_label = "User" if m.role.lower() == "user" else "Assistant"
            history_lines.append(f"{role_label}: {m.content}")
        history_text = "\n".join(history_lines)

        condense_prompt = CONDENSE_QUESTION_PROMPT.format(
            chat_history=history_text,
            question=question
        )

        try:
            standalone_query = self.llm_client.generate_answer(
                system_prompt="You are a query reformulation assistant. Output ONLY the standalone search query.",
                user_prompt=condense_prompt,
                chat_history=[]
            )
            return standalone_query.strip().replace('"', '') or question
        except Exception:
            return question

    def check_and_execute_tools(self, question: str) -> Optional[str]:
        """Checks if the query is a direct calculation and executes the calculator tool."""
        calc_patterns = [
            r"^(?:calculate|compute|what is|eval)\s+([0-9\+\-\*\/\(\)\.\s\^\%]+)$",
            r"^([0-9]+(?:\.[0-9]+)?\s*[\+\-\*\/]\s*[0-9]+(?:\.[0-9]+)?)$"
        ]
        q_lower = question.strip().lower()
        for pat in calc_patterns:
            match = re.search(pat, q_lower)
            if match:
                expr = match.group(1).strip()
                res = SafeCalculator.evaluate(expr)
                if res["success"]:
                    return f"**Calculation Result (Tool Execution):**\n`{res['expression']}` = **{res['formatted']}**"
        return None

    def prepare_rag_context(
        self,
        question: str,
        document_id: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        top_k: int = 4
    ) -> Dict[str, Any]:
        """Prepares standalone query, context chunks, and user prompts."""
        search_query = self.reformulate_query(question, conversation_history)
        chunks = self.retriever.retrieve(
            query=search_query,
            top_k=top_k,
            document_id=document_id
        )
        context_str = build_rag_context(chunks)
        user_prompt = build_user_prompt(question, context_str)
        history_list = []
        if conversation_history:
            history_list = [{"role": m.role, "content": m.content} for m in conversation_history]

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

        return {
            "search_query": search_query,
            "chunks": chunks,
            "sources": sources,
            "user_prompt": user_prompt,
            "history_list": history_list
        }

    def answer_question(
        self,
        question: str,
        document_id: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        top_k: int = 4
    ) -> RAGAnswerResponse:
        # Tool check first (M5 Agent Tool Calling)
        tool_result = self.check_and_execute_tools(question)
        if tool_result:
            return RAGAnswerResponse(
                question=question,
                answer=tool_result,
                confidence="high",
                sources=[]
            )

        rag_data = self.prepare_rag_context(question, document_id, conversation_history, top_k)

        answer = self.llm_client.generate_answer(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=rag_data["user_prompt"],
            chat_history=rag_data["history_list"]
        )

        confidence = "high" if len(rag_data["chunks"]) > 0 and "not contain enough information" not in answer.lower() else "unanswerable"

        return RAGAnswerResponse(
            question=question,
            answer=answer,
            confidence=confidence,
            sources=rag_data["sources"]
        )

    def stream_question(
        self,
        question: str,
        document_id: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        top_k: int = 4
    ) -> Iterator[str]:
        tool_result = self.check_and_execute_tools(question)
        if tool_result:
            yield tool_result
            return

        rag_data = self.prepare_rag_context(question, document_id, conversation_history, top_k)
        for token in self.llm_client.stream_answer(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=rag_data["user_prompt"],
            chat_history=rag_data["history_list"]
        ):
            yield token

