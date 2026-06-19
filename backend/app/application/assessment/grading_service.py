from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.question import Question, Attempt, Modality
from app.infrastructure.db.repositories import SQLQuestionRepository, SQLAttemptRepository
from app.application.tracing.bkt_service import KnowledgeTracingService


class GradingService:
    """Grades student answers and updates knowledge tracing."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.question_repo = SQLQuestionRepository(db)
        self.attempt_repo = SQLAttemptRepository(db)
        self.bkt_service = KnowledgeTracingService(db)

    async def grade_answer(
        self,
        student_id: UUID,
        question_id: UUID,
        response_text: str = "",
        response_audio_path: str | None = None,
    ) -> dict:
        question = await self.question_repo.get_by_id(question_id)
        if not question:
            raise ValueError(f"Question {question_id} not found")

        correct = self._check_correctness(question, response_text)

        modality = Modality.TEXT
        if response_audio_path:
            modality = Modality.ORAL

        attempt = Attempt(
            id=UUID(int=0),  # Will be assigned by DB
            student_id=student_id,
            question_id=question_id,
            skill_id=question.skill_id,
            correct=correct,
            response_text=response_text,
            response_audio_path=response_audio_path,
            modality=modality,
        )

        # Reset ID for DB generation
        from uuid import uuid4
        attempt.id = uuid4()
        saved_attempt = await self.attempt_repo.create(attempt)

        # Update BKT
        bkt_result = await self.bkt_service.update_mastery(
            student_id=student_id,
            skill_id=question.skill_id,
            correct=correct,
        )

        return {
            "attempt_id": saved_attempt.id,
            "correct": correct,
            "skill_id": question.skill_id,
            "p_mastery_new": bkt_result.p_mastery,
        }

    def _check_correctness(self, question: Question, response: str) -> bool:
        """Check if response matches the correct answer."""
        response_lower = response.strip().lower()
        answer_lower = question.correct_answer.strip().lower()

        # Exact match
        if response_lower == answer_lower:
            return True

        # MCQ: check option index
        if question.type.value == "mcq":
            try:
                idx = int(response)
                if 0 <= idx < len(question.options):
                    return question.options[idx].get("text", "").lower() == answer_lower
            except (ValueError, IndexError):
                pass

        # Cloze: check if answer is contained
        if question.type.value == "cloze":
            if answer_lower in response_lower or response_lower in answer_lower:
                return True

        # Token-level similarity fallback
        response_tokens = set(response_lower.split())
        answer_tokens = set(answer_lower.split())
        if answer_tokens:
            overlap = len(response_tokens & answer_tokens) / len(answer_tokens)
            if overlap >= 0.6:
                return True

        return False
