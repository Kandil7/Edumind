from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, require_role, UserRole
from app.infrastructure.db.models.content import LessonModel, ConceptModel, SkillModel, ContentChunkModel
from app.infrastructure.db.models.question import QuestionModel, AttemptModel
from app.infrastructure.db.models.student import StudentModel, StudentSkillStateModel
from app.infrastructure.db.models.misconception import MisconceptionModel, MisconceptionInstanceModel

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/{teacher_id}/courses/overview")
async def get_course_overview(
    teacher_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregate analytics: all lessons with student counts and average mastery."""
    lessons_result = await db.execute(select(LessonModel).where(LessonModel.is_active == True))
    lessons = lessons_result.scalars().all()

    overview = []
    for lesson in lessons:
        # Count concepts
        concepts_result = await db.execute(
            select(func.count(ConceptModel.id)).where(ConceptModel.lesson_id == lesson.id)
        )
        concept_count = concepts_result.scalar() or 0

        # Count chunks
        chunks_result = await db.execute(
            select(func.count(ContentChunkModel.id)).where(ContentChunkModel.lesson_id == lesson.id)
        )
        chunk_count = chunks_result.scalar() or 0

        # Count questions
        questions_result = await db.execute(
            select(func.count(QuestionModel.id)).where(QuestionModel.lesson_id == lesson.id)
        )
        question_count = questions_result.scalar() or 0

        # Count students who attempted questions for this lesson
        students_result = await db.execute(
            select(func.count(func.distinct(AttemptModel.student_id)))
            .join(QuestionModel, QuestionModel.id == AttemptModel.question_id)
            .where(QuestionModel.lesson_id == lesson.id)
        )
        student_count = students_result.scalar() or 0

        # Average mastery across skills in this lesson
        avg_mastery_result = await db.execute(
            select(func.avg(StudentSkillStateModel.p_mastery))
            .join(SkillModel, SkillModel.id == StudentSkillStateModel.skill_id)
            .join(ConceptModel, ConceptModel.id == SkillModel.concept_id)
            .where(ConceptModel.lesson_id == lesson.id)
        )
        avg_mastery = avg_mastery_result.scalar()
        avg_mastery_pct = round(float(avg_mastery) * 100, 1) if avg_mastery else 0.0

        overview.append({
            "lesson_id": str(lesson.id),
            "title": lesson.title,
            "subject": lesson.subject,
            "grade_level": lesson.grade_level,
            "concept_count": concept_count,
            "chunk_count": chunk_count,
            "question_count": question_count,
            "student_count": student_count,
            "avg_mastery_pct": avg_mastery_pct,
        })

    return {"lessons": overview}


@router.get("/lessons/{lesson_id}/analytics")
async def get_lesson_analytics(
    lesson_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed analytics for a specific lesson."""
    lesson_result = await db.execute(
        select(LessonModel).where(LessonModel.id == UUID(lesson_id))
    )
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Get concepts with mastery stats
    concepts_result = await db.execute(
        select(ConceptModel).where(ConceptModel.lesson_id == UUID(lesson_id))
    )
    concepts = concepts_result.scalars().all()

    concept_stats = []
    for concept in concepts:
        # Skills for this concept
        skills_result = await db.execute(
            select(SkillModel).where(SkillModel.concept_id == concept.id)
        )
        skills = skills_result.scalars().all()

        skill_stats = []
        for skill in skills:
            # Mastery stats
            mastery_result = await db.execute(
                select(
                    func.avg(StudentSkillStateModel.p_mastery),
                    func.count(StudentSkillStateModel.student_id),
                ).where(StudentSkillStateModel.skill_id == skill.id)
            )
            row = mastery_result.one()
            avg_mastery = float(row[0]) if row[0] else 0.0
            student_count = row[1] or 0

            # Attempt stats
            attempts_result = await db.execute(
                select(
                    func.count(AttemptModel.id),
                    func.count(AttemptModel.id).filter(AttemptModel.correct == True),
                ).where(AttemptModel.skill_id == skill.id)
            )
            att_row = attempts_result.one()
            total_attempts = att_row[0] or 0
            correct_attempts = att_row[1] or 0
            accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0.0

            skill_stats.append({
                "skill_id": str(skill.id),
                "skill_name": skill.name,
                "avg_mastery_pct": round(avg_mastery * 100, 1),
                "student_count": student_count,
                "total_attempts": total_attempts,
                "accuracy_pct": round(accuracy, 1),
            })

        concept_stats.append({
            "concept_id": str(concept.id),
            "concept_name": concept.name,
            "difficulty_level": concept.difficulty_level,
            "skills": skill_stats,
        })

    # Top misconceptions for this lesson
    misconceptions_result = await db.execute(
        select(MisconceptionModel)
        .join(SkillModel, SkillModel.id == MisconceptionModel.skill_id)
        .join(ConceptModel, ConceptModel.id == SkillModel.concept_id)
        .where(ConceptModel.lesson_id == UUID(lesson_id))
        .limit(10)
    )
    misconceptions = misconceptions_result.scalars().all()

    top_misconceptions = [
        {
            "misconception_id": str(m.id),
            "description": m.description,
        }
        for m in misconceptions
    ]

    return {
        "lesson_id": lesson_id,
        "title": lesson.title,
        "concepts": concept_stats,
        "top_misconceptions": top_misconceptions,
    }


@router.get("/skills/{skill_id}/misconceptions")
async def get_skill_misconceptions(
    skill_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get top misconceptions for a specific skill."""
    result = await db.execute(
        select(MisconceptionModel).where(MisconceptionModel.skill_id == UUID(skill_id))
    )
    misconceptions = result.scalars().all()

    results = []
    for m in misconceptions:
        # Count students affected
        instances_result = await db.execute(
            select(
                func.count(func.distinct(MisconceptionInstanceModel.student_id)),
                func.sum(MisconceptionInstanceModel.num_occurrences),
            ).where(MisconceptionInstanceModel.misconception_id == m.id)
        )
        row = instances_result.one()
        students_affected = row[0] or 0
        total_occurrences = row[1] or 0

        results.append({
            "misconception_id": str(m.id),
            "description": m.description,
            "students_affected": students_affected,
            "total_occurrences": total_occurrences,
        })

    return {"skill_id": skill_id, "misconceptions": results}
