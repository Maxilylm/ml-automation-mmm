"""Shared pytest fixtures for ml-automation-mmm."""

import pytest


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing without live API calls."""
    return {
        "id": "test-run-123",
        "content": [
            {
                "type": "text",
                "text": "Test MMM model initialized successfully."
            }
        ],
        "model": "claude-opus-4-7",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50
        }
    }


@pytest.fixture
def sample_dataset():
    """Sample dataset for testing MMM workflows."""
    return {
        "media_channels": ["tv", "radio", "digital"],
        "spend": [1000, 500, 2000],
        "impressions": [1000000, 500000, 5000000],
        "sales": [5000, 2500, 12000],
        "date_range": "2024-01-01 to 2024-12-31"
    }


@pytest.fixture
def temp_workspace(tmp_path):
    """Temporary workspace directory for test isolation."""
    workspace = tmp_path / "mmm_workspace"
    workspace.mkdir(exist_ok=True)
    (workspace / "models").mkdir(exist_ok=True)
    (workspace / "reports").mkdir(exist_ok=True)
    (workspace / "data").mkdir(exist_ok=True)
    return workspace
