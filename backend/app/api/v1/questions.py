from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, require_role, UserRole
from app.api.schemas.question import (
    QuestionCreate, QuestionResponse,
    GradeRequest, GradeResponse,
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/generate-batch")
async def generate_questions(
    body: QuestionCreate,
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.application.assessment.question_generator import QuestionGeneratorService
    from app.infrastructure.db.repositories import SQLContentChunkRepository

    chunk_repo = SQLContentChunkRepository(db)
    generator = QuestionGeneratorService(chunk_repo)

    question_ids = []
    for concept_id_str in body.concept_ids:
        questions = await generator.generate_for_concept(
            lesson_id=UUID(body.lesson_id),
            concept_id=UUID(concept_id_str),
            num_questions=body.num_questions_per_concept,
        )
        question_ids.extend([str(q.id) for q in questions])

    return {"question_ids": question_ids, "count": len(question_ids)}


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.infrastructure.db.repositories import SQLQuestionRepository

    repo = SQLQuestionRepository(db)
    question = await repo.get_by_id(UUID(question_id))
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionResponse(
        id=str(question.id),
        type=question.type.value,
        lesson_id=str(question.lesson_id),
        concept_id=str(question.concept_id),
        skill_id=str(question.skill_id),
        stem=question.stem,
        options=question.options,
        difficulty=question.difficulty,
        source_chunk_ids=[str(cid) for cid in question.source_chunk_ids],
    )
