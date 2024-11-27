import PyPDF2
from io import BytesIO
from typing import Optional

class PDFExtractor:
    @staticmethod
    def extract_text(pdf_content: bytes) -> Optional[str]:
        try:
            # Create a BytesIO object from the PDF content
            pdf_file = BytesIO(pdf_content)
            
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
                
            return text.strip()
            
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return None