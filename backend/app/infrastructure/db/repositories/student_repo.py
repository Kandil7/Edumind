from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.student import Student, StudentSkillState
from app.domain.interfaces.repositories import StudentRepository, StudentSkillStateRepository
from app.infrastructure.db.models.student import StudentModel, StudentSkillStateModel


def _to_str(val) -> str:
    """Convert UUID to string, or pass through if already string."""
    return str(val) if isinstance(val, UUID) else val


def _model_to_student(m: StudentModel) -> Student:
    return Student(
        id=m.id,
        name=m.name,
        email=m.email,
        preferred_language=m.preferred_language,
        level=m.level,
        created_at=m.created_at,
    )


def _model_to_skill_state(m: StudentSkillStateModel) -> StudentSkillState:
    return StudentSkillState(
        student_id=m.student_id,
        skill_id=m.skill_id,
        p_mastery=m.p_mastery,
        num_attempts=m.num_attempts,
        last_updated=m.last_updated,
        initialized=m.initialized,
    )


class SQLStudentRepository(StudentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, student: Student) -> Student:
        model = StudentModel(
            id=_to_str(student.id),
            name=student.name,
            email=student.email,
            preferred_language=student.preferred_language,
            level=student.level,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_student(model)

    async def get_by_id(self, id) -> Student | None:
        result = await self.session.execute(
            select(StudentModel).where(StudentModel.id == _to_str(id))
        )
        model = result.scalar_one_or_none()
        return _model_to_student(model) if model else None

    async def get_by_email(self, email: str) -> Student | None:
        result = await self.session.execute(
            select(StudentModel).where(StudentModel.email == email)
        )
        model = result.scalar_one_or_none()
        return _model_to_student(model) if model else None


class SQLStudentSkillStateRepository(StudentSkillStateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, student_id, skill_id) -> StudentSkillState:
        sid = _to_str(student_id)
        skid = _to_str(skill_id)
        result = await self.session.execute(
            select(StudentSkillStateModel).where(
                StudentSkillStateModel.student_id == sid,
                StudentSkillStateModel.skill_id == skid,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            model = StudentSkillStateModel(
                student_id=sid,
                skill_id=skid,
                p_mastery=0.0,
                num_attempts=0,
                initialized=False,
            )
            self.session.add(model)
            await self.session.flush()
        return _model_to_skill_state(model)

    async def update_mastery(self, student_id, skill_id, p_mastery: float) -> StudentSkillState:
        sid = _to_str(student_id)
        skid = _to_str(skill_id)
        result = await self.session.execute(
            select(StudentSkillStateModel).where(
                StudentSkillStateModel.student_id == sid,
                StudentSkillStateModel.skill_id == skid,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            model = StudentSkillStateModel(
                student_id=sid,
                skill_id=skid,
                p_mastery=p_mastery,
                num_attempts=1,
                initialized=True,
            )
            self.session.add(model)
        else:
            model.p_mastery = p_mastery
            model.num_attempts += 1
            model.initialized = True
        await self.session.flush()
        return _model_to_skill_state(model)

    async def list_by_student(self, student_id) -> list[StudentSkillState]:
        result = await self.session.execute(
            select(StudentSkillStateModel).where(
                StudentSkillStateModel.student_id == _to_str(student_id)
            )
        )
        return [_model_to_skill_state(m) for m in result.scalars().all()]
