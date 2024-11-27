import pytest
from fastapi import status

def test_chat_with_valid_pdf(test_client):
    # First upload a PDF
    test_pdf_content = b"%PDF-1.4\n%Test PDF content"
    files = {"file": ("test.pdf", test_pdf_content, "application/pdf")}
    upload_response = test_client.post("/v1/pdf", files=files)
    pdf_id = upload_response.json()["pdf_id"]
    
    # Then try to chat about it
    chat_data = {"message": "What is this document about?"}
    response = test_client.post(
        f"/v1/chat/{pdf_id}",
        json=chat_data
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert "response" in response.json()
    assert "timestamp" in response.json()

def test_chat_with_invalid_pdf_id(test_client):
    chat_data = {"message": "What is this document about?"}
    response = test_client.post(
        "/v1/chat/invalid_id",
        json=chat_data
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND 