from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import os

class AddHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Skip middleware for Swagger UI & Redoc
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)

        # access_token = request.headers.get("access-token", "default_token")
        # Injecting headers
        request.state.custom_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        }
        
        response = await call_next(request)

        # Update response headers
        for key, value in request.state.custom_headers.items():
            response.headers[key] = value

        return response 