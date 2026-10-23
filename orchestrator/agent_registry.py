"""Agent Registry for Agentic Loop."""

from typing import Dict, Any, Callable, List
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """Configuration for a processing agent."""

    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    enabled: bool = True
    priority: int = 0


class AgentRegistry:
    """Manages registration and dispatch of processing agents."""

    def __init__(self):
        self._agents: Dict[str, Callable] = {}
        self._agent_configs: Dict[str, AgentConfig] = {}
        self._execution_order: List[str] = []

    def register_agent(
        self, 
        name: str,
        agent_func: Callable,
        config: AgentConfig = None
    ) -> str:
        """Register a new processing agent.
        
        Args:
            name: Unique identifier for the agent
            agent_func: Async function to process data
            config: Optional configuration
            
        Returns:
            Registered agent ID
        """
        if not callable(agent_func):
            raise ValueError("Agent must be a callable")

        self._agents[name] = agent_func

        if config is None:
            config = AgentConfig(
                name=name,
                description=f"Auto-generated for {name}",
                input_schema={},
                output_schema={}
            )

        self._agent_configs[name] = config

        # Add to default execution order if not present
        if name not in self._execution_order:
            self._execution_order.append(name)

        return name
    async def execute_agents(
        self, 
        data: Dict[str, Any],
        workflow_id: str,
        agent_names: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Execute registered agents in sequence.
        
        Args:
            data: Input data to process
            workflow_id: Workflow identifier for tracking
            agent_names: Optional subset of agents to execute
            
        Returns:
            List of execution results from each agent
        """
        if agent_names is None:
            agent_names = self._execution_order

        results = []

        for name in agent_names:
            config = self._agent_configs.get(name)

            # Skip disabled agents
            if not config or not config.enabled:
                continue

            try:
                result = await self._agents[name](data, workflow_id, config)
                results.append({
                    "agent": name,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "agent": name,
                    "status": "failed",
                    "error": str(e)
                })

        return results

    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get configuration for a registered agent.
        
        Args:
            agent_name: Agent identifier
            
        Returns:
            Agent configuration or None if not found
        """
        return self._agent_configs.get(agent_name)

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents with their configurations.
        
        Returns:
            List of agent information dictionaries
        """
        info = []

        for name in self._execution_order:
            config = self._agent_configs.get(name)

            if config:
                info.append({
                    "name": name,
                    "description": config.description,
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "has_config": True
                })

        return info

    def remove_agent(self, agent_name: str) -> bool:
        """Remove a registered agent.
        
        Args:
            agent_name: Agent to remove
            
        Returns:
            True if removed, False otherwise
        """
        if agent_name in self._agents:
            del self._agents[agent_name]

            if agent_name in self._execution_order:
                self._execution_order.remove(agent_name)

            if agent_name in self._agent_configs:
                del self._agent_configs[agent_name]

            return True

        return False

    def enable_agent(self, agent_name: str) -> bool:
        """Enable a registered agent.
        
        Args:
            agent_name: Agent to enable
            
        Returns:
            True if enabled, False otherwise
        """
        config = self._agent_configs.get(agent_name)

        if not config:
            return False

        config.enabled = True
        return True

    def disable_agent(self, agent_name: str) -> bool:
        """Disable a registered agent.
        
        Args:
            agent_name: Agent to disable
            
        Returns:
            True if disabled, False otherwise
        """
        config = self._agent_configs.get(agent_name)

        if not config:
            return False

        config.enabled = False
        return True


if __name__ == "__main__":
    import asyncio
    
    async def test_agent(data: Dict[str, Any], workflow_id: str, config: AgentConfig):
        print(f"[{config.name}] Processing data for workflow {workflow_id}")
        return {"processed": True}

    registry = AgentRegistry()
    registry.register_agent("test", test_agent)

    print("Registered agents:", registry.list_agents())
    
    # Test execution
    asyncio.run(registry.execute_agents(
        data={"input": "test"},
        workflow_id="wf-001"
    ))

    def get_agent(self, agent_name: str) -> Callable:
        """Get registered agent by name.
        
        Args:
            agent_name: Agent identifier
            
        Returns:
            Agent function or None if not found
        """
        return self._agents.get(agent_name)