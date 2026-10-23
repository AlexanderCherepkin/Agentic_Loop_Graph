"""Integration tests for API endpoints."""

import sys
from pathlib import Path

# Динамически добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


@pytest.fixture
def client():
    """Create test client with mocked dependencies."""
    from figma_agent_core.api_routes import app
    
    # Mock Figma API controller
    with patch("figma_agent_core.api_controller.FigmaExportController"):
        yield TestClient(app)


class TestApiRoutes:
    """Test all API routes."""

    def test_export_endpoint(self, client):
        """Тест эндпоинта экспорта через HTTP"""
        response = client.post(
            "/api/figma/export",
            json={
                "file_key": "test_123",
                "operation": "png_export"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_nodes_endpoint(self, client):
        """Тест эндпоинта получения узлов"""
        response = client.get(
            "/api/figma/nodes",
            params={"file_key": "test_123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data

    def test_list_files_endpoint(self, client):
        """Тест эндпоинта списка файлов"""
        response = client.get("/api/figma/files")
        
        assert response.status_code == 200
        data = response.json()
        assert "files" in data

    @pytest.mark.asyncio
    async def test_invalid_operation(self, client):
        """Тест с недопустимой операцией"""
        # This would be tested with actual controller logic
        pass
    
    @pytest.mark.asyncio 
    async def test_rate_limit_exceeded(self, client):
        """Тест превышения лимитов запросов"""
        # Would require rate limiting setup
        pass
