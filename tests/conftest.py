"""Shared test setup."""

import os

# Safe settings for tests. These must be set before the app is imported.
os.environ["EAIOS_ANTHROPIC_API_KEY"] = "test-key-not-real"
os.environ["EAIOS_ENVIRONMENT"] = "development"
os.environ["EAIOS_LOG_CHAT_CONTENT"] = "false"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402 - This comment makes sure that the Ruff skips these checks (e.g., the imports should come at top)

from eaios.app import app  # noqa: E402


@pytest.fixture
def client():
    """A test client that sends requests to the app without a real server."""
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
