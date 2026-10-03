import json
import io
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_golden_dataset_rag_benchmark():
    # 1. Ingest sample document
    sample_text = """
    DocuPilot Refund Policy:
    Customers may request a complete reimbursement within 45 calendar days of purchase.
    To be eligible, the software license must not have been activated on more than 2 devices.
    Processing refunds typically takes 3 to 5 business days.
    """
    file_bytes = io.BytesIO(sample_text.encode("utf-8"))
    upload_resp = client.post(
        "/api/v1/documents/upload",
        files={"file": ("benchmark_refund_policy.txt", file_bytes, "text/plain")}
    )
    assert upload_resp.status_code == 200
    doc_id = upload_resp.json()["document_id"]

    try:
        # 2. Load golden evaluation dataset
        dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "golden_dataset.json")
        with open(dataset_path, "r") as f:
            test_cases = json.load(f)

        passed_evals = 0
        for tc in test_cases:
            resp = client.post(
                "/api/v1/chat/query",
                json={
                    "question": tc["question"],
                    "document_id": doc_id,
                    "top_k": 3
                }
            )
            assert resp.status_code == 200
            answer = resp.json()["answer"].lower()
            
            # Check keywords
            assert any(kw.lower() in answer for kw in tc["expected_keywords"]), f"Failed test case {tc['id']}: {answer}"
            passed_evals += 1

        assert passed_evals == len(test_cases)
    finally:
        # Clean up
        client.delete(f"/api/v1/documents/{doc_id}")
