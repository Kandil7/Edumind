from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.api.schemas.tracing import (
    TracingUpdateRequest, TracingUpdateResponse,
    TutorStepRequest, TutorStepResponse,
)
from app.api.schemas.question import GradeRequest

router = APIRouter(prefix="/tracing", tags=["tracing"])


@router.post("/update", response_model=TracingUpdateResponse)
async def update_tracing(
    body: TracingUpdateRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.application.tracing.bkt_service import KnowledgeTracingService

    service = KnowledgeTracingService(db)
    result = await service.update_mastery(
        student_id=UUID(body.student_id),
        skill_id=UUID(body.skill_id),
        correct=body.correct,
    )
    return TracingUpdateResponse(
        student_id=body.student_id,
        skill_id=body.skill_id,
        p_mastery_new=result.p_mastery,
        num_attempts=result.num_attempts,
    )


@router.post("/assessments/grade")
async def grade_answer(
    body: "GradeRequest",
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.application.assessment.grading_service import GradingService

    grading = GradingService(db)
    result = await grading.grade_answer(
        student_id=UUID(body.student_id),
        question_id=UUID(body.question_id),
        response_text=body.response_text,
    )
    return {
        "attempt_id": str(result["attempt_id"]),
        "correct": result["correct"],
        "question_id": body.question_id,
        "skill_id": str(result["skill_id"]),
        "p_mastery_new": result.get("p_mastery_new"),
    }
