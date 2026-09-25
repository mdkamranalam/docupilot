import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document, Chunk
from app.documents.parser import DocumentParser
from app.documents.cleaner import TextCleaner
from app.documents.chunker import TextChunker
from app.retrieval.vector_store import VectorStore
from app.services.qa_service import QAService
from app.llm.schemas import ChatQueryRequest, RAGAnswerResponse

router = APIRouter()

UPLOAD_DIR = "/tmp/docupilot_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Uploads, cleans, chunks, embeds, and saves a PDF, TXT, or MD document."""
    allowed_exts = [".pdf", ".txt", ".md", ".markdown"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed: {', '.join(allowed_exts)}"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Parse document
        raw_pages = DocumentParser.parse(file_path)

        # 2. Clean pages
        cleaned_pages = []
        for p in raw_pages:
            cleaned_pages.append({
                "page": p["page"],
                "text": TextCleaner.clean(p["text"])
            })

        # 3. Create Document Record in DB
        doc = Document(
            filename=file.filename,
            file_type=ext.replace(".", ""),
            doc_metadata={"file_size": os.path.getsize(file_path)}
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # 4. Chunk document
        chunker = TextChunker(chunk_size=800, chunk_overlap=150)
        chunks_data = chunker.chunk_document_pages(
            pages_data=cleaned_pages,
            document_id=doc.id,
            filename=doc.filename
        )

        # 5. Embed and store chunks in pgvector
        vector_store = VectorStore(db)
        vector_store.store_chunks(chunks_data)

        return {
            "document_id": doc.id,
            "filename": doc.filename,
            "chunks_count": len(chunks_data),
            "status": "indexed_successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    """Lists all uploaded documents with chunk counts."""
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    results = []
    for d in docs:
        chunk_count = db.query(Chunk).filter(Chunk.document_id == d.id).count()
        results.append({
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "uploaded_at": d.uploaded_at.isoformat(),
            "chunks_count": chunk_count,
            "metadata": d.doc_metadata
        })
    return results


@router.delete("/documents/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Deletes a document and cascades deletion to all vector chunks."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(doc)
    db.commit()
    return {"status": "deleted", "document_id": document_id}


@router.post("/chat/query", response_model=RAGAnswerResponse)
def query_rag(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """Answers a question using RAG over the uploaded document corpus."""
    qa_service = QAService(db)
    return qa_service.answer_question(
        question=request.question,
        document_id=request.document_id,
        conversation_history=request.conversation_history,
        top_k=request.top_k
    )
