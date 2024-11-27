import os
import uuid
import logging
from fastapi import UploadFile
from app.managers.pdf_manager import PDFStateManager
from app.managers.models import PDFDocument, PDFMetadata
from app.config.config import settings
from typing import List, Optional
from datetime import datetime 
from app.utils.pdf_extractor import PDFExtractor
from io import BytesIO

# Configure logger
logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        self.state_manager = PDFStateManager()
        self.pdf_extractor = PDFExtractor()

    async def save_file(self, file: UploadFile) -> dict:
        try:
            pdf_id = str(uuid.uuid4())
            contents = await file.read()
            
            extracted_text = self.pdf_extractor.extract_text(contents)
            
            extension = file.filename.split('.')[-1]
            new_filename = f"{pdf_id}.{extension}"
            file_location = os.path.join(settings.UPLOAD_FOLDER, new_filename)
            
            with open(file_location, "wb") as buffer:
                buffer.write(contents)
            
            self.state_manager.add_pdf(
                pdf_id=pdf_id,
                filename=file.filename,
                content=contents,
                path=file_location,
                extracted_text=extracted_text
            )
            logger.info(f"File saved successfully: {file.filename} (ID: {pdf_id})")
            
            return {
                "pdf_id": pdf_id,
                "text_extracted": bool(extracted_text),
                "text_preview": extracted_text[:200] if extracted_text else None  # Return first 200 chars as preview
            }
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}", exc_info=True)
            raise

    async def get_file(self, pdf_id: str) -> Optional[PDFDocument]:
        return self.state_manager.get_pdf(pdf_id)

    async def search_files(self, 
                          filename: Optional[str] = None,
                          date: Optional[datetime.date] = None,
                          min_size: Optional[int] = None,
                          max_size: Optional[int] = None) -> List[PDFDocument]:
        if filename:
            return self.state_manager.search_by_filename(filename)
        elif date:
            return self.state_manager.search_by_date(date)
        elif min_size is not None and max_size is not None:
            return self.state_manager.search_by_size_range(min_size, max_size)
        return []