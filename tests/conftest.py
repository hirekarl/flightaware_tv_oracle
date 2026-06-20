"""Shared pytest fixtures for the backend test suite."""

import pytest

from backend.main import _ai_cache


@pytest.fixture(autouse=True)
def clear_ai_cache() -> None:
    """Reset the module-level AI analysis cache before every test.

    Prevents cache entries written by one test from suppressing coordinator
    calls in a later test, which would cause false passes or false failures
    depending on execution order.
    """
    _ai_cache.clear()
