"""Tests for question grading service."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.application.assessment.grading_service import GradingService
from app.domain.entities.question import Question, QuestionType


class TestGradingLogic:
    """Test grading correctness checking (sync logic, no DB needed)."""

    def setup_method(self):
        self.grading = GradingService.__new__(GradingService)

    def test_exact_match_cloze(self):
        question = Question(
            id=uuid4(),
            type=QuestionType.CLOZE,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="أكمل: المشتقة لـ x² هي ___",
            correct_answer="2x",
        )
        assert self.grading._check_correctness(question, "2x") is True
        assert self.grading._check_correctness(question, "2X") is True
        assert self.grading._check_correctness(question, "3x") is False

    def test_exact_match_mcq(self):
        question = Question(
            id=uuid4(),
            type=QuestionType.MCQ,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="ما مشتقة x²؟",
            correct_answer="2x",
            options=[
                {"id": 0, "text": "2x"},
                {"id": 1, "text": "x²"},
                {"id": 2, "text": "2"},
            ],
        )
        assert self.grading._check_correctness(question, "0") is True
        assert self.grading._check_correctness(question, "1") is False
        assert self.grading._check_correctness(question, "2") is False

    def test_cloze_containment(self):
        question = Question(
            id=uuid4(),
            type=QuestionType.CLOZE,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="Complete: the derivative of x² is ___",
            correct_answer="2x",
        )
        # Containment check
        assert self.grading._check_correctness(question, "The answer is 2x") is True

    def test_token_overlap_fallback(self):
        question = Question(
            id=uuid4(),
            type=QuestionType.OPEN_TEXT,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="اشرح المشتقة",
            correct_answer="المشتقة هي الميل الإنسياسي لخط المماس",
        )
        # High overlap should pass
        assert self.grading._check_correctness(
            question, "المشتقة هي الميل الإنسياسي لخط المماس عند نقطة"
        ) is True

    def test_no_match(self):
        question = Question(
            id=uuid4(),
            type=QuestionType.OPEN_TEXT,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="اشرح",
            correct_answer="المشتقة هي الميل الإنسياسي",
        )
        assert self.grading._check_correctness(question, "لا أعرف") is False

    def test_cloze_arabic(self):
        question = Question(
            id=uuid4(),
            type=QuestionType.CLOZE,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="أكمل: قاعدة السلسلة هي ___",
            correct_answer="f'(g(x)) · g'(x)",
        )
        assert self.grading._check_correctness(question, "f'(g(x)) · g'(x)") is True
        assert self.grading._check_correctness(question, "f'(g(x))*g'(x)") is False
