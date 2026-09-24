# DocuPilot — GenAI Project Overview

## 1. Project Title

**DocuPilot — AI-Powered Document Intelligence & Knowledge Assistant**

## 2. Project Type

**Generative AI / RAG Application**

DocuPilot is a document-based knowledge assistant that allows users to upload documents, retrieve relevant information from them, ask questions in natural language, and receive grounded answers with source references.

## 3. Problem Statement

Organizations and individuals often have large collections of documents containing useful information, but finding specific information manually can be slow and inefficient.

Traditional keyword search also has limitations because users may ask questions using different words from those used in the documents.

DocuPilot addresses this by combining:

* Document processing
* Semantic search
* Embeddings
* Vector search
* Retrieval-Augmented Generation (RAG)
* Large Language Models
* Conversation state
* Source attribution

## 4. Core Objective

Build a GenAI application that can:

> **Understand a user's document collection, retrieve relevant information, and generate accurate, context-grounded answers based on that information.**

The system should prioritize information retrieved from the user's documents instead of relying solely on the LLM's pretrained knowledge.

---

# 5. Core User Flow

```text
User
 │
 ├── Upload Documents
 │
 ▼
Document Processing
 │
 ├── Extract Text
 ├── Clean Text
 └── Create Metadata
 │
 ▼
Chunking
 │
 ▼
Embedding Generation
 │
 ▼
Vector Database
 │
 │
 └─────────────────────────────┐
                               │
User asks question             │
 │                             │
 ▼                             │
Query Embedding                │
 │                             │
 ▼                             │
Semantic Retrieval ◄───────────┘
 │
 ▼
Relevant Chunks
 │
 ▼
Context Construction
 │
 ▼
LLM
 │
 ▼
Grounded Answer
 │
 ▼
Source References
```

---

# 6. Key Features

### Document Management

* Upload documents
* Support PDF, TXT and Markdown initially
* Document metadata
* Document identification
* Document deletion/reprocessing

### Document Processing

* Text extraction
* Text cleaning
* Chunking
* Metadata generation
* Embedding generation
* Vector storage

### Semantic Search

Users can ask questions using natural language.

Example:

> "What is the refund period?"

Even if the document says:

> "Customers may request reimbursement within 30 calendar days."

semantic retrieval can identify the relevant passage.

### RAG Question Answering

The system retrieves relevant document chunks and provides them to the LLM as context.

```text
Question
   ↓
Retrieval
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

### Source Attribution

Each answer should identify the document/chunk used to generate the response.

Example:

```text
Answer:
Customers can request a refund within 30 days.

Sources:
• refund-policy.pdf — Section 4
• customer-policy.pdf — Page 12
```

### Conversational Context

Users should be able to ask follow-up questions.

```text
User:
What is the refund period?

Assistant:
The refund period is 30 days.

User:
Does this apply to digital products?

Assistant:
According to the uploaded policy...
```

The application maintains the relevant conversation context.

---

# 7. High-Level Architecture

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Streamlit   │
                         │      UI      │
                         └──────┬───────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │ Application Layer  │
                     └─────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   Document Service      Retrieval Service     LLM Service
          │                    │                    │
          ▼                    ▼                    ▼
   Document Parser       Vector Database        LLM API
          │                    │                    │
          ▼                    │                    │
       Chunking                │                    │
          │                    │                    │
          ▼                    │                    │
      Embeddings ──────────────┘                    │
                               │                    │
                               └─────────┬──────────┘
                                         ▼
                                      Response
                                         │
                                         ▼
                                      Sources
```

---

# 8. RAG Architecture

DocuPilot's central technical component is the RAG pipeline.

## Ingestion Pipeline

```text
Document
   ↓
Parser
   ↓
Text
   ↓
Cleaner
   ↓
Chunker
   ↓
Chunks + Metadata
   ↓
Embedding Model
   ↓
Vectors
   ↓
Vector Database
```

## Query Pipeline

```text
User Question
      ↓
Query Processing
      ↓
Query Embedding
      ↓
Vector Search
      ↓
Top-K Chunks
      ↓
Context Builder
      ↓
Prompt
      ↓
LLM
      ↓
Answer + Sources
```

---

# 9. Chunking Strategy

DocuPilot should explicitly treat chunking as an engineering decision.

The project should experiment with:

* Chunk size
* Chunk overlap
* Paragraph-based splitting
* Section-aware splitting
* Metadata preservation

Each chunk should retain useful metadata such as:

```json
{
  "document_id": "doc_001",
  "document_name": "refund-policy.pdf",
  "page": 12,
  "section": "Refund Policy",
  "chunk_index": 8
}
```

This metadata can later be used for retrieval filtering and source attribution.

---

# 10. Embedding Layer

Text is converted into numerical vector representations.

```text
"Refund policy"
       ↓
Embedding Model
       ↓
[0.13, -0.42, 0.81, ...]
```

The same process is applied to the user's query.

```text
Query
 ↓
Embedding
 ↓
Vector Similarity
 ↓
Relevant Chunks
```

The project should make the embedding and retrieval process visible rather than hiding everything behind a single high-level framework call.

---

# 11. Vector Database

The vector database stores:

```text
Document
Chunk
Embedding
Metadata
```

Example conceptual schema:

```text
documents
├── id
├── filename
├── file_type
├── uploaded_at
└── metadata

chunks
├── id
├── document_id
├── content
├── embedding
├── chunk_index
├── page
└── metadata
```

A suitable implementation for the reference project is:

**PostgreSQL + pgvector**

This also gives the project a conventional relational database alongside vector search.

---

# 12. LLM Layer

The LLM should not directly receive the entire document collection.

Instead:

```text
User Question
      ↓
Retriever
      ↓
Relevant Chunks
      ↓
Context
      ↓
LLM
```

A conceptual prompt:

```text
System:
Answer using the supplied document context.

Context:
[Retrieved document chunks]

Question:
[User question]

Instructions:
- Use the provided context.
- Do not invent unsupported information.
- If the information is unavailable, say so.
- Identify the relevant sources.
```

The exact prompt should be versioned and evaluated.

---

# 13. Structured Output

Where useful, DocuPilot can request a structured response such as:

```json
{
  "answer": "Customers can request a refund within 30 days.",
  "confidence": "high",
  "sources": [
    {
      "document": "refund-policy.pdf",
      "page": 12
    }
  ]
}
```

The application then validates the response before displaying it.

```text
LLM
 ↓
Structured Output
 ↓
Schema Validation
 ├── Valid → Application
 └── Invalid → Error / Retry
```

This demonstrates the transition from probabilistic model output to application-level data.

---

# 14. Conversation Management

DocuPilot should support multi-turn conversations.

Conceptually:

```text
Session
 │
 ├── User Message
 ├── Assistant Response
 ├── User Follow-up
 ├── Assistant Response
 └── ...
```

The application should manage context rather than continuously sending unlimited history.

Possible future improvements include:

* Conversation summarization
* Context truncation
* Relevant-history retrieval

---

# 15. Evaluation

Evaluation should be a major part of the project documentation.

Create a test dataset containing questions with known expected information.

Example:

| Question                          | Expected Source   | Expected Information     |
| --------------------------------- | ----------------- | ------------------------ |
| What is the refund period?        | refund-policy.pdf | 30 days                  |
| Who is eligible?                  | eligibility.pdf   | Eligible customers       |
| Can digital products be refunded? | refund-policy.pdf | Policy-specific answer   |
| What happens after 30 days?       | refund-policy.pdf | Policy-specific response |

Evaluate:

* Retrieval relevance
* Answer correctness
* Context relevance
* Groundedness
* Source accuracy
* Format compliance
* Failure cases

---

# 16. Failure Modes to Document

DocuPilot should explicitly demonstrate that RAG does not automatically guarantee correctness.

Important failure cases:

### Poor retrieval

```text
Question
 ↓
Wrong chunks retrieved
 ↓
LLM receives irrelevant context
 ↓
Poor answer
```

### Poor chunking

Important information may be split across chunks.

### Missing information

The documents may simply not contain the answer.

The application should respond accordingly rather than inventing information.

### Excessive context

Too many retrieved chunks can introduce noise.

### Ambiguous questions

The system may need clarification.

### Conflicting documents

Two documents may provide different information.

The application should expose or handle this situation explicitly.

---

# 17. Suggested Technology Stack

### Backend

* Python
* FastAPI
* Pydantic

### LLM

* Configurable LLM provider
* Provider abstraction through an internal LLM service

### Embeddings

* Configurable embedding model

### Database

* PostgreSQL
* pgvector

### Document Processing

* PDF parser
* Text/Markdown processing

### Frontend

* Streamlit

### Testing

* pytest

### Infrastructure

* Docker
* Docker Compose

### Version Control

* Git
* GitHub

---

# 18. Proposed Repository Structure

```text
docupilot/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── documents/
│   │   ├── parser.py
│   │   ├── cleaner.py
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   └── service.py
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   ├── prompts.py
│   │   └── schemas.py
│   │
│   ├── conversations/
│   │   └── service.py
│   │
│   ├── services/
│   │   └── qa_service.py
│   │
│   └── main.py
│
├── frontend/
│   └── streamlit_app.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│
├── docs/
│   ├── 01-problem.md
│   ├── 02-requirements.md
│   ├── 03-architecture.md
│   ├── 04-document-processing.md
│   ├── 05-chunking.md
│   ├── 06-embeddings.md
│   ├── 07-retrieval.md
│   ├── 08-rag.md
│   ├── 09-prompt-design.md
│   ├── 10-evaluation.md
│   ├── 11-failure-modes.md
│   └── 12-design-decisions.md
│
├── data/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── AGENTS.md
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── LICENSE
```

---

# 19. Documentation Requirements

The project documentation should explain both **implementation and engineering reasoning**.

### README.md

```text
1. Project Overview
2. Problem Statement
3. Solution
4. Features
5. Architecture
6. RAG Pipeline
7. Technology Stack
8. Project Structure
9. Installation
10. Environment Variables
11. Running Locally
12. Example Usage
13. Testing
14. Evaluation
15. Limitations
16. Future Improvements
```

### Architecture Documentation

Explain:

* Component responsibilities
* Data flow
* Ingestion pipeline
* Query pipeline
* Database architecture
* LLM interaction
* UI/backend interaction

### Design Decisions

Document decisions such as:

```text
Why PostgreSQL + pgvector?
Why this chunking strategy?
Why this embedding model?
Why RAG?
Why FastAPI?
Why Streamlit?
Why provider abstraction?
```

---

# 20. Project Milestones

### Phase 1 — Foundation

```text
Project Setup
 ↓
FastAPI
 ↓
Database
 ↓
Configuration
```

### Phase 2 — Document Pipeline

```text
Upload
 ↓
Parse
 ↓
Clean
 ↓
Chunk
 ↓
Store
```

### Phase 3 — Retrieval

```text
Embeddings
 ↓
Vector Store
 ↓
Similarity Search
 ↓
Top-K Retrieval
```

### Phase 4 — RAG

```text
Question
 ↓
Retrieve
 ↓
Context
 ↓
LLM
 ↓
Answer
```

### Phase 5 — Application

```text
Conversation
 ↓
Structured Output
 ↓
Source Attribution
 ↓
Error Handling
```

### Phase 6 — UI

```text
Streamlit
 ↓
Upload
 ↓
Chat
 ↓
Sources
```

### Phase 7 — Evaluation

```text
Test Dataset
 ↓
Run RAG
 ↓
Measure
 ↓
Analyze Failures
 ↓
Improve
```

---

# 21. Final Project Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │   Application Service  │
                       └───────────┬────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
        Document Service    Retrieval Service     LLM Service
                │                  │                  │
                ▼                  ▼                  ▼
          PDF / TXT / MD      Vector Search       LLM API
                │                  │                  │
                ▼                  │                  │
             Chunking              │                  │
                │                  │                  │
                ▼                  │                  │
           Embeddings ─────────────┘                  │
                                   │                  │
                                   └────────┬─────────┘
                                            ▼
                                      Context Builder
                                            │
                                            ▼
                                           LLM
                                            │
                                   ┌────────┴────────┐
                                   ▼                 ▼
                                Answer            Sources
                                   │                 │
                                   └────────┬────────┘
                                            ▼
                                           USER
```

## 22. Final Objective

DocuPilot should ultimately demonstrate:

> **A complete, well-engineered GenAI application that transforms unstructured documents into a searchable knowledge base and uses RAG to provide grounded, source-attributed answers through a usable interface.**

It should serve simultaneously as:

* A **mentor reference project**
* A **Course 1 M4 demonstration**
* A **Course 1 M6 architectural reference**
* A practical example for **RAG, embeddings, structured outputs, LLM APIs and evaluation**
* A foundation that can later be extended with **agentic capabilities** in ProjectPilot.