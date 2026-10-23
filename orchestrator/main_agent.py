"""Main Agent Orchestrator for Agentic Loop."""

import asyncio
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class WorkflowResult:
    """Result of a workflow execution."""
    
    request_id: str
    status: str
    timestamp: str
    result_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgenticLoopOrchestrator:
    """Main orchestrator coordinating agent workflows with Figma API."""
    
    def __init__(self, figma_controller):
        """Initialize orchestrator with Figma controller.
        
        Args:
            figma_controller: Instance of FigmaExportController or similar
        """
        self.figma_api = figma_controller
        self._registered_agents: List[Callable] = []
        self._workflow_history: Dict[str, WorkflowResult] = {}
    
    def register_agent(self, agent: Callable):
        """Register a processing agent.
        
        Args:
            agent: Async function to process Figma data
        """
        self._registered_agents.append(agent)
        return self
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a complete workflow with Figma data integration.
        
        Args:
            workflow_id: Unique identifier for the workflow
            
        Returns:
            Workflow execution result
        """
        request_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        try:
            # Step 1: Fetch Figma data via controller
            file_data = await self.fetch_figma_data(request_id)
            
            # Step 2: Process with registered agents (chain-of-thought)
            result = await self.process_with_agents(file_data, workflow_id)
            
            # Step 3: Store execution history
            self._workflow_history[request_id] = WorkflowResult(
                request_id=request_id,
                status="completed",
                timestamp=timestamp,
                result_data=result
            )
            
            return {
                "status": "success",
                "request_id": request_id,
                "data": result
            }
            
        except Exception as e:
            # Step 4: Handle errors gracefully
            self._workflow_history[request_id] = WorkflowResult(
                request_id=request_id,
                status="failed",
                timestamp=timestamp,
                result_data={"error": str(e)}
            )
            
            return {
                "status": "failed",
                "request_id": request_id,
                "error": str(e)
            }
    
    async def fetch_figma_data(self, request_id: str) -> Dict[str, Any]:
        """Fetch data from Figma via the API controller.
        
        Args:
            request_id: Unique request identifier
            
        Returns:
            Figma file data
        """
        # This would be configured with actual file_key in production
        payload = {
            "operation": "get_nodes",
            "file_key": self._config.get("file_key", ""),
            "format": self._config.get("export_format", "png")
        }
        
        return await self.figma_api.handle_request(
            request_id=request_id,
            payload=payload
        )
    
    async def process_with_agents(self, file_data: Dict[str, Any], 
                                  workflow_id: str) -> Dict[str, Any]:
        """Process fetched data through registered agents.
        
        Implements chain-of-thought reasoning for agent decisions.
        
        Args:
            file_data: Raw Figma data
            workflow_id: Workflow identifier
            
        Returns:
            Processed result from agents
        """
        if not self._registered_agents:
            return {"message": "No agents registered"}
        
        # Chain-of-thought reasoning phase
        thoughts = []
        
        for agent in self._registered_agents:
            try:
                # Execute agent with thought logging
                result = await agent(file_data, workflow_id)
                
                if isinstance(result, dict):
                    thoughts.append({
                        "agent": agent.__name__,
                        "thoughts": f"Processed file_data with {len(result)} items",
                        "result": result.get("processed_items", [])
                    })
            except Exception as e:
                thoughts.append({
                    "agent": agent.__name__,
                    "error": str(e)
                })
        
        # Aggregate results from all agents
        return {
            "workflow_id": workflow_id,
            "agents_executed": len(self._registered_agents),
            "thoughts": thoughts,
            "file_data_summary": file_data.get("summary", {})
        }
    
    @property
    def _config(self) -> Dict[str, Any]:
        """Get orchestrator configuration."""
        return getattr(self.figma_api, '_config', {})