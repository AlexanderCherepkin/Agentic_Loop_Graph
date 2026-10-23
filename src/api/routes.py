"""API Routes for Agentic Loop Graph."""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Agentic Loop Graph API", version="1.0.0")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": None}


# Re-export api_controller endpoints if available
try:
    from .api_controller import app as figma_app
    
    # Merge routes - add Figma endpoints to main app
    for route in figma_app.routes:
        if hasattr(route, 'path') and not route.path.startswith('/health'):
            logger.info(f"Importing route from api_controller: {route.path}")
except ImportError as e:
    logger.warning(f"Could not import api_controller: {e}")
