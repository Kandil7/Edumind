from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.content import ContentChunk
from app.infrastructure.db.repositories import (
    SQLContentChunkRepository,
    SQLStudentSkillStateRepository,
    SQLConceptRepository,
)
from app.application.content.rag_service import RAGService


class TutorOrchestrator:
    """Orchestrates adaptive tutoring sessions using a state machine approach."""

    MASTERY_THRESHOLD = 0.4
    EXPLAIN_THRESHOLD = 0.6
    MAX_CONSECUTIVE_WRONG = 2

    def __init__(self, db: AsyncSession):
        self.db = db
        self.chunk_repo = SQLContentChunkRepository(db)
        self.skill_state_repo = SQLStudentSkillStateRepository(db)
        self.concept_repo = SQLConceptRepository(db)
        self.rag = RAGService(db)

    async def step(
        self,
        student_id: UUID,
        lesson_id: UUID,
        last_question_id: UUID | None = None,
        last_response: str | None = None,
    ) -> dict:
        # If there was a last question, grade it
        if last_question_id and last_response is not None:
            from app.application.assessment.grading_service import GradingService
            grading = GradingService(self.db)
            try:
                grade_result = await grading.grade_answer(
                    student_id=student_id,
                    question_id=last_question_id,
                    response_text=last_response,
                )
            except ValueError:
                pass

        # Get student profile for this lesson's concepts
        concepts = await self.concept_repo.list_by_lesson(lesson_id)
        if not concepts:
            return {"action": "FINISHED"}

        # Find the weakest skill
        weakest_skill_id = None
        lowest_mastery = 1.0

        for concept in concepts:
            state = await self.skill_state_repo.get_or_create(student_id, concept.id)
            if state.p_mastery < lowest_mastery:
                lowest_mastery = state.p_mastery
                weakest_skill_id = concept.id

        if weakest_skill_id is None:
            return {"action": "FINISHED"}

        # Decide: explain or question?
        if lowest_mastery < self.MASTERY_THRESHOLD:
            # Need explanation
            chunks = await self.chunk_repo.list_by_lesson(lesson_id)
            concept_chunks = [c for c in chunks if c.concept_id == weakest_skill_id]

            if concept_chunks:
                context = "\n".join([c.content for c in concept_chunks[:3]])
                explanation = f"شرح مبسّط للمفهوم:\n{context[:500]}"

                sources = [
                    {
                        "source_id": str(c.source_id),
                        "source_name": c.metadata.get("source_name", "المحتوى التعليمي"),
                        "source_type": c.source_type.value,
                    }
                    for c in concept_chunks[:3]
                ]
            else:
                explanation = "لا يوجد محتوى متاح لهذا المفهوم بعد."
                sources = []

            return {
                "action": "EXPLAIN",
                "skill_id": str(weakest_skill_id),
                "explanation": explanation,
                "sources": sources,
                "question": None,
            }

        else:
            # Find an appropriate question
            from app.infrastructure.db.repositories import SQLQuestionRepository
            question_repo = SQLQuestionRepository(self.db)
            question = await question_repo.find_for_student(
                skill_id=weakest_skill_id,
                student_id=student_id,
            )

            if question:
                return {
                    "action": "QUESTION",
                    "skill_id": str(weakest_skill_id),
                    "explanation": None,
                    "sources": None,
                    "question": {
                        "id": str(question.id),
                        "type": question.type.value,
                        "stem": question.stem,
                        "options": question.options,
                        "difficulty": question.difficulty,
                    },
                }

            return {"action": "FINISHED"}
