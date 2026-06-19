from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.api.schemas.tracing import TutorStepRequest, TutorStepResponse

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.post("/session/step", response_model=TutorStepResponse)
async def tutor_session_step(
    body: TutorStepRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.application.tutor.tutor_orchestrator import TutorOrchestrator

    orchestrator = TutorOrchestrator(db)
    result = await orchestrator.step(
        student_id=UUID(body.student_id),
        lesson_id=UUID(body.lesson_id),
        last_question_id=UUID(body.last_question_id) if body.last_question_id else None,
        last_response=body.last_response,
    )
    return TutorStepResponse(**result)


@router.post("/ask")
async def ask_question(
    lesson_id: str,
    query: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.application.content.rag_service import RAGService

    rag = RAGService(db)
    result = await rag.answer(query=query, lesson_id=UUID(lesson_id))
    return result
