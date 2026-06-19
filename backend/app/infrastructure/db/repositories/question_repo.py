from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.question import Question, Attempt, QuestionType, Modality
from app.domain.interfaces.assessment_repository import QuestionRepository, AttemptRepository
from app.infrastructure.db.models.question import QuestionModel, AttemptModel


def _model_to_question(m: QuestionModel) -> Question:
    return Question(
        id=m.id,
        type=QuestionType(m.type),
        lesson_id=m.lesson_id,
        concept_id=m.concept_id,
        skill_id=m.skill_id,
        stem=m.stem,
        correct_answer=m.correct_answer,
        difficulty=m.difficulty,
        options=m.options or [],
        source_chunk_ids=m.source_chunk_ids or [],
        generator_metadata=m.generator_metadata or {},
    )


def _model_to_attempt(m: AttemptModel) -> Attempt:
    return Attempt(
        id=m.id,
        student_id=m.student_id,
        question_id=m.question_id,
        skill_id=m.skill_id,
        correct=m.correct,
        response_text=m.response_text or "",
        response_audio_path=m.response_audio_path,
        modality=Modality(m.modality),
        created_at=m.created_at,
        metadata=m.metadata_ or {},
    )


class SQLQuestionRepository(QuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, question: Question) -> Question:
        model = QuestionModel(
            id=question.id,
            type=question.type.value,
            lesson_id=question.lesson_id,
            concept_id=question.concept_id,
            skill_id=question.skill_id,
            stem=question.stem,
            options=question.options,
            correct_answer=question.correct_answer,
            difficulty=question.difficulty,
            source_chunk_ids=[str(cid) for cid in question.source_chunk_ids],
            generator_metadata=question.generator_metadata,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_question(model)

    async def create_many(self, questions: list[Question]) -> list[Question]:
        models = []
        for q in questions:
            model = QuestionModel(
                id=q.id,
                type=q.type.value,
                lesson_id=q.lesson_id,
                concept_id=q.concept_id,
                skill_id=q.skill_id,
                stem=q.stem,
                options=q.options,
                correct_answer=q.correct_answer,
                difficulty=q.difficulty,
                source_chunk_ids=[str(cid) for cid in q.source_chunk_ids],
                generator_metadata=q.generator_metadata,
            )
            self.session.add(model)
            models.append(model)
        await self.session.flush()
        return [_model_to_question(m) for m in models]

    async def get_by_id(self, id: UUID) -> Question | None:
        result = await self.session.execute(
            select(QuestionModel).where(QuestionModel.id == id)
        )
        model = result.scalar_one_or_none()
        return _model_to_question(model) if model else None

    async def list_by_lesson(self, lesson_id: UUID) -> list[Question]:
        result = await self.session.execute(
            select(QuestionModel).where(QuestionModel.lesson_id == lesson_id)
        )
        return [_model_to_question(m) for m in result.scalars().all()]

    async def list_by_skill(self, skill_id: UUID) -> list[Question]:
        result = await self.session.execute(
            select(QuestionModel).where(QuestionModel.skill_id == skill_id)
        )
        return [_model_to_question(m) for m in result.scalars().all()]

    async def find_for_student(
        self,
        skill_id: UUID,
        student_id: UUID,
        difficulty: int | None = None,
        exclude_recent: int = 5,
    ) -> Question | None:
        # Find questions for skill, excluding recently attempted ones
        subquery = (
            select(AttemptModel.question_id)
            .where(AttemptModel.student_id == student_id)
            .order_by(AttemptModel.created_at.desc())
            .limit(exclude_recent)
        )
        query = (
            select(QuestionModel)
            .where(
                QuestionModel.skill_id == skill_id,
                QuestionModel.id.notin_(subquery),
            )
        )
        if difficulty is not None:
            query = query.where(QuestionModel.difficulty == difficulty)
        query = query.order_by(QuestionModel.difficulty).limit(1)

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return _model_to_question(model) if model else None


class SQLAttemptRepository(AttemptRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, attempt: Attempt) -> Attempt:
        model = AttemptModel(
            id=attempt.id,
            student_id=attempt.student_id,
            question_id=attempt.question_id,
            skill_id=attempt.skill_id,
            correct=attempt.correct,
            response_text=attempt.response_text,
            response_audio_path=attempt.response_audio_path,
            modality=attempt.modality.value,
            metadata_=attempt.metadata,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_attempt(model)

    async def list_by_student(self, student_id: UUID) -> list[Attempt]:
        result = await self.session.execute(
            select(AttemptModel)
            .where(AttemptModel.student_id == student_id)
            .order_by(AttemptModel.created_at.desc())
        )
        return [_model_to_attempt(m) for m in result.scalars().all()]

    async def list_by_student_skill(self, student_id: UUID, skill_id: UUID) -> list[Attempt]:
        result = await self.session.execute(
            select(AttemptModel)
            .where(
                AttemptModel.student_id == student_id,
                AttemptModel.skill_id == skill_id,
            )
            .order_by(AttemptModel.created_at.desc())
        )
        return [_model_to_attempt(m) for m in result.scalars().all()]

    async def get_wrong_attempts_by_skill(self, skill_id: UUID) -> list[Attempt]:
        result = await self.session.execute(
            select(AttemptModel)
            .where(
                AttemptModel.skill_id == skill_id,
                AttemptModel.correct == False,
            )
            .order_by(AttemptModel.created_at.desc())
        )
        return [_model_to_attempt(m) for m in result.scalars().all()]
