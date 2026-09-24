````markdown
# DocuPilot

> AI-Powered Document Intelligence & Knowledge Assistant

DocuPilot is a Generative AI application that allows users to upload documents, ask questions about their content using natural language, and receive grounded answers with relevant source references.

The project demonstrates a complete Retrieval-Augmented Generation (RAG) pipeline, including document ingestion, text processing, chunking, embeddings, vector search, context construction, LLM generation, structured outputs, conversation state, and evaluation.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [RAG Pipeline](#rag-pipeline)
- [Project Workflow](#project-workflow)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Document Processing](#document-processing)
- [Chunking Strategy](#chunking-strategy)
- [Embeddings & Vector Search](#embeddings--vector-search)
- [LLM Layer](#llm-layer)
- [Structured Outputs](#structured-outputs)
- [Conversation Management](#conversation-management)
- [Source Attribution](#source-attribution)
- [Evaluation](#evaluation)
- [Failure Modes](#failure-modes)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Example Usage](#example-usage)
- [Design Decisions](#design-decisions)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)
- [License](#license)

---

## Overview

DocuPilot is designed to solve a common information-access problem: users often have large collections of documents but need a fast and natural way to find specific information inside them.

Instead of relying only on keyword-based search, DocuPilot uses semantic retrieval and Large Language Models to understand the meaning of a user's question and retrieve relevant document content.

The retrieved content is then provided to the LLM as context so that the generated answer is grounded in the uploaded documents.

### Core Flow

```text
Documents
    ↓
Document Processing
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
LLM
    ↓
Grounded Answer
    ↓
Source References
````

---

## Problem Statement

Traditional document search generally relies on exact or closely related keywords.

For example, a user may ask:

> "How long do I have to request a refund?"

while the document may contain:

> "Customers may request reimbursement within 30 calendar days."

A keyword search may not reliably connect these two expressions.

DocuPilot addresses this problem through semantic search and Retrieval-Augmented Generation.

---

## Solution

DocuPilot combines several GenAI technologies:

* Large Language Models
* Prompt Engineering
* Embeddings
* Vector Search
* Retrieval-Augmented Generation
* Structured Outputs
* Conversation State
* Source Attribution
* Evaluation

The application retrieves relevant information from the user's documents before generating an answer.

This reduces the need for the model to rely solely on its pretrained knowledge.

---

## Objectives

The primary objectives of DocuPilot are to:

1. Build a complete GenAI application.
2. Implement an end-to-end RAG pipeline.
3. Process and index user documents.
4. Perform semantic document retrieval.
5. Generate context-grounded answers.
6. Provide source references for generated answers.
7. Maintain conversational context.
8. Validate structured model outputs.
9. Evaluate retrieval and answer quality.
10. Demonstrate common RAG failure modes.

---

## Key Features

### Document Upload

Users can upload supported document formats such as:

* PDF
* TXT
* Markdown

### Document Processing

Uploaded documents are:

1. Parsed
2. Cleaned
3. Split into chunks
4. Enriched with metadata
5. Converted into embeddings
6. Stored in the vector database

### Semantic Search

Users can ask questions using natural language.

The system retrieves documents based on semantic similarity rather than relying exclusively on exact keyword matches.

### RAG-Based Question Answering

Relevant document chunks are retrieved and supplied to the LLM as context.

```text
Question
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
Context
   ↓
LLM
   ↓
Answer
```

### Source Attribution

Generated answers include references to the documents and relevant metadata used during retrieval.

### Conversation State

Users can ask follow-up questions while maintaining relevant conversational context.

### Structured Responses

Where appropriate, LLM responses are generated in a predefined structure and validated before being used by the application.

### Evaluation

The application can be evaluated using predefined question-answer datasets and retrieval test cases.

---

# How It Works

DocuPilot has two major pipelines:

1. Document Ingestion Pipeline
2. Query & Generation Pipeline

---

## Document Ingestion Pipeline

```text
                Document
                   ↓
             Document Parser
                   ↓
              Text Extraction
                   ↓
              Text Cleaning
                   ↓
                 Chunking
                   ↓
            Metadata Creation
                   ↓
            Embedding Model
                   ↓
             Vector Database
```

Each document is transformed into smaller searchable chunks.

Each chunk contains both its content and metadata.

Example:

```json
{
  "document_id": "doc_001",
  "document_name": "refund-policy.pdf",
  "page": 12,
  "section": "Refund Policy",
  "chunk_index": 8
}
```

---

## Query & Generation Pipeline

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
              Context Construction
                     ↓
                    Prompt
                     ↓
                    LLM
                     ↓
              Generated Response
                     ↓
              Source Attribution
                     ↓
                    User
```

---

# Architecture

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
                    ┌──────────────────────┐
                    │  Application Layer   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Document Service   Retrieval Service   LLM Service
             │                 │                 │
             ▼                 ▼                 ▼
      Document Parser     Vector Database      LLM API
             │                 │                 │
             ▼                 │                 │
          Chunking             │                 │
             │                 │                 │
             ▼                 │                 │
        Embeddings ────────────┘                 │
                               │                 │
                               └────────┬────────┘
                                        ▼
                                 Context Builder
                                        │
                                        ▼
                                       LLM
                                        │
                              ┌─────────┴─────────┐
                              ▼                   ▼
                           Answer              Sources
                              │                   │
                              └─────────┬─────────┘
                                        ▼
                                       User
```

---

# RAG Pipeline

DocuPilot's core functionality is based on Retrieval-Augmented Generation.

## 1. Document Ingestion

Documents are uploaded and processed.

```text
PDF / TXT / Markdown
        ↓
     Parser
        ↓
      Text
```

## 2. Text Cleaning

Extracted text is normalized before chunking.

Potential processing includes:

* Removing unnecessary whitespace
* Normalizing text
* Preserving meaningful sections
* Preserving metadata

## 3. Chunking

Large documents are divided into smaller chunks.

```text
Document
   ↓
 ┌─────────┐
 │ Chunk 1 │
 ├─────────┤
 │ Chunk 2 │
 ├─────────┤
 │ Chunk 3 │
 ├─────────┤
 │ Chunk 4 │
 └─────────┘
```

Chunking allows the retrieval system to identify specific portions of a document instead of passing the entire document to the LLM.

## 4. Embedding Generation

Each chunk is converted into a vector representation.

```text
Text Chunk
    ↓
Embedding Model
    ↓
Vector
```

Example:

```text
"Refund requests must be submitted within 30 days."
                         ↓
             [0.13, -0.42, 0.81, ...]
```

## 5. Vector Storage

Embeddings and metadata are stored in a vector-enabled database.

```text
Chunk
 ├── Content
 ├── Embedding
 ├── Document ID
 ├── Page
 └── Metadata
```

## 6. Query Retrieval

When a user asks a question:

```text
Question
   ↓
Query Embedding
   ↓
Similarity Search
   ↓
Top-K Results
```

## 7. Context Construction

The retrieved chunks are assembled into context for the LLM.

```text
Question
    +
Retrieved Context
    +
System Instructions
    ↓
Prompt
```

## 8. Generation

The LLM generates an answer using the supplied context.

```text
Context + Question
        ↓
       LLM
        ↓
     Answer
```

---

# Project Workflow

### Step 1 — Upload

The user uploads one or more documents.

### Step 2 — Process

DocuPilot extracts and processes the document contents.

### Step 3 — Index

The system generates embeddings and stores them in the vector database.

### Step 4 — Ask

The user asks a natural-language question.

### Step 5 — Retrieve

The system finds the most relevant document chunks.

### Step 6 — Generate

The retrieved content is passed to the LLM.

### Step 7 — Respond

The application displays:

* Answer
* Relevant sources
* Conversation context

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic

## Frontend

* Streamlit

## Database

* PostgreSQL
* pgvector

## AI

* Large Language Model
* Embedding Model

The specific model/provider should remain configurable through environment variables.

## Testing

* pytest

## Infrastructure

* Docker
* Docker Compose

## Version Control

* Git
* GitHub

---

# Project Structure

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

# Core Components

## Document Service

Responsible for:

* File validation
* Document parsing
* Text extraction
* Cleaning
* Chunking
* Metadata generation

```text
Document
   ↓
Document Service
   ↓
Processed Chunks
```

## Embedding Service

Responsible for converting text into vector representations.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

## Retrieval Service

Responsible for:

* Query embedding
* Vector similarity search
* Top-K retrieval
* Metadata filtering
* Returning relevant chunks

## LLM Service

Responsible for:

* Model interaction
* Prompt construction
* Structured generation
* Response parsing
* Error handling

## Conversation Service

Responsible for:

* Sessions
* Message history
* Context management
* Follow-up questions

---

# Chunking Strategy

Chunking is an important RAG design decision.

DocuPilot should evaluate different strategies, including:

* Fixed-size chunks
* Overlapping chunks
* Paragraph-based chunks
* Section-aware chunks

Each chunk should retain metadata whenever possible.

Example:

```json
{
  "document_id": "doc_001",
  "document_name": "company-policy.pdf",
  "chunk_index": 14,
  "page": 8,
  "section": "Leave Policy"
}
```

The chosen strategy should be documented in:

```text
docs/05-chunking.md
```

---

# Embeddings & Vector Search

Embeddings represent text as numerical vectors.

```text
Document Chunk
      ↓
Embedding Model
      ↓
Vector
```

The user's question is embedded using the same embedding space.

```text
Question
   ↓
Embedding
   ↓
Similarity Search
   ↓
Relevant Chunks
```

The initial implementation uses:

**PostgreSQL + pgvector**

This allows document metadata and vector representations to be managed within the same database system.

---

# LLM Layer

The LLM receives:

1. System instructions
2. Relevant retrieved context
3. User question
4. Conversation context when required

Conceptually:

```text
System Instructions
        +
Retrieved Context
        +
Conversation Context
        +
User Question
        ↓
       LLM
        ↓
Generated Answer
```

The LLM should not be expected to know the contents of user-uploaded documents unless that information is explicitly retrieved and supplied as context.

---

# Structured Outputs

Where the application requires predictable machine-readable data, DocuPilot uses structured output.

Example:

```json
{
  "answer": "The refund period is 30 days.",
  "sources": [
    {
      "document": "refund-policy.pdf",
      "page": 12
    }
  ]
}
```

The application validates this structure before consuming it.

```text
LLM
 ↓
Structured Response
 ↓
Schema Validation
 ├── Valid → Continue
 └── Invalid → Retry / Error
```

---

# Conversation Management

DocuPilot supports multi-turn interactions.

Example:

```text
User:
What is the refund period?

Assistant:
The refund period is 30 days.

User:
Does that apply to digital products?

Assistant:
According to the uploaded policy...
```

Conversation state should be managed carefully to prevent unnecessary growth of the LLM context.

Potential strategies include:

* Context truncation
* Conversation summarization
* Relevant-history retrieval

---

# Source Attribution

Source attribution is an important part of the application.

Instead of returning only:

```text
"The refund period is 30 days."
```

DocuPilot should provide information about where the answer originated.

Example:

```text
Answer:
The refund period is 30 days.

Sources:
- refund-policy.pdf — Page 12
- customer-policy.pdf — Section 4
```

This makes the answer easier to verify.

---

# Evaluation

A GenAI application should not be evaluated only by manually checking a few responses.

DocuPilot should maintain an evaluation dataset.

Example:

```text
Question:
What is the refund period?

Expected Source:
refund-policy.pdf

Expected Information:
30 days
```

Evaluation dimensions include:

* Retrieval relevance
* Answer correctness
* Context relevance
* Groundedness
* Source accuracy
* Structured-output compliance
* Failure handling

### Evaluation Flow

```text
Evaluation Dataset
        ↓
Run Application
        ↓
Collect Results
        ↓
Evaluate
        ↓
Analyze Failures
        ↓
Improve
        ↓
Run Again
```

Evaluation results should be documented under:

```text
docs/10-evaluation.md
```

---

# Failure Modes

DocuPilot should explicitly account for common RAG failure modes.

### 1. Poor Retrieval

The system retrieves irrelevant chunks.

```text
Question
   ↓
Incorrect Retrieval
   ↓
Incorrect Context
   ↓
Poor Answer
```

### 2. Poor Chunking

Important information may be split across multiple chunks.

### 3. Missing Information

The requested information may not exist in the uploaded documents.

The system should acknowledge this rather than fabricate an answer.

### 4. Excessive Context

Retrieving too many chunks can introduce irrelevant information.

### 5. Ambiguous Questions

Some questions may require clarification.

### 6. Conflicting Documents

Different documents may contain conflicting information.

The system should identify or expose the conflict rather than silently selecting unsupported information.

---

# Testing

Testing should be divided into multiple levels.

## Unit Tests

Test individual components:

```text
Parser
Chunker
Embedding Service
Retriever
Prompt Builder
Schema Validation
```

## Integration Tests

Test interactions between components:

```text
Document
 ↓
Parser
 ↓
Chunker
 ↓
Embedding
 ↓
Vector Store
```

## End-to-End Tests

Test the complete application:

```text
Upload
 ↓
Process
 ↓
Index
 ↓
Question
 ↓
Retrieve
 ↓
Generate
 ↓
Answer
```

## Evaluation Tests

Test response quality against predefined examples.

---

# Security Considerations

DocuPilot should treat uploaded documents and model interactions as potentially sensitive.

Important considerations include:

* Never commit API keys.
* Store secrets in environment variables.
* Validate uploaded files.
* Restrict supported file types.
* Limit file sizes.
* Sanitize document processing inputs.
* Avoid exposing internal configuration.
* Validate model-generated structured data.
* Apply access controls if multi-user functionality is added.
* Consider prompt injection risks originating from uploaded documents.

Example:

```text
Uploaded Document
        ↓
Untrusted Content
        ↓
Retrieval
        ↓
LLM Context
```

Retrieved document content should be treated as **data**, not as trusted application instructions.

---

# Installation

## Prerequisites

Make sure the following are installed:

* Python 3.x
* Git
* Docker
* Docker Compose

Clone the repository:

```bash
git clone <repository-url>
cd docupilot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
LLM_API_KEY=your_api_key
LLM_MODEL=your_model

EMBEDDING_MODEL=your_embedding_model

DATABASE_URL=postgresql://user:password@localhost:5432/docupilot
```

Never commit `.env` to Git.

The repository should contain:

```text
.env.example
```

but not:

```text
.env
```

---

# Running the Project

## Start PostgreSQL + pgvector

```bash
docker compose up -d
```

Verify the services:

```bash
docker compose ps
```

## Start the backend

```bash
uvicorn app.main:app --reload
```

The backend should expose the API locally.

## Start Streamlit

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open the displayed local URL in your browser.

---

# Example Usage

## 1. Upload a document

Upload:

```text
refund-policy.pdf
```

DocuPilot processes the document:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Database
```

## 2. Ask a question

```text
What is the refund period?
```

## 3. Retrieval

The system retrieves the most relevant chunks.

## 4. Generation

The LLM receives the question and retrieved context.

## 5. Response

Example:

```text
The refund period is 30 days.

Sources:
- refund-policy.pdf — Page 12
```

---

# Design Decisions

Important architectural decisions should be documented as the project evolves.

Examples:

### Why RAG?

Because the application needs to answer questions using user-provided documents that may not be part of the LLM's pretrained knowledge.

### Why PostgreSQL + pgvector?

It provides relational database functionality together with vector storage and similarity search in a single database system.

### Why a separate retrieval service?

To keep retrieval logic independent from the LLM layer.

### Why source attribution?

To make generated answers easier to verify and improve transparency around retrieved information.

### Why structured outputs?

To create a predictable contract between probabilistic model output and application logic.

Detailed decisions should be maintained in:

```text
docs/12-design-decisions.md
```

---

# Limitations

The initial version of DocuPilot may have limitations such as:

* Limited document formats
* Basic chunking strategies
* Retrieval errors
* LLM hallucinations
* Limited handling of conflicting documents
* Context-window limitations
* Model/provider dependency
* No advanced multi-user authorization
* No sophisticated production-scale observability

These limitations should be documented rather than hidden.

---

# Future Improvements

Potential future improvements include:

### Document Support

* DOCX
* CSV
* HTML
* PPTX
* Scanned PDFs
* OCR

### Retrieval

* Hybrid search
* Reranking
* Query rewriting
* Metadata filtering
* Multi-query retrieval

### RAG

* Advanced chunking
* Context compression
* Citation verification
* Retrieval evaluation
* Answer faithfulness evaluation

### Application

* Multi-user support
* Authentication
* Document collections
* Conversation management
* Workspace management

### Production

* LLM observability
* Token/cost tracking
* Prompt versioning
* Model routing
* Caching
* Rate limiting
* Monitoring

### Agentic Extension

DocuPilot could later become a tool available to an agent.

For example:

```text
Agent
  ↓
"Search the uploaded company documents"
  ↓
DocuPilot Retrieval Tool
  ↓
Relevant Context
  ↓
Agent
```

This provides a natural connection between the GenAI project and the later Agentic AI project.

---

# Learning Outcomes

Building DocuPilot provides practical experience with:

* Python application development
* LLM APIs
* Prompt engineering
* Structured outputs
* Embeddings
* Vector databases
* Semantic search
* RAG
* Document processing
* Conversation state
* Source attribution
* Evaluation
* Error handling
* API architecture
* FastAPI
* Streamlit
* PostgreSQL
* pgvector
* Docker
* Testing

---

# Mentor / Course Relevance

DocuPilot is designed as a reference implementation for teaching Generative AI application development.

It maps naturally to the curriculum:

```text
M3 — Prompt Engineering
        ↓
Prompt design
Structured outputs
Evaluation
        ↓
M4 — Generative AI Application Development
        ↓
LLM APIs
Embeddings
Vector Search
RAG
Conversation State
UI
        ↓
M6 — Capstone
        ↓
Architecture
Implementation
Testing
Evaluation
Documentation
```

The project demonstrates the progression from a basic LLM interaction to a complete GenAI application.

---

# Project Status

> 🚧 **Status: In Development**

The project is being developed as a mentor/reference implementation for a Generative AI course.

---

# License

This project is licensed under the terms specified in the [`LICENSE`](LICENSE) file.

---

## Author

**Md. Kamran Alam**

GenAI · Software Engineering · AI/ML