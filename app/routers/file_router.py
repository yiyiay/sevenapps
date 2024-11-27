from fastapi import APIRouter, File, UploadFile, Request, Form, HTTPException, Depends
from app.controllers.file_controller import FileController
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.DEBUG)  
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str

router = APIRouter(prefix="/v1")
file_controller = FileController()

@router.post("/pdf")
async def upload_file(
    file: UploadFile = File(description="PDF file to upload")
):
    if not file:
        return JSONResponse(
            content={"error": "No file provided"},
            status_code=400
        )
    return await file_controller.upload_file(file)

@router.get("/chat/{pdf_id}")
async def get_file(request: Request):
    return await file_controller.get_files(request)

@router.get("/pdf/{pdf_id}/text")
async def get_pdf_text(pdf_id: str):
    pdf_doc = await file_controller.get_file_by_id(pdf_id)
    if pdf_doc and pdf_doc.extracted_text:
        return {"text": pdf_doc.extracted_text}
    return {"error": "Text not found or extraction failed"}

@router.post("/chat/{pdf_id}")
async def chat_with_pdf(
    pdf_id: str,
    message: ChatMessage,
    request: Request
) -> JSONResponse:
    try:
        # Debugging logs
        logger.info(f"PDF ID: {pdf_id}")
        logger.info(f"Message: {message}")
        logger.info(f"Parsed message: {message.message}")
        logger.info(f"Raw Body: {await request.body()}")
        return await file_controller.process_chat(pdf_id, message.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/{pdf_id}/cache")
async def clear_chat_cache(pdf_id: str):
    """Clear cached responses for a specific PDF"""
    return await file_controller.clear_chat_cache(pdf_id)