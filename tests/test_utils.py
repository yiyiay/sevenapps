import pytest
from app.utils.pdf_extractor import extract_text_from_pdf

def test_pdf_text_extraction():
    # Create a test PDF file
    test_pdf_path = "test_uploads/test.pdf"
    with open(test_pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%Test PDF content")
    
    text = extract_text_from_pdf(test_pdf_path)
    assert isinstance(text, str) 