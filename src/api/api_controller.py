"""API Controller for Agentic Loop Graph."""

import sys
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager


# Import Figma controller from orchestrator
try:
    from orchestrator.figma_controller import FigmaExportController, FigmaConfig
except ImportError as e:
    print(f"Warning: Could not import FigmaExportController: {e}")
    FigmaExportController = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifecycle hooks for FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    logger.info("Starting Agentic Loop Graph API")
    
    # Create Figma controller instance
    figma_controller = None
    if FigmaExportController is not None:
        try:
            figma_controller = FigmaExportController()
            logger.info("FigmaExportController initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize FigmaExportController: {e}")
    
    yield
    
    # Shutdown
    if figma_controller is not None:
        await figma_controller.close()
        logger.info("FigmaExportController closed")


# Create FastAPI application with lifespan
app = FastAPI(
    title="Agentic Loop Graph API",
    version="1.0.0",
    description="API for Figma export and graph management",
    lifespan=lifespan
)

# Request/Response Models
class ExportRequest(BaseModel):
    """Figma export request parameters."""
    
    file_key: str
    format: Optional[str] = "png"  # png, jpg, webp, svg, pdf, sketch
    scale_factor: float = 1.0  # 1.0 or 2.0 for PNG
    width: int = None
    height: int = None


class ExportResponse(BaseModel):
    """Figma export response."""
    
    status: str
    message: Optional[str] = None
    data_url: Optional[str] = None
    file_size: Optional[int] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "agentic-loop-graph", 
        "version": "1.0.0"
    }


@app.post("/api/figma/export", response_model=ExportResponse)
async def export_figma(request: ExportRequest, request_obj: Request = None):
    """Export Figma file to specified format."""
    
    logger.info(f"Received export request for file_key: {request.file_key}")
    
    # Validate Figma controller is available
    if FigmaExportController is None:
        raise HTTPException(
            status_code=503, 
            detail="Figma service unavailable. Please check dependencies."
        )
    
    try:
        # Create or get Figma controller instance (singleton pattern)
        figma_controller = getattr(app.state, '_figma_controller', None)
        if figma_controller is None:
            app.state._figma_controller = FigmaExportController()
            figma_controller = app.state._figma_controller
        
        # Perform export with error handling
        result = await figma_controller.export_file(
            file_key=request.file_key,
            format=request.format or "png",
            scale_factor=request.scale_factor or 1.0
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500, 
                detail=result.get("message", "Export failed")
            )
        
        logger.info(f"Export completed successfully for file_key: {request.file_key}")
        
        return ExportResponse(
            status="success",
            message="Figma file exported successfully",
            data_url=result.get("data_url"),
            file_size=result.get("file_size")
        )
        
    except HTTPException:
        # Re-raise FastAPI exceptions
        raise
    except Exception as e:
        logger.error(f"Export failed with error: {str(e)}", exc_info=sys.exc_info())
        raise HTTPException(
            status_code=500, 
            detail=f"Export service error: {str(e)}"
        )


@app.get("/api/figma/status")
async def figma_status():
    """Check Figma service status."""
    
    if FigmaExportController is None:
        return {"status": "unavailable", "reason": "Figma controller not initialized"}
    
    try:
        # Create temp controller for status check
        temp_controller = FigmaExportController()
        
        # Try to get file info (will fail gracefully if no token)
        result = await temp_controller.get_file_info(file_key="test")
        
        return {
            "status": result.get("status", "unknown"),
            "message": result.get("message", "")
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Agentic Loop Graph API server...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8002,
        log_level="info"
    )