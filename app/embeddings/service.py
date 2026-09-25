from abc import ABC, abstractmethod
from typing import List, Optional
from openai import OpenAI
from app.config.settings import settings


class BaseEmbeddingProvider(ABC):
    """Abstract base class for generating text embeddings."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass


class FastEmbedProvider(BaseEmbeddingProvider):
    """
    100% Free, local embedding provider using fastembed (ONNX runtime).
    Zero API keys required.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        try:
            from fastembed import TextEmbedding
            self.model = TextEmbedding(model_name=self.model_name)
        except ImportError:
            self.model = None

    def embed_text(self, text: str) -> List[float]:
        if not self.model:
            from fastembed import TextEmbedding
            self.model = TextEmbedding(model_name=self.model_name)
        embeddings = list(self.model.embed([text]))
        return embeddings[0].tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        if not self.model:
            from fastembed import TextEmbedding
            self.model = TextEmbedding(model_name=self.model_name)
        embeddings = list(self.model.embed(texts))
        return [e.tolist() for e in embeddings]


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """OpenAI Embedding implementation."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.EMBEDDING_MODEL
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def embed_text(self, text: str) -> List[float]:
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not set.")
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not self.client or not texts:
            return []
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """Deterministic fallback mock."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def embed_text(self, text: str) -> List[float]:
        val = (hash(text) % 1000) / 1000.0
        return [val] * self.dimension

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


def get_embedding_provider() -> BaseEmbeddingProvider:
    if settings.EMBEDDING_PROVIDER == "fastembed":
        try:
            return FastEmbedProvider()
        except Exception:
            return MockEmbeddingProvider(dimension=settings.EMBEDDING_DIMENSION)
    elif settings.EMBEDDING_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        return OpenAIEmbeddingProvider()
    return MockEmbeddingProvider(dimension=settings.EMBEDDING_DIMENSION)
