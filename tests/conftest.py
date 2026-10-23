"""Pytest configuration and fixtures for Agentic Loop API tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_figma_api():
    """Mock Figma API calls to isolate controller logic."""
    with patch('figma_agent_core.api_controller.FigmaAPI') as mock_api:
        api_instance = MagicMock()
        mock_api.return_value = api_instance
        
        # Mock successful export response
        api_instance.export_image.AsyncMock(return_value={
            "success": True,
            "data": {
                "file_key": "test_123",
                "url": "https://figma.com/export/abc123.png"
            }
        })
        
        yield api_instance


@pytest.fixture(autouse=True)
def mock_rate_limiter():
    """Mock rate limiting to allow unlimited test requests."""
    with patch('figma_agent_core.api_controller.RateLimiter') as mock_limiter:
        limiter_instance = MagicMock()
        limiter_instance.is_allowed.AsyncMock(return_value=True)
        mock_limiter.return_value = limiter_instance
        
        yield limiter_instance


@pytest.fixture(autouse=True)
def mock_data_store():
    """Mock data store for persistence layer."""
    with patch('figma_agent_core.api_controller.DataStore') as mock_ds:
        ds_instance = MagicMock()
        mock_ds.return_value = ds_instance
        ds_instance.save.AsyncMock(return_value=True)
        
        yield ds_instance


@pytest.fixture(scope="function")
def test_client():
    """FastAPI TestClient for integration testing."""
    from api.routes import app
    
    with TestClient(app) as client:
        yield client
