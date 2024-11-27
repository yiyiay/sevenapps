from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PDFMetadata:
    filename: str
    upload_date: datetime
    file_size: int
    file_hash: str
    content_type: str

@dataclass
class PDFDocument:
    pdf_id: str
    filename: str
    content: bytes
    path: str
    extracted_text: Optional[str] = None
    created_at: datetime = datetime.now()