"""Workflow Manager for Agentic Loop."""

import asyncio
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class WorkflowStatus(Enum):
    """Possible workflow statuses."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    WAITING = "waiting"


@dataclass
class WorkflowConfig:
    """Configuration for a workflow."""
    
    name: str
    description: Optional[str] = None
    timeout_seconds: int = 300
    max_retries: int = 3
    retry_delay_seconds: float = 5.0
    
    dependencies: List[str] = field(default_factory=list)
    parallel_execution: bool = False
    max_parallel_agents: int = 1


@dataclass 
class WorkflowResult:
    workflow_id: str
    status: WorkflowStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    
    agent_results: List[Dict[str, Any]] = field(default_factory=list)
    success: bool = False
    final_output: Any = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 0


class WorkflowManager:
    """Manages workflow execution lifecycle and agent coordination."""

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.active_workflows: Dict[str, 'Workflow'] = {}
        self.completed_workflow_history: List[WorkflowResult] = []
        self.workflow_locks: Dict[str, asyncio.Lock] = {}

    async def create_workflow(self, config: WorkflowConfig) -> str:
        """Create and initialize a new workflow."""
        if not config.name or not config.description:
            raise ValueError("Workflow name and description are required")

        # Generate unique ID
        workflow_id = f"{config.name}_{uuid.uuid4().hex[:8]}"
        
        # Create workflow instance
        workflow = Workflow(
            id=workflow_id,
            config=config,
            status=WorkflowStatus.PENDING,
            result=WorkflowResult(
                workflow_id=workflow_id,
                status=WorkflowStatus.PENDING,
                start_time=datetime.now()
            )
        )

        self.active_workflows[workflow_id] = workflow
        
        # Create lock for this workflow if not exists
        if workflow_id not in self.workflow_locks:
            self.workflow_locks[workflow_id] = asyncio.Lock()

        return workflow_id

    async def start_workflow(self, workflow_id: str) -> bool:
        """Start a pending workflow."""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.active_workflows[workflow_id]
        
        async with self.workflow_locks[workflow_id]:
            # Check dependencies
            for dep_id in workflow.config.dependencies:
                if dep_id not in self.completed_workflow_history:
                    raise ValueError(f"Dependency {dep_id} not completed")

            # Change status to running
            workflow.status = WorkflowStatus.RUNNING
            workflow.result.status = WorkflowStatus.RUNNING
            
            return True
