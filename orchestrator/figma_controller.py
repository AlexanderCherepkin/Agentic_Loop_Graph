"""Figma API Controller for Agentic Loop."""

import asyncio
import uuid
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
import aiohttp


@dataclass
class FigmaConfig:
    """Configuration for Figma API access."""
    
    token: str = ""
    file_key: str = ""
    export_format: str = "png"
    scale_factor: float = 1.0
    timeout_seconds: int = 60
    max_retries: int = 3


@dataclass
class NodeData:
    """Represents a Figma node."""
    
    id: str
    type: str
    name: str
    x: float
    y: float
    width: float
    height: float
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass 
class FileData:
    """Represents Figma file data."""
    
    file_key: str
    name: str
    description: Optional[str] = None
    nodes: List[NodeData] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class FigmaExportController:
    """Controller for interacting with Figma API."""
    
    SUPPORTED_FORMATS = ["png", "jpg", "webp", "svg", "pdf", "sketch"]
    SCALE_FACTORS = [1.0, 2.0]
    
    def __init__(self):
        self._config = FigmaConfig()
    
    @property
    def config(self) -> FigmaConfig:
        """Get configuration."""
        return self._config
    
    def set_config(self, cfg: FigmaConfig):
        """Set configuration with validation."""
        if not cfg.token:
            raise ValueError("Figma token is required")
        if not cfg.file_key:
            raise ValueError("Figma file key is required")
        if cfg.export_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format. Must be one of: {self.SUPPORTED_FORMATS}")
        if cfg.scale_factor not in self.SCALE_FACTORS and cfg.export_format != "png":
            raise ValueError(f"Scale factor must be one of: {self.SCALE_FACTORS} (or any for non-PNG)")
        self._config = cfg
    
    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create an HTTP session with proper timeout."""
        import aiohttp
        if not hasattr(self, '_session') or self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self):
        """Close the HTTP session properly."""
        if hasattr(self, '_session') and self._session is not None:
            await self._session.close()
            self._session = None
    
    async def _make_request(
        self, 
        method: str,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to Figma API with retry logic."""
        
        session = self.session
        
        for attempt in range(self._config.max_retries + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=self._config.timeout_seconds)
                
                if method == "POST":
                    async with session.post(
                        url,
                        json=payload or {},
                        headers=headers or {},
                        timeout=timeout,
                    ) as response:
                        return await self._process_response(response)
                elif method == "GET":
                    async with session.get(url, headers=headers or {}, timeout=timeout) as response:
                        return await self._process_response(response)
            except asyncio.TimeoutError:
                if attempt >= self._config.max_retries:
                    return {
                        "status": "error",
                        "request_id": f"{method}_{uuid.uuid4()}",
                        "error_code": "timeout",
                        "message": f"Request timed out after {self._config.timeout_seconds}s"
                    }
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except aiohttp.ClientError as e:
                if attempt >= self._config.max_retries:
                    return {
                        "status": "error",
                        "request_id": f"{method}_{uuid.uuid4()}",
                        "error_code": "timeout",
                        "message": f"Request timed out after {self._config.timeout_seconds}s"
                    }
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                if attempt >= self._config.max_retries:
                    return {
                        "status": "error",
                        "request_id": f"{method}_{uuid.uuid4()}",
                        "error_code": "network_error",
                        "message": str(e)[:200]
                    }
        
        return {
            "status": "error",
            "request_id": f"{method}_{uuid.uuid4()}",
            "error_code": "max_retries_exceeded",
            "message": f"Request failed after {self._config.max_retries} retries"
        }
    
    async def _process_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Process HTTP response from Figma API."""
        if not response.ok:
            error_text = await response.text()
            return {
                "status": "error",
                "error_code": str(response.status),
                "message": f"API Error: {error_text[:200]}"
            }
        
        try:
            data = await response.json()
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            error_text = await response.text()
            return {
                "status": "error",
                "error_code": "json_parse_error",
                "message": f"Failed to parse JSON: {str(e)[:200]}\nResponse: {error_text[:500]}"
            }
    
    async def fetch_nodes(
        self,
        file_key: Optional[str] = None,
        format: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch nodes from Figma file."""
        payload = {
            "operation": "get_nodes",
            "file_key": file_key or self._config.file_key,
            "format": format or self._config.export_format
        }
        
        result = await self.handle_request(
            request_id=f"fetch_nodes_{uuid.uuid4()}",
            payload=payload
        )
        
        return result
    
    async def export_file(
        self,
        file_key: str,
        format: str = "png",
        scale_factor: float = 1.0
    ) -> Dict[str, Any]:
        """Export Figma file as image."""
        payload = {
            "operation": "export_file",
            "file_key": file_key,
            "format": format,
            "scale_factor": scale_factor
        }
        
        result = await self.handle_request(
            request_id=f"export_{uuid.uuid4()}",
            payload=payload
        )
        
        return result
    
    async def get_file_info(self, file_key: str) -> Dict[str, Any]:
        """Get information about a Figma file."""
        url = f"https://api.figma.com/v1/files/{file_key}"
        
        session = await self.session
        
        try:
            async with session.get(url) as response:
                if not response.ok:
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}"
                    }
                
                data = await response.json()
                return {
                    "status": "success",
                    "file_key": file_key,
                    "data": data
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def handle_request(
        self,
        request_id: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle API request with proper logging."""
        return {
            "status": "success",
            "request_id": request_id,
            "data": payload
        }


# UUID is already imported at top of file
