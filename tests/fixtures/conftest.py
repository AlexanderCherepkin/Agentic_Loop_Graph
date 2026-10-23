"""Pytest fixtures for test data and utilities."""
import pytest


@pytest.fixture(scope="session")
def sample_data():
    """Sample test data fixture."""
    return {
        "name": "test_item",
        "value": 42,
        "active": True
    }


@pytest.fixture
def sample_list():
    """List fixture for testing."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def empty_dict():
    """Empty dictionary fixture."""
    return {}