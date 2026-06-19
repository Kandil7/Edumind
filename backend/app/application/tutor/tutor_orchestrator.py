from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.content import ContentChunk
from app.infrastructure.db.repositories import (
    SQLContentChunkRepository,
    SQLStudentSkillStateRepository,
    SQLConceptRepository,
    SQLSkillRepository,
)
from app.application.content.rag_service import RAGService


class TutorOrchestrator:
    """Orchestrates adaptive tutoring sessions using a state machine approach.

    Flow:
    1. Grade previous answer (if any)
    2. Get student mastery profile for lesson
    3. Select weakest skill
    4. If mastery < EXPLAIN_THRESHOLD → provide explanation with sources
    5. If mastery >= EXPLAIN_THRESHOLD → find and serve a question
    6. If no questions available → generate one on-the-fly
    7. If all skills mastered → FINISHED
    """

    MASTERY_THRESHOLD = 0.4    # Below this: must explain first
    EXPLAIN_THRESHOLD = 0.6    # Above this: ready for questions
    MAX_STEPS = 20             # Safety limit per session

    def __init__(self, db: AsyncSession):
        self.db = db
        self.chunk_repo = SQLContentChunkRepository(db)
        self.skill_state_repo = SQLStudentSkillStateRepository(db)
        self.concept_repo = SQLConceptRepository(db)
        self.skill_repo = SQLSkillRepository(db)
        self.rag = RAGService(db)

    async def step(
        self,
        student_id: UUID,
        lesson_id: UUID,
        last_question_id: UUID | None = None,
        last_response: str | None = None,
    ) -> dict:
        # Step 1: Grade previous answer if provided
        if last_question_id and last_response is not None:
            await self._grade_last_answer(student_id, last_question_id, last_response)

        # Step 2: Get all concepts and skills for this lesson
        concepts = await self.concept_repo.list_by_lesson(lesson_id)
        if not concepts:
            return {"action": "FINISHED", "reason": "no_concepts"}

        # Step 3: Find the weakest skill across all concepts
        weakest_skill_id, lowest_mastery = await self._find_weakest_skill(student_id, concepts)

        if weakest_skill_id is None:
            return {"action": "FINISHED", "reason": "all_mastered"}

        # Step 4: Decide action based on mastery level
        if lowest_mastery < self.MASTERY_THRESHOLD:
            return await self._explain_concept(lesson_id, weakest_skill_id)
        else:
            return await self._serve_question(student_id, weakest_skill_id)

    async def _grade_last_answer(self, student_id: UUID, question_id: UUID, response: str):
        """Grade the previous answer and update mastery."""
        from app.application.assessment.grading_service import GradingService
        grading = GradingService(self.db)
        try:
            await grading.grade_answer(
                student_id=student_id,
                question_id=question_id,
                response_text=response,
            )
        except (ValueError, Exception) as e:
            # Log but don't fail the session
            pass

    async def _find_weakest_skill(self, student_id: UUID, concepts) -> tuple[UUID | None, float]:
        """Find the skill with lowest mastery across all lesson concepts."""
        weakest_skill_id = None
        lowest_mastery = 1.0

        for concept in concepts:
            # Get skills for this concept
            skills = await self.skill_repo.list_by_concept(concept.id)
            for skill in skills:
                state = await self.skill_state_repo.get_or_create(student_id, skill.id)
                if state.p_mastery < lowest_mastery:
                    lowest_mastery = state.p_mastery
                    weakest_skill_id = skill.id

        return weakest_skill_id, lowest_mastery

    async def _explain_concept(self, lesson_id: UUID, skill_id: UUID) -> dict:
        """Provide an explanation for a concept with low mastery."""
        chunks = await self.chunk_repo.list_by_lesson(lesson_id)

        # Find chunks relevant to this skill's concept
        skill = await self.skill_repo.get_by_id(skill_id)
        if not skill:
            return {"action": "FINISHED", "reason": "skill_not_found"}

        concept_chunks = [c for c in chunks if c.concept_id == skill.concept_id]

        if concept_chunks:
            # Build explanation from content chunks
            context = "\n".join([c.content for c in concept_chunks[:5]])
            explanation = f"💡 شرح مبسّط:\n\n{context}"

            sources = [
                {
                    "source_id": str(c.source_id),
                    "source_name": c.metadata.get("source_name", "المحتوى التعليمي"),
                    "source_type": c.source_type.value,
                    "start_offset": c.start_offset,
                    "end_offset": c.end_offset,
                }
                for c in concept_chunks[:3]
            ]
        else:
            explanation = "لا يوجد محتوى شرح متاح لهذا المفهوم بعد. يمكنك محاولة سؤال آخر."
            sources = []

        return {
            "action": "EXPLAIN",
            "skill_id": str(skill_id),
            "explanation": explanation,
            "sources": sources,
            "question": None,
        }

    async def _serve_question(self, student_id: UUID, skill_id: UUID) -> dict:
        """Find or generate a question for the given skill."""
        from app.infrastructure.db.repositories import SQLQuestionRepository
        question_repo = SQLQuestionRepository(self.db)

        # Try to find an existing question
        question = await question_repo.find_for_student(
            skill_id=skill_id,
            student_id=student_id,
        )

        if question:
            return {
                "action": "QUESTION",
                "skill_id": str(skill_id),
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

        # No questions available — generate one on-the-fly from content
        return await self._generate_on_the_fly(student_id, skill_id)

    async def _generate_on_the_fly(self, student_id: UUID, skill_id: UUID) -> dict:
        """Generate a question dynamically when none exist in the bank."""
        skill = await self.skill_repo.get_by_id(skill_id)
        if not skill:
            return {"action": "FINISHED", "reason": "skill_not_found"}

        # Find chunks for this concept
        chunks = await self.chunk_repo.list_by_lesson(UUID(int(0)))  # Need lesson_id
        # Fallback: search by concept
        from app.application.assessment.question_generator import QuestionGeneratorService
        generator = QuestionGeneratorService(self.db)

        # Get the concept's lesson
        concept = await self.concept_repo.get_by_id(skill.concept_id)
        if not concept:
            return {"action": "FINISHED", "reason": "concept_not_found"}

        questions = await generator.generate_for_concept(
            lesson_id=concept.lesson_id,
            concept_id=concept.id,
            num_questions=1,
        )

        if questions:
            q = questions[0]
            return {
                "action": "QUESTION",
                "skill_id": str(skill_id),
                "explanation": None,
                "sources": None,
                "question": {
                    "id": str(q.id),
                    "type": q.type.value,
                    "stem": q.stem,
                    "options": q.options,
                    "difficulty": q.difficulty,
                },
            }

        return {"action": "FINISHED", "reason": "no_content_available"}
