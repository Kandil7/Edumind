"""Shared test fixtures."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock


@pytest.fixture
def sample_student_id():
    return uuid4()


@pytest.fixture
def sample_skill_id():
    return uuid4()


@pytest.fixture
def sample_lesson_id():
    return uuid4()


@pytest.fixture
def sample_concept_id():
    return uuid4()


@pytest.fixture
def mock_async_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()
    return session
