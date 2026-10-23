"""Unit tests for FigmaExportController - Professional Test Suite."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
import json
import asyncio
from datetime import datetime, timezone


class TestRateLimitConfig:
    """Test rate limit configuration."""

    def test_default_values(self):
        """Test default rate limit values."""
        config = RateLimitConfig()
        assert config.requests_per_minute == 60
        assert config.burst_limit == 10

    def test_custom_values(self):
        """Test custom rate limit values."""
        config = RateLimitConfig(requests_per_minute=100, burst_limit=20)
        assert config.requests_per_minute == 100
        assert config.burst_limit == 20


class TestValidationResult:
    """Test validation result data structure."""

    def test_valid_result(self):
        """Test valid validation result."""
        result = ValidationResult(valid=True)
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_invalid_result(self):
        """Test invalid validation result."""
        result = ValidationResult(valid=False)
        result.errors.append("Missing file_key")
        
        assert result.valid is False
        assert len(result.errors) == 1


class TestExportResult:
    """Test export result data structure."""

    def test_export_result(self):
        """Test export result creation and serialization."""
        file_key = "test_file_123"
        result = ExportResult(file_key=file_key)
        
        assert result.file_key == file_key
        assert result.status == ExportStatus.COMPLETED


class TestErrorResponse:
    """Test error response data structure."""

    def test_error_response_basic(self):
        """Test basic error response."""
        error = ErrorResponse(error_code="VALIDATION_ERROR", message="Invalid request")
        
        assert error.error_code == "VALIDATION_ERROR"
        dict_result = error.to_dict()
        assert dict_result["error"] == "VALIDATION_ERROR"


class TestFigmaExportController:
    """Comprehensive tests for FigmaExportController."""

    @pytest.fixture
    def controller(self):
        return FigmaExportController(rate_limit_config=RateLimitConfig(requests_per_minute=100, burst_limit=20))
        return FigmaExportController(
            rate_limit_config=RateLimitConfig(requests_per_minute=100, burst_limit=20)
        )

    @pytest.mark.asyncio
    async def test_handle_request_valid(self, controller):
        """Test successful export request."""
        with patch('sys.modules', {
            'figma_agent_core': MagicMock(),
            'figma_agent_core.export_to_png': AsyncMock(return_value={"success": True, "file_key": "mock_123"})
        }):
            response = await controller.handle_request({}, json.dumps({"file_key": "test", "quality": 1.0}))
            assert response["success"] is True

    @pytest.mark.asyncio
    async def test_handle_request_missing_file_key(self, controller):
        """Test request without file_key."""
        response = await controller.handle_request({}, json.dumps({"quality": 1.0}))
        assert response["success"] is False

    @pytest.mark.asyncio
    async def test_validate_request_valid_file_key(self, controller):
        """Test validation with valid file key."""
        result = await controller.validate_request({"file_key": "test-123"})
        assert result.valid is True
        assert len(result.errors) == 0

    @pytest.mark.asyncio
    async def test_validate_request_missing_file_key(self, controller):
        """Test validation without file key."""
        result = await controller.validate_request({})
        assert result.valid is False
        assert "Missing required field: file_key" in result.errors[0]

    @pytest.mark.asyncio
    async def test_validate_request_invalid_format(self, controller):
        """Test validation with invalid format."""
        result = await controller.validate_request({"file_key": "test", "format": "pdf"})
        assert result.valid is False
        assert "Invalid format" in result.errors[0]

    @pytest.mark.asyncio
    async def test_validate_request_quality_out_of_range(self, controller):
        """Test validation with quality out of range."""
        result = await controller.validate_request({"file_key": "test", "quality": 2.0})
        assert result.valid is False
        assert "quality must be between" in result.errors[0]

    @pytest.mark.asyncio
    async def test_check_rate_limit_within_limits(self, controller):
        """Test rate limit check within limits."""
        # Reset request count for mock API key
        controller.request_count["mock_key"] = []
        result = await controller.check_rate_limit("mock_key")
        assert result is True

    @pytest.mark.asyncio
    async def test_check_rate_limit_exceeded(self, controller):
        """Test rate limit check when exceeded."""
        # Simulate exceeding rate limit
        controller.request_count["overflow_key"] = [100] * 200  # More than 100 requests in minute window
        
        result = await controller.check_rate_limit("overflow_key")
        assert result is False

    @pytest.mark.asyncio
    async def test_handle_request_validation_error(self, controller):
        """Test handling of validation errors."""
        response = await controller.handle_request({}, json.dumps({"file_key": "test", "quality": 2.0}))
        assert response["success"] is False
        assert "VALIDATION_ERROR" in str(response.get("error_code", ""))


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
"""Unit tests for FigmaExportController - Professional Test Suite."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
import json
import asyncio
from datetime import datetime, timezone
import logging


# Mock the logger before importing the module
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestRateLimitConfig:
    """Test rate limit configuration."""

    def test_default_values(self):
        """Test default rate limit values."""
        config = RateLimitConfig()
        assert config.requests_per_minute == 60
        assert config.burst_limit == 10

    def test_custom_values(self):
        """Test custom rate limit values."""
        config = RateLimitConfig(requests_per_minute=100, burst_limit=20)
        assert config.requests_per_minute == 100
        assert config.burst_limit == 20


class TestValidationResult:
    """Test validation result data structure."""

    def test_valid_result(self):
        """Test valid validation result."""
        result = ValidationResult(valid=True)
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_invalid_result(self):
        """Test invalid validation result."""
        result = ValidationResult(valid=False)
        result.errors.append("Missing file_key")

        assert result.valid is False
        assert len(result.errors) == 1

    def test_to_dict(self):
        """Test serialization to dictionary."""
        result = ValidationResult(valid=True, errors=["test"], warnings=["warn"])
        d = result.to_dict()
        assert d["valid"] is True
        assert d["errors"] == ["test"]
        assert d["warnings"] == ["warn"]


class TestExportResult:
    """Test export result data structure."""

    def test_export_result(self):
        """Test export result creation and serialization."""
        file_key = "test_file_123"
        result = ExportResult(file_key=file_key)

        assert result.file_key == file_key
        assert result.status == ExportStatus.COMPLETED
        assert isinstance(result.processed_at, datetime)

    def test_export_result_to_dict(self):
        """Test export result serialization."""
        result = ExportResult(file_key="test_123")
        d = result.to_dict()
        assert "file_key" in d
        assert "status" in d
        assert "processed_at" in d


class TestErrorResponse:
    """Test error response data structure."""

    def test_error_response_basic(self):
        """Test basic error response."""
        error = ErrorResponse(error_code="VALIDATION_ERROR", message="Invalid request")

        assert error.error_code == "VALIDATION_ERROR"
        dict_result = error.to_dict()
        assert dict_result["error"] == "VALIDATION_ERROR"
        assert dict_result["message"] == "Invalid request"


class TestFigmaExportController:
    """Comprehensive tests for FigmaExportController."""

    @pytest.fixture
    def controller(self):
        return FigmaExportController(
            rate_limit_config=RateLimitConfig(requests_per_minute=100, burst_limit=20)
        )

    @pytest.mark.asyncio
    async def test_handle_request_valid(self, controller):
        """Test successful export request."""
        with patch('sys.modules', {
            'figma_agent_core': MagicMock(),
            'figma_agent_core.export_to_png': AsyncMock(return_value={"success": True, "file_key": "mock_123"})
        }):
            response = await controller.handle_request({}, json.dumps({"file_key": "test", "quality": 1.0}))
            assert response["success"] is True

    @pytest.mark.asyncio
    async def test_handle_request_missing_file_key(self, controller):
        """Test request without file_key."""
        response = await controller.handle_request({}, json.dumps({"quality": 1.0}))
        assert response["success"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])