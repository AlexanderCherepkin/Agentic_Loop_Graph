"""Processing Agents for Agentic Loop Framework."""

import asyncio
from typing import Dict, Any, List


class FigmaNodeAnalyzer:
    """Analyzes Figma node structure and properties."""
    
    @staticmethod
    async def analyze_nodes(file_data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Analyze nodes in the Figma file.
        
        Args:
            file_data: Raw Figma API response containing nodes
            workflow_id: Workflow identifier for tracking
            
        Returns:
            Analysis results with node metrics and structure insights
        """
        result = {
            "workflow_id": workflow_id,
            "agent_name": "FigmaNodeAnalyzer",
            "analysis_timestamp": asyncio.get_event_loop().time(),
            "nodes_analyzed": 0,
            "node_types_counted": {},
            "complex_nodes": [],
            "metadata": {}
        }
        
        nodes = file_data.get("data", {}).get("nodes", [])
        result["nodes_analyzed"] = len(nodes) if nodes else 0
        
        # Count node types and identify complex structures
        for node in (nodes or []):
            node_type = node.get("type", "unknown")
            result["node_types_counted"][node_type] = result["node_types_counted"].get(node_type, 0) + 1
            
            if len(node.get("properties", {})) > 3:
                result["complex_nodes"].append({
                    "id": node.get("id"),
                    "type": node_type,
                    "property_count": len(node.get("properties", {})),
                    "name": node.get("name")
                })
        
        result["metadata"]["node_types"] = list(result["node_types_counted"].keys())
        return result
