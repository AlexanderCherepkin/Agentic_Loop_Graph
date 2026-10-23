"""Data Store for Agentic Loop."""

import json
from typing import Dict, Any, List, Optional


class DataStore:
    """Persistent data storage for workflow artifacts."""
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        
    def save(self, artifact_id: str, data: Dict[str, Any]) -> bool:
        """Save an artifact to storage.
        
        Args:
            artifact_id: Unique identifier for the artifact
            data: Data to store
            
        Returns:
            True if saved successfully
        """
        self._storage[artifact_id] = {
            "data": data,
            "version": 1
        }
        return True
    
    def get(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """Get an artifact by ID.
        
        Args:
            artifact_id: Artifact identifier
            
        Returns:
            Artifact data or None if not found
        """
        return self._storage.get(artifact_id, {}).get("data")
    
    def delete(self, artifact_id: str) -> bool:
        """Delete an artifact.
        
        Args:
            artifact_id: Artifact to remove
            
        Returns:
            True if deleted, False otherwise
        """
        if artifact_id in self._storage:
            del self._storage[artifact_id]
            return True
        return False
    
    def update(self, artifact_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing artifact.
        
        Args:
            artifact_id: Artifact to update
            updates: Fields to update
            
        Returns:
            True if updated successfully
        """
        if artifact_id not in self._storage:
            return False
        
        self._storage[artifact_id]["data"].update(updates)
        self._storage[artifact_id]["version"] += 1
        return True
    
    def list_artifacts(self, prefix: str = None) -> List[str]:
        """List artifact IDs.
        
        Args:
            prefix: Optional filter by ID prefix
            
        Returns:
            List of matching artifact IDs
        """
        artifacts = []
        
        for key in self._storage.keys():
            if prefix is None or key.startswith(prefix):
                artifacts.append(key)
        
        return artifacts
    
    def clear(self):
        """Clear all stored data."""
        self._storage.clear()
