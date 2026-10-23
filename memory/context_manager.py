"""Context Manager for Agentic Loop."""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ContextEntry:
    """Single context entry with metadata."""
    
    key: str
    value: Any
    source: str = "unknown"
    created_at: str = ""
    expires_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "source": self.source,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextEntry':
        entry = cls(
            key=data["key"],
            value=data["value"],
            source=data.get("source", "unknown"),
            created_at=data.get("created_at", ""),
            expires_at=data.get("expires_at")
        )
        return entry


class ContextManager:
    """Manages workflow context storage and retrieval."""
    
    def __init__(self):
        self._context: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict[str, str]] = {}
        
        # Default metadata keys
        default_metadata = {
            "workflow_id": "",
            "step_name": "",
            "agent_name": "",
            "iteration_count": 0
        }
        self._metadata.update(default_metadata)
    
    def set_context(self, key: str, value: Any, source: str = None):
        """Set a context entry.
        
        Args:
            key: Context variable name
            value: Value to store
            source: Optional source identifier
        """
        if source is None:
            source = self._metadata.get("agent_name", "system")
        
        self._context[key] = {
            "value": value,
            "source": source
        }
    
    def get_context(self, key: str) -> Optional[Any]:
        """Get a context entry by key.
        
        Args:
            key: Context variable name
            
        Returns:
            Value or None if not found
        """
        return self._context.get(key, {}).get("value")
    
    def update_context(self, updates: Dict[str, Any]):
        """Update multiple context entries at once.
        
        Args:
            updates: Dictionary of key-value pairs to set
        """
        for key, value in updates.items():
            self.set_context(key, value)
    
    def get_all_context(self) -> Dict[str, Any]:
        """Get all context as a dictionary.
        
        Returns:
            Copy of all context values
        """
        return {key: data["value"] for key, data in self._context.items()}
    
    def set_metadata(self, **kwargs):
        """Set metadata fields.
        
        Args:
            **kwargs: Metadata field names and values
        """
        self._metadata.update(kwargs)
    
    def get_metadata(self, key: str) -> Optional[str]:
        """Get a metadata field value.
        
        Args:
            key: Metadata field name
            
        Returns:
            Value or None if not found
        """
        return self._metadata.get(key)
    
    def reset_context(self):
        """Clear all context entries."""
        self._context.clear()
    
    def save_to_file(self, filepath: str):
        """Save context to JSON file.
        
        Args:
            filepath: Path to save file
        """
        data = {
            "metadata": self._metadata.copy(),
            "entries": []
        }
        
        for key, entry in self._context.items():
            data["entries"].append(entry)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_file(self, filepath: str):
        """Load context from JSON file.
        
        Args:
            filepath: Path to load from
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self._metadata.update(data.get("metadata", {}))
            
            for entry in data.get("entries", []):
                key = entry["key"]
                value = entry["value"]
                
                # Handle nested dictionaries/lists properly
                if isinstance(value, dict):
                    self._context[key] = {
                        "value": value,
                        "source": entry.get("source", "file")
                    }
                else:
                    self._context[key] = {"value": value}
                    
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in context file: {e}")
