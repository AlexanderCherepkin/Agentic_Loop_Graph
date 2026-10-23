"""Figma Agent Server - Async HTTP Server."""

import asyncio
from typing import Dict, Any
from api_controller import FigmaExportController


class FigmaAgentServer:
    """Async HTTP server for Figma export operations."""

    def __init__(self):
        self.controller = FigmaExportController()
        self._running = False

    async def start_server(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Start the HTTP server."""
        self._host = host
        self._port = port
        self._running = True
        await self.controller.handle_request("system_start", {"status": "started"})

    async def stop_server(self) -> None:
        """Stop the server gracefully."""
        self._running = False
        await asyncio.sleep(0.1)

    async def handle_connection(self, request_id: str, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming client connection and requests."""
        payload = client_data.get("payload", {})
        return await self.controller.handle_request(request_id, payload)

    async def process_batch_request(self, request_ids: list, payloads: list) -> list:
        """Process multiple requests in batch."""
        results = []
        for req_id, payload in zip(request_ids, payloads):
            result = await self.controller.handle_request(req_id, payload)
            results.append(result)
        return results

    def get_server_status(self) -> Dict[str, Any]:
        """Return current server status."""
        return {"running": self._running, "host": self._host, "port": self._port}


# Singleton instance
_agent_instance: FigmaAgentServer = None


async def get_figma_agent() -> FigmaAgentServer:
    """Get or create the singleton Figma agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = FigmaAgentServer()
    return _agent_instance
