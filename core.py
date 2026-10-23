"""Figma Agent Core Module."""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid
import json
import math


@dataclass
class ComponentData:
    """Represents a Figma component or instance."""
    id: str
    name: str
    type_: str  # 'component' or 'instance'
    layer_id: str
    children: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StyleData:
    """Represents a Figma style."""
    id: str
    name: str
    type_: str  # 'text', 'paint', 'stroke'
    layer_id: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PageData:
    """Represents a Figma page."""
    id: str
    name: str
    children: List[str] = field(default_factory=list)
    auto_layout_properties: Dict[str, Any] = field(default_factory=dict)
