import pytest
from fastapi import status

@pytest.mark.upload
def test_upload_valid_pdf(test_client):
    # Create a test PDF file
    test_pdf_content = b"%PDF-1.4\n%Test PDF content"
    files = {"file": ("test.pdf", test_pdf_content, "application/pdf")}
    
    response = test_client.post("/v1/pdf", files=files)
    
    assert response.status_code == status.HTTP_200_OK
    assert "pdf_id" in response.json()
    assert "filename" in response.json()
    assert response.json()["filename"] == "test.pdf"

@pytest.mark.integration
def test_upload_and_chat(test_client):
    ## @Todo : Implement this test

def test_upload_invalid_file_type(test_client):
    # Try to upload a text file
    files = {"file": ("test.txt", b"Test content", "text/plain")}
    
    response = test_client.post("/v1/pdf", files=files)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.json() 