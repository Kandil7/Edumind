from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.infrastructure.db.repositories import SQLStudentRepository
from app.api.schemas.tracing import StudentProfileResponse, MasteryEntry

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/{student_id}/profile", response_model=StudentProfileResponse)
async def get_student_profile(
    student_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    from app.infrastructure.db.models.student import StudentModel, StudentSkillStateModel
    from app.infrastructure.db.models.content import SkillModel, ConceptModel

    # Query student by string ID
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Query mastery entries
    result = await db.execute(
        select(
            StudentSkillStateModel,
            SkillModel.name.label("skill_name"),
            ConceptModel.name.label("concept_name"),
        )
        .join(SkillModel, SkillModel.id == StudentSkillStateModel.skill_id)
        .join(ConceptModel, ConceptModel.id == SkillModel.concept_id)
        .where(StudentSkillStateModel.student_id == student_id)
    )
    rows = result.all()

    return StudentProfileResponse(
        student_id=student_id,
        mastery=[
            MasteryEntry(
                skill_id=str(row[0].skill_id),
                skill_name=row.skill_name,
                concept_name=row.concept_name,
                p_mastery=row[0].p_mastery,
                num_attempts=row[0].num_attempts,
            )
            for row in rows
        ],
    )


@router.get("/{student_id}/summary")
async def get_student_summary(
    student_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select, func
    from app.infrastructure.db.models.question import AttemptModel

    result = await db.execute(
        select(func.count(AttemptModel.id))
        .where(AttemptModel.student_id == student_id)
    )
    total_attempts = result.scalar() or 0

    result = await db.execute(
        select(func.count(AttemptModel.id))
        .where(AttemptModel.student_id == student_id, AttemptModel.correct == True)
    )
    correct_attempts = result.scalar() or 0

    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0.0

    return {
        "student_id": student_id,
        "total_attempts": total_attempts,
        "correct_attempts": correct_attempts,
        "accuracy_pct": round(accuracy, 2),
    }


@router.get("/{student_id}/gaps")
async def get_student_gaps(
    student_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.application.gap_detector.gap_service import GapDetectorService

    gap_service = GapDetectorService(db)
    gaps = await gap_service.get_student_gaps(student_id)
    return {"student_id": student_id, "gaps": gaps}
