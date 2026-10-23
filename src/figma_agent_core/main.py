"""Figma Agent - Main Entry Point."""

import asyncio
from typing import Dict, Any


async def main():
    """Main entry point for the Figma agent."""
    from figma_agent_core.server import get_figma_agent
    
    server = await get_figma_agent()
    
    # Start server
    await server.start_server(host="0.0.0.0", port=8000)
    print("Figma Agent Server started on 0.0.0.0:8000")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    await server.stop_server()
    print("Figma Agent Server stopped.")


if __name__ == "__main__":
    asyncio.run(main())
