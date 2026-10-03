from typing import List, Dict, Any

RAG_SYSTEM_PROMPT = """You are DocuPilot, an accurate and grounded AI Document Assistant.
Your goal is to answer the user's questions based EXCLUSIVELY on the provided document excerpts below.

Follow these strict guidelines:
1. Groundedness: Rely strictly on facts directly mentioned in the Context. Do not extrapolate, assume, or invent details not present in the text.
2. Unanswerable Questions: If the context does not contain sufficient information to answer the question, clearly state: "The uploaded documents do not contain enough information to answer this question."
3. Source References: Explicitly reference the document name and page number when citing facts.
4. Tone: Clear, objective, concise, and professional.
"""

CONDENSE_QUESTION_PROMPT = """Given the following conversation history and a follow-up question from the user, rephrase the follow-up question to be a standalone search query that contains all necessary context for document retrieval.

Do NOT answer the question. Only return the reformulated standalone query. If the question is already standalone, return it as-is.

Conversation History:
{chat_history}

Follow-up Question: {question}
Standalone Search Query:"""


def build_rag_context(chunks: List[Dict[str, Any]]) -> str:
    """Formats retrieved chunks into a clean context block with clear source markers."""
    if not chunks:
        return "No relevant context found in uploaded documents."

    context_parts = []
    for idx, chunk in enumerate(chunks, start=1):
        filename = chunk.get("filename", "Unknown Document")
        page = chunk.get("page", "N/A")
        content = chunk.get("content", "").strip()
        context_parts.append(
            f"[Source {idx}: {filename} (Page: {page})]\n{content}"
        )

    return "\n\n---\n\n".join(context_parts)


def build_user_prompt(question: str, context: str) -> str:
    return f"""Context:
{context}

Question:
{question}

Answer:"""

