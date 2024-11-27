from fastapi import UploadFile, Request, HTTPException
from app.services.file_service import FileService
from app.services.gemini_service import GeminiService
import logging

logger = logging.getLogger(__name__)

class FileController:
    def __init__(self):
        self.file_service = FileService()
        self.gemini_service = GeminiService()

    async def upload_file(self, file: UploadFile) -> dict:
        try:
            file_info = await self.file_service.save_file(file)
            return {
                "message": "File uploaded successfully",
                **file_info
            }
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    async def get_file_by_id(self, request: Request) -> dict:
        try:
            file = self.file_service.get_file(request.query_params.get("pdf_id"))
            return {
                "message": "Get file details by file id",
                "client_ip": request.client.host,
                "file_id": request.query_params.get("pdf_id"),
                "status": request.url,
            }
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    async def get_file(self, pdf_id: str) -> dict:
        try:
            file = self.file_service.get_file(pdf_id)
            return {
                "message": "Get file details by file id",
                "file_id": pdf_id,
            }
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    async def process_chat(self, pdf_id: str, message: str) -> dict:
        try:
            # Get PDF metadata
            pdf_doc = await self.file_service.get_file(pdf_id)
            if not pdf_doc:
                raise HTTPException(status_code=404, detail="PDF not found")

            # Prepare metadata for context
            pdf_metadata = {
                "pdf_id": pdf_id,
                "filename": pdf_doc.filename,
                "text_preview": pdf_doc.extracted_text[:500] if pdf_doc.extracted_text else None
            }

            # Generate response using Gemini
            response = await self.gemini_service.generate_response(message, pdf_metadata)

            return {
                "message": "Chat response generated successfully",
                "pdf_id": pdf_id,
                "response": response
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")