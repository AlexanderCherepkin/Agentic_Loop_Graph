"""API Middleware for Authentication, Logging, and CORS."""

import time
from datetime import datetime
from typing import Callable, Optional
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI):
    """Configure middleware for the FastAPI application."""
    
    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.3f}s"
        )
        
        return response
    
    # Authentication Middleware
    @app.middleware("http")
    async def authenticate(request: Request, call_next):
        """Authenticate requests using API key."""
        
        if request.url.path.startswith("/api/v1"):
            auth_header = request.headers.get("X-Figma-Token") or \
                         request.headers.get("Authorization", "")
            
            expected_token = os.getenv(
                "FIGMA_API_TOKEN", 
                os.getenv("API_SECRET_KEY", "default-token")
            )
            
            if not auth_header or auth_header != expected_token:
                logger.warning(f"Unauthorized access from {request.client.host}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"}
                )
        
        response = await call_next(request)
        return response


def create_middleware_config() -> dict:
    """Create middleware configuration dictionary."""
    
    config = {
        "cors": {
            "allow_origins": os.getenv("CORS_ORIGINS", "*").split(","),
            "allow_methods": ["*"],
            "allow_headers": ["*"]
        },
        "authentication": {
            "enabled": True,
            "header_name": "X-Figma-Token"
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "include_request_body": False
        }
    }
    
    return config


# Global configuration instance
MIDDLEWARE_CONFIG = create_middleware_config()