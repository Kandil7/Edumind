"""Integration tests for the full API using FastAPI TestClient."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch, MagicMock

from fastapi.testclient import TestClient
from httpx import AsyncClient


# Mock the database dependency for all tests
@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    return session


@pytest.fixture
def client(mock_db_session):
    from app.main import app
    from app.core.database import get_db

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "edumind"

    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "EduMind"
        assert "docs" in data


class TestAuthEndpoints:
    def test_register_requires_body(self, client):
        response = client.post("/api/v1/auth/register")
        assert response.status_code == 422  # Validation error

    def test_login_requires_body(self, client):
        response = client.post("/api/v1/auth/login")
        assert response.status_code == 422

    def test_me_requires_token(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403  # No auth header


class TestContentEndpoints:
    def test_list_lessons_empty(self, client, mock_db_session):
        from sqlalchemy import Result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result

        response = client.get("/api/v1/content/lessons")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_lesson_requires_auth(self, client):
        response = client.post("/api/v1/content/lessons", json={
            "title": "Test",
            "subject": "Math",
            "grade_level": "10",
        })
        assert response.status_code == 403

    def test_upload_requires_auth(self, client):
        response = client.post("/api/v1/content/sources/upload")
        assert response.status_code == 403


class TestQuestionEndpoints:
    def test_get_question_requires_auth(self, client):
        response = client.get(f"/api/v1/questions/{uuid4()}")
        assert response.status_code == 403

    def test_generate_batch_requires_auth(self, client):
        response = client.post("/api/v1/questions/generate-batch", json={
            "lesson_id": str(uuid4()),
            "concept_ids": [str(uuid4())],
            "num_questions_per_concept": 5,
        })
        assert response.status_code == 403


class TestTracingEndpoints:
    def test_update_requires_auth(self, client):
        response = client.post("/api/v1/tracing/update", json={
            "student_id": str(uuid4()),
            "skill_id": str(uuid4()),
            "correct": True,
        })
        assert response.status_code == 403


class TestTutorEndpoints:
    def test_session_step_requires_auth(self, client):
        response = client.post("/api/v1/tutor/session/step", json={
            "student_id": str(uuid4()),
            "lesson_id": str(uuid4()),
        })
        assert response.status_code == 403

    def test_ask_requires_auth(self, client):
        response = client.post(
            f"/api/v1/tutor/ask?lesson_id={uuid4()}&query=test"
        )
        assert response.status_code == 403


class TestSpeechEndpoints:
    def test_tts_requires_auth(self, client):
        response = client.post("/api/v1/speech/tts", json={
            "text": "مرحبا",
            "language": "ar",
        })
        assert response.status_code == 403

    def test_asr_requires_auth(self, client):
        response = client.post("/api/v1/speech/asr")
        assert response.status_code == 403
