"""API Routes for Figma Agent Integration."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["figma"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.post("/export")
async def export_design(payload: Dict[str, Any]):
    """Export design from Figma.
    
    Args:
        payload: Export parameters including file_key, format, quality
        
    Returns:
        Export job details and status
    """
    try:
        request_id = str(uuid.uuid4())
        
        # Validate required fields
        if not payload.get("file_key"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing file_key parameter"
            )
        
        operation = payload.get("operation", "export")
        format_type = payload.get("format", "png")
        quality = payload.get("quality", 1.0)
        scale = payload.get("scale", 1.0)
        
        # Call the Figma controller
        from figma_agent_core.api_controller import (
            FigmaExportController, APIException
        )
        
        controller = FigmaExportController()
        result = await controller.handle_request(
            request_id=request_id,
            payload=payload
        )
        
        return {
            "success": True,
            "request_id": request_id,
            "data": result.get("data", {})
        }
    except APIException as e:
        logger.error(f"API Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": e.error_code, "message": str(e)}
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "request_id": request_id if 'request_id' in locals() else None
            }
        )


@router.get("/nodes/{file_key}")
async def get_nodes(file_key: str, page: int = 1, limit: int = 50):
    """Get nodes from a Figma file."""
    try:
        request_id = str(uuid.uuid4())
        
        payload = {
            "operation": "get_nodes",
            "file_key": file_key,
            "page": page,
            "limit": limit
        }
        
        from figma_agent_core.api_controller import FigmaExportController
        
        controller = FigmaExportController()
        result = await controller.handle_request(
            request_id=request_id,
            payload=payload
        )
        
        return {
            "success": True,
            "request_id": request_id,
            "data": result.get("data", {})
        }
    except Exception as e:
        logger.exception(f"Error getting nodes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/workflow/execute/{workflow_id}")
async def execute_workflow(workflow_id: str):
    """Execute an agent workflow with Figma data."""
    try:
        request_id = str(uuid.uuid4())
        
        # This would integrate with the orchestrator layer
        from figma_agent_core.api_controller import APIException
        
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Workflow execution requires orchestrator endpoint"
        )
    except Exception as e:
        logger.exception(f"Error executing workflow: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )