#!/usr/bin/env python3
"""Figma Export API Controller."""

import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field
import logging
import os
import sys

try:
    from orchestrator.figma_controller import FigmaExportController, FigmaConfig, NodeData, FileData
except ImportError:
    # Fallback for local development
    sys.path.insert(0, r"d:/My_head_folders/My-desktop/Agentic_Loop_Graph")
    try:
        from figma_agent_core.api_controller import FigmaExportController, FigmaConfig, NodeData, FileData
    except ImportError:
        class FigmaExportController:
            async def export_file(self, **kwargs): return {"status": "error", "message": "Not implemented"}
        class FigmaConfig: pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("figma_api_controller")

from dataclasses import dataclass

@dataclass
class NodeData:
    id: str
    type: str
    x: float
    y: float
    name: str = ""

@dataclass
class FileData:
    id: str
    name: str

class ExportRequest(BaseModel):
    file_id: str = Field(..., description="Figma file ID")
    node_ids: List[str] = Field(default_factory=list, description="Node IDs to export")
    format: str = Field(default="png", description="Export format")
    width: int = Field(default=1920, ge=16, le=4096)
    height: int = Field(default=1080, ge=16, le=4096)
    scale: float = Field(default=1.0, ge=1, le=4)

class ExportResponse(BaseModel):
    status: str = Field(..., description="Export status")
    file_id: Optional[str] = None
    format: Optional[str] = None
    message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: str

app = FastAPI(title="Figma Export API Controller")

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", timestamp=datetime.now(timezone.utc).isoformat())

@app.post("/api/figma/export", response_model=ExportResponse, tags=["Figma Export"])
async def export_figma_file(request: ExportRequest) -> ExportResponse:
    """
    Export Figma file to specified format.

    Args:
        request: Export parameters including file_id, node_ids, format, dimensions
    """
    logger.info(f"Export request received: {request.file_id}")

    try:
        controller = FigmaExportController()
        result = await controller.export_file(
            file_id=request.file_id,
            nodes=request.node_ids or [],
            format=request.format,
            width=request.width,
            height=request.height,
            scale=request.scale
        )
        logger.info(f"Export completed successfully: {result}")
        return ExportResponse(
            status="success",
            file_id=result.get("file_id", request.file_id),
            format=result.get("format", request.format)
        )
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
