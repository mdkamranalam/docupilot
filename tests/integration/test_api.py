import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "DocuPilot"


def test_document_ingestion_and_rag_query():
    # 1. Upload a text document
    sample_text = """
    DocuPilot Refund Policy:
    Customers may request a complete reimbursement within 45 calendar days of purchase.
    To be eligible, the software license must not have been activated on more than 2 devices.
    Processing refunds typically takes 3 to 5 business days.
    """
    file_bytes = io.BytesIO(sample_text.encode("utf-8"))
    upload_resp = client.post(
        "/api/v1/documents/upload",
        files={"file": ("refund_policy.txt", file_bytes, "text/plain")}
    )
    assert upload_resp.status_code == 200
    upload_data = upload_resp.json()
    doc_id = upload_data["document_id"]
    assert upload_data["chunks_count"] > 0

    # 2. List documents
    list_resp = client.get("/api/v1/documents")
    assert list_resp.status_code == 200
    docs = list_resp.json()
    assert any(d["id"] == doc_id for d in docs)

    # 3. Query RAG
    query_resp = client.post(
        "/api/v1/chat/query",
        json={
            "question": "What is the refund period?",
            "document_id": doc_id,
            "top_k": 3
        }
    )
    assert query_resp.status_code == 200
    rag_data = query_resp.json()
    assert "answer" in rag_data
    assert len(rag_data["sources"]) > 0
    assert rag_data["sources"][0]["document_id"] == doc_id

    # 4. Clean up - delete document
    del_resp = client.delete(f"/api/v1/documents/{doc_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["status"] == "deleted"
