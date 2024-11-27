from fastapi import UploadFile, Request, HTTPException
from app.services.file_service import FileService
from app.services.gemini_service import GeminiService
from app.services.vector_store import VectorStore
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FileController:
    def __init__(self):
        self.file_service = FileService()
        self.gemini_service = GeminiService()
        self.vector_store = VectorStore()
        self.response_cache = {}
        self.cache_ttl = timedelta(hours=24)

    async def upload_file(self, file: UploadFile) -> dict:
        try:
            file_info = await self.file_service.save_file(file)
            
            # Index the document for RAG
            if file_info.get("text_extracted"):
                pdf_doc = await self.file_service.get_file(file_info["pdf_id"])
                await self.vector_store.add_document(
                    file_info["pdf_id"], 
                    pdf_doc.extracted_text
                )
            
            return {
                "message": "File uploaded and indexed successfully",
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

    def _get_cache_key(self, pdf_id: str, message: str) -> str:
        return f"{pdf_id}:{message}"

    def _get_cached_response(self, pdf_id: str, message: str) -> Optional[str]:
        cache_key = self._get_cache_key(pdf_id, message)
        if cache_key in self.response_cache:
            cached_item = self.response_cache[cache_key]
            if datetime.now() - cached_item["timestamp"] < self.cache_ttl:
                return cached_item["response"]
            else:
                # Remove expired cache entry
                del self.response_cache[cache_key]
        return None

    def _cache_response(self, pdf_id: str, message: str, response: str):
        cache_key = self._get_cache_key(pdf_id, message)
        self.response_cache[cache_key] = {
            "response": response,
            "timestamp": datetime.now()
        }

    async def process_chat(self, pdf_id: str, message: str) -> dict:
        try:
            # Check cache first
            cached_response = self._get_cached_response(pdf_id, message)
            if cached_response:
                return {
                    "message": "Chat response retrieved from cache",
                    "pdf_id": pdf_id,
                    "response": cached_response,
                    "cached": True
                }

            # Get relevant chunks using RAG
            relevant_chunks = await self.vector_store.get_relevant_chunks(pdf_id, message)
            
            # Prepare metadata with relevant chunks
            pdf_doc = await self.file_service.get_file(pdf_id)
            if not pdf_doc:
                raise HTTPException(status_code=404, detail="PDF not found")

            pdf_metadata = {
                "pdf_id": pdf_id,
                "filename": pdf_doc.filename,
                "relevant_chunks": relevant_chunks  # Send relevant chunks instead of preview
            }

            # Generate response using Gemini
            response = await self.gemini_service.generate_response(message, pdf_metadata)
            
            # Cache the response
            self._cache_response(pdf_id, message, response)

            return {
                "message": "Chat response generated successfully",
                "pdf_id": pdf_id,
                "response": response,
                "cached": False
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")