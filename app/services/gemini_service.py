import google.generativeai as genai
from fastapi import HTTPException
import logging
from app.config.config import gemini_config
from typing import Dict, Any
import time
from datetime import datetime, timedelta
from collections import deque
import os

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.config = gemini_config
        self.model = "gemini-1.5-flash"
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self._setup_client()
        self._request_timestamps = deque(maxlen=self.config.RATE_LIMIT_REQUESTS)
        
    def _setup_client(self) -> None:
        try:
            # Configure the API key first
            genai.configure(api_key=self.config.API_KEY)
            
            # Create the model
            self.client = genai.GenerativeModel(
                model_name=self.model,
                generation_config=self.generation_config
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize AI service: {str(e)}"
            )

    def _check_rate_limit(self) -> None:
        """Check if we've exceeded our rate limit"""
        now = datetime.now()
        
        # Remove timestamps older than 1 minute
        while self._request_timestamps and self._request_timestamps[0] < now - timedelta(minutes=1):
            self._request_timestamps.popleft()
            
        if len(self._request_timestamps) >= self.config.RATE_LIMIT_REQUESTS:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    async def generate_response(self, message: str, pdf_metadata: Dict[str, Any]) -> str:
        """Generate a response using the Gemini API"""
        try:
            self._check_rate_limit()
            
            # Add context about the PDF to the prompt
            context = f"""Context: This conversation is about a PDF document with the following metadata:
            File ID: {pdf_metadata.get('pdf_id')}
            Filename: {pdf_metadata.get('filename')}
            Text Preview: {pdf_metadata.get('text_preview', 'Not available')}
            
            User Question: {message}"""

            # Create the model
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )            

            chat_session = model.start_chat(
                history=[
                ]
            )

            response = chat_session.send_message(context)
            
            self._request_timestamps.append(datetime.now())
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")
                
            return response.text

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}") 