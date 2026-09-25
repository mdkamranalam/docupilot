from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from openai import OpenAI
from app.config.settings import settings


class BaseLLMClient(ABC):
    @abstractmethod
    def generate_answer(
        self,
        system_prompt: str,
        user_prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        pass


class GroqLLMClient(BaseLLMClient):
    """
    100% Free Tier LLM client using Groq Cloud API.
    Groq provides OpenAI-compatible endpoints with ultra-fast inference.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.LLM_MODEL
        self.client = (
            OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.api_key
            )
            if self.api_key and self.api_key != "gsk_your_groq_api_key_here"
            else None
        )

    def generate_answer(
        self,
        system_prompt: str,
        user_prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not set. Get a free API key at https://console.groq.com/keys and paste it in your .env file."
            )

        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for turn in chat_history[-6:]:
                messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()


class OpenAILLMClient(BaseLLMClient):
    """OpenAI LLM implementation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.LLM_MODEL
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_answer(
        self,
        system_prompt: str,
        user_prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not set.")

        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for turn in chat_history[-6:]:
                messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()


class MockLLMClient(BaseLLMClient):
    """Fallback when no API key is provided."""

    def generate_answer(
        self,
        system_prompt: str,
        user_prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        if "No relevant context" in user_prompt:
            return "The uploaded documents do not contain enough information to answer this question."
        return "According to the uploaded documents, this is a simulated grounded answer based on the retrieved context."


def get_llm_client() -> BaseLLMClient:
    if settings.LLM_PROVIDER == "groq" and settings.GROQ_API_KEY and settings.GROQ_API_KEY != "gsk_your_groq_api_key_here":
        return GroqLLMClient()
    elif settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
        return OpenAILLMClient()
    return MockLLMClient()
