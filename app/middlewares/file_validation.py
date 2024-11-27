from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import json

class FileValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path == "/v1/pdf" and request.method == "POST":
            try:
                # Store the file in memory
                body = await request.body()
                
                # Create a new request with the file in the form data
                request._body = body

                form = await request.form() # Consumes the body
                file = form.get("file")
                
                if not file:
                    return Response(
                        content=json.dumps({"error": "No file provided"}),
                        media_type="application/json",
                        status_code=400
                    )
                
                if not (file.content_type == "application/pdf" or 
                       file.content_type == "binary/octet-stream" or 
                       file.filename.lower().endswith('.pdf')):
                    return Response(
                        content=json.dumps({"error": "Only PDF files are allowed"}),
                        media_type="application/json",
                        status_code=400
                    )
                # Reset file pointer and request body
                await file.seek(0)
                request._body = body
                
            except Exception as e:
                return Response(
                    content=json.dumps({"error": f"Error processing file: {str(e)}"}),
                    media_type="application/json",
                    status_code=400
                )
            
        return await call_next(request)