"""Tests for question generation service."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from app.application.assessment.question_generator import QuestionGeneratorService
from app.domain.entities.content import ContentChunk, SourceType
from app.domain.entities.question import QuestionType


class TestQuestionGenerator:
    """Test question generation from content chunks."""

    def setup_method(self):
        self.generator = QuestionGeneratorService.__new__(QuestionGeneratorService)
        self.generator.chunk_repo = AsyncMock()
        self.generator.question_repo = AsyncMock()

    def test_generate_cloze(self):
        chunk = ContentChunk(
            id=uuid4(),
            source_id=uuid4(),
            lesson_id=uuid4(),
            concept_id=uuid4(),
            content="المشتقة للدالة f(x) عند نقطة x=a هي الميل الإنسياسي لخط المماس",
            source_type=SourceType.TEXT,
        )
        question = self.generator._generate_cloze(chunk)
        assert question is not None
        assert question.type == QuestionType.CLOZE
        assert "_____" in question.stem
        assert len(question.correct_answer) > 0
        assert len(question.source_chunk_ids) == 1

    def test_generate_cloze_short_text_returns_none(self):
        chunk = ContentChunk(
            id=uuid4(),
            source_id=uuid4(),
            lesson_id=uuid4(),
            concept_id=uuid4(),
            content="short",
            source_type=SourceType.TEXT,
        )
        question = self.generator._generate_cloze(chunk)
        assert question is None

    def test_generate_mcq(self):
        chunk = ContentChunk(
            id=uuid4(),
            source_id=uuid4(),
            lesson_id=uuid4(),
            concept_id=uuid4(),
            content="المشتقة للدالة f(x) عند نقطة x=a هي الميل الإنسياسي",
            source_type=SourceType.TEXT,
        )
        question = self.generator._generate_mcq(chunk)
        assert question is not None
        assert question.type == QuestionType.MCQ
        assert len(question.options) == 3
        assert question.options[0]["id"] == 0

    def test_generate_open_text(self):
        chunk = ContentChunk(
            id=uuid4(),
            source_id=uuid4(),
            lesson_id=uuid4(),
            concept_id=uuid4(),
            content="المشتقة هي الميل الإنسياسي لخط المماس عند نقطة معينة",
            source_type=SourceType.TEXT,
        )
        question = self.generator._generate_open_text(chunk)
        assert question is not None
        assert question.type == QuestionType.OPEN_TEXT
        assert len(question.correct_answer) > 0

    def test_question_has_source_provenance(self):
        chunk = ContentChunk(
            id=uuid4(),
            source_id=uuid4(),
            lesson_id=uuid4(),
            concept_id=uuid4(),
            content="This is a test chunk with enough words to generate a question from it",
            source_type=SourceType.TEXT,
        )
        question = self.generator._generate_cloze(chunk)
        assert question is not None
        assert len(question.source_chunk_ids) == 1
        assert question.source_chunk_ids[0] == chunk.id
