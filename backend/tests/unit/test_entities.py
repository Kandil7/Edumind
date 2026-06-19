"""Tests for domain entities."""
import pytest
from uuid import uuid4

from app.domain.entities.content import (
    ContentSource, Lesson, Concept, Skill, ContentChunk,
    SourceType, SourceOrigin, SourceLocator,
)
from app.domain.entities.student import Student, StudentSkillState, MasteryScore
from app.domain.entities.question import Question, Attempt, QuestionType, Modality
from app.domain.entities.misconception import Misconception, MisconceptionInstance


class TestSourceLocator:
    def test_to_dict(self):
        locator = SourceLocator(
            source_id=uuid4(),
            source_name="Calculus Book",
            source_type=SourceType.TEXT,
            start_offset=100.0,
            end_offset=200.0,
        )
        d = locator.to_dict()
        assert d["source_name"] == "Calculus Book"
        assert d["source_type"] == "text"
        assert d["start_offset"] == 100.0

    def test_to_dict_audio(self):
        locator = SourceLocator(
            source_id=uuid4(),
            source_name="Lecture 1",
            source_type=SourceType.AUDIO,
            start_offset=60.0,
            end_offset=120.0,
        )
        d = locator.to_dict()
        assert d["source_type"] == "audio"


class TestMasteryScore:
    def test_valid_scores(self):
        assert MasteryScore(0.0).value == 0.0
        assert MasteryScore(0.5).value == 0.5
        assert MasteryScore(1.0).value == 1.0

    def test_invalid_scores(self):
        with pytest.raises(ValueError):
            MasteryScore(-0.1)
        with pytest.raises(ValueError):
            MasteryScore(1.1)

    def test_is_mastered(self):
        assert MasteryScore(0.8).is_mastered is True
        assert MasteryScore(0.9).is_mastered is True
        assert MasteryScore(0.7).is_mastered is False

    def test_needs_remediation(self):
        assert MasteryScore(0.2).needs_remédiation is True
        assert MasteryScore(0.3).needs_remédiation is True
        assert MasteryScore(0.5).needs_remédiation is False

    def test_repr(self):
        assert "MasteryScore" in repr(MasteryScore(0.5))


class TestContentEntities:
    def test_content_source_creation(self):
        source = ContentSource(
            id=uuid4(),
            type=SourceType.TEXT,
            origin=SourceOrigin.BOOK,
            title="Calculus",
            language="ar",
        )
        assert source.title == "Calculus"
        assert source.type == SourceType.TEXT

    def test_lesson_creation(self):
        lesson = Lesson(
            id=uuid4(),
            title="Derivatives",
            subject="Math",
            grade_level="10",
            language="en",
        )
        assert lesson.is_active is True

    def test_concept_creation(self):
        concept = Concept(
            id=uuid4(),
            lesson_id=uuid4(),
            name="Chain Rule",
            difficulty_level=2,
        )
        assert concept.difficulty_level == 2

    def test_skill_creation(self):
        skill = Skill(
            id=uuid4(),
            concept_id=uuid4(),
            name="Apply chain rule",
        )
        assert len(skill.name) > 0


class TestStudentEntities:
    def test_student_creation(self):
        student = Student(
            id=uuid4(),
            name="Ahmed",
            email="ahmed@test.com",
        )
        assert student.preferred_language == "ar"
        assert student.level == "beginner"

    def test_skill_state_creation(self):
        state = StudentSkillState(
            student_id=uuid4(),
            skill_id=uuid4(),
            p_mastery=0.5,
        )
        assert state.p_mastery == 0.5
        assert state.num_attempts == 0


class TestQuestionEntities:
    def test_question_creation(self):
        q = Question(
            id=uuid4(),
            type=QuestionType.CLOZE,
            lesson_id=uuid4(),
            concept_id=uuid4(),
            skill_id=uuid4(),
            stem="Complete: x² → ___",
            correct_answer="2x",
        )
        assert q.difficulty == 1
        assert len(q.options) == 0

    def test_attempt_creation(self):
        a = Attempt(
            id=uuid4(),
            student_id=uuid4(),
            question_id=uuid4(),
            skill_id=uuid4(),
            correct=True,
            response_text="2x",
        )
        assert a.correct is True
        assert a.modality == Modality.TEXT


class TestMisconceptionEntities:
    def test_misconception_creation(self):
        m = Misconception(
            id=uuid4(),
            skill_id=uuid4(),
            description="Student confuses product rule with chain rule",
        )
        assert len(m.description) > 0

    def test_instance_creation(self):
        inst = MisconceptionInstance(
            id=uuid4(),
            student_id=uuid4(),
            misconception_id=uuid4(),
            num_occurrences=3,
        )
        assert inst.num_occurrences == 3
