# 06 — Embedding Layer

## Embedding Providers (`app/embeddings/service.py`)
DocuPilot supports interchangeable embedding providers using the `BaseEmbeddingProvider` interface:

### 1. FastEmbed (Default — 100% Free & Local)
* **Model**: `BAAI/bge-small-en-v1.5`
* **Dimension**: 384
* **Runtime**: Lightweight ONNX runtime running locally on CPU.
* **Benefits**: Zero cost, no network latency, no external API keys required.

### 2. OpenAI Embedding
* **Model**: `text-embedding-3-small`
* **Dimension**: 1536
* **Provider**: OpenAI Cloud API.

### 3. Mock Provider
* Deterministic mathematical hash vector generator for offline testing and fast CI/CD pipelines.
