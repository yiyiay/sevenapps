from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from collections import defaultdict
import time
from datetime import datetime, timedelta

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.request_counts = defaultdict(list)
        self.WINDOW_SIZE = 60  # 1 minute
        self.MAX_REQUESTS = 100  # per minute per IP

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = datetime.now()

        # Clean old requests
        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip]
            if timestamp > now - timedelta(seconds=self.WINDOW_SIZE)
        ]

        # Check rate limit
        if len(self.request_counts[client_ip]) >= self.MAX_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded. Please try again later."}
            )

        # Add current request
        self.request_counts[client_ip].append(now)

        response = await call_next(request)
        return response 