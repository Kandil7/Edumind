"""Tests for Knowledge Tracing (BKT) service."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.application.tracing.bkt_service import KnowledgeTracingService
from app.domain.entities.student import StudentSkillState


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def mock_state_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def bkt_service(mock_db, mock_state_repo):
    service = KnowledgeTracingService.__new__(KnowledgeTracingService)
    service.db = mock_db
    service.state_repo = mock_state_repo
    return service


class TestBKTUpdate:
    def test_default_parameters(self):
        assert KnowledgeTracingService.DEFAULT_P_KNOW == 0.3
        assert KnowledgeTracingService.DEFAULT_P_LEARN == 0.4
        assert KnowledgeTracingService.DEFAULT_P_GUESS == 0.2
        assert KnowledgeTracingService.DEFAULT_P_SLIP == 0.1

    @pytest.mark.asyncio
    async def test_update_correct_answer_increases_mastery(self, bkt_service, mock_state_repo):
        student_id = uuid4()
        skill_id = uuid4()

        # Initial state: low mastery
        initial_state = StudentSkillState(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=0.3,
            num_attempts=0,
            initialized=True,
        )
        mock_state_repo.get_or_create.return_value = initial_state
        mock_state_repo.update_mastery.return_value = StudentSkillState(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=0.5,
            num_attempts=1,
            initialized=True,
        )

        result = await bkt_service.update_mastery(student_id, skill_id, correct=True)

        assert result.p_mastery > 0.3
        mock_state_repo.update_mastery.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_wrong_answer_decreases_mastery(self, bkt_service, mock_state_repo):
        student_id = uuid4()
        skill_id = uuid4()

        initial_state = StudentSkillState(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=0.7,
            num_attempts=0,
            initialized=True,
        )
        mock_state_repo.get_or_create.return_value = initial_state
        mock_state_repo.update_mastery.return_value = StudentSkillState(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=0.5,
            num_attempts=1,
            initialized=True,
        )

        result = await bkt_service.update_mastery(student_id, skill_id, correct=False)

        assert result.p_mastery < 0.7
        mock_state_repo.update_mastery.assert_called_once()

    @pytest.mark.asyncio
    async def test_initialization_sets_prior(self, bkt_service, mock_state_repo):
        student_id = uuid4()
        skill_id = uuid4()

        # Uninitialized state
        initial_state = StudentSkillState(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=0.0,
            num_attempts=0,
            initialized=False,
        )
        mock_state_repo.get_or_create.return_value = initial_state
        mock_state_repo.update_mastery.return_value = StudentSkillState(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=0.5,
            num_attempts=1,
            initialized=True,
        )

        result = await bkt_service.update_mastery(student_id, skill_id, correct=True)

        assert result.initialized is True
        assert result.p_mastery > 0.0

    def test_mastery_clamped_to_bounds(self):
        from app.domain.entities.student import MasteryScore

        # Valid scores
        MasteryScore(0.0)
        MasteryScore(0.5)
        MasteryScore(1.0)

        # Invalid scores should raise
        with pytest.raises(ValueError):
            MasteryScore(-0.1)
        with pytest.raises(ValueError):
            MasteryScore(1.1)
