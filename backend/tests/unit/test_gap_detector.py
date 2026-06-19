"""Tests for gap detector service."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from app.application.gap_detector.gap_service import GapDetectorService
from app.domain.entities.question import Attempt, Modality


class TestGapDetector:
    """Test misconception detection from wrong answers."""

    def setup_method(self):
        self.gap = GapDetectorService.__new__(GapDetectorService)
        self.gap.attempt_repo = AsyncMock()
        self.gap.misconception_repo = AsyncMock()
        self.gap.instance_repo = AsyncMock()

    @pytest.mark.asyncio
    async def test_no_wrong_attempts_returns_empty(self):
        self.gap.attempt_repo.get_wrong_attempts_by_skill = AsyncMock(return_value=[])
        result = await self.gap.analyze_skill_gaps(uuid4())
        assert result == []

    @pytest.mark.asyncio
    async def test_groups_wrong_attempts_by_pattern(self):
        skill_id = uuid4()
        student1 = uuid4()
        student2 = uuid4()

        attempts = [
            Attempt(id=uuid4(), student_id=student1, question_id=uuid4(),
                    skill_id=skill_id, correct=False, response_text="2x is the answer"),
            Attempt(id=uuid4(), student_id=student2, question_id=uuid4(),
                    skill_id=skill_id, correct=False, response_text="2x is the answer too"),
            Attempt(id=uuid4(), student_id=student1, question_id=uuid4(),
                    skill_id=skill_id, correct=False, response_text="x squared"),
        ]
        self.gap.attempt_repo.get_wrong_attempts_by_skill = AsyncMock(return_value=attempts)
        self.gap.misconception_repo.find_similar = AsyncMock(return_value=None)

        from app.domain.entities.misconception import Misconception
        mock_misconception = Misconception(
            id=uuid4(), skill_id=skill_id, description="test"
        )
        self.gap.misconception_repo.create = AsyncMock(return_value=mock_misconception)
        self.gap.instance_repo.upsert = AsyncMock()

        result = await self.gap.analyze_skill_gaps(skill_id)

        # Should find patterns with >= 2 occurrences
        assert len(result) >= 1
        assert "misconception_id" in result[0]
        assert "description" in result[0]

    @pytest.mark.asyncio
    async def test_skips_patterns_with_single_occurrence(self):
        skill_id = uuid4()
        attempts = [
            Attempt(id=uuid4(), student_id=uuid4(), question_id=uuid4(),
                    skill_id=skill_id, correct=False, response_text="unique answer"),
        ]
        self.gap.attempt_repo.get_wrong_attempts_by_skill = AsyncMock(return_value=attempts)

        result = await self.gap.analyze_skill_gaps(skill_id)
        assert len(result) == 0
