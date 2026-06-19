from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.student import Student, StudentSkillState
from app.domain.interfaces.repositories import StudentRepository, StudentSkillStateRepository
from app.infrastructure.db.models.student import StudentModel, StudentSkillStateModel


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
            id=student.id,
            name=student.name,
            email=student.email,
            preferred_language=student.preferred_language,
            level=student.level,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_student(model)

    async def get_by_id(self, id: UUID) -> Student | None:
        result = await self.session.execute(
            select(StudentModel).where(StudentModel.id == id)
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

    async def get_or_create(self, student_id: UUID, skill_id: UUID) -> StudentSkillState:
        result = await self.session.execute(
            select(StudentSkillStateModel).where(
                StudentSkillStateModel.student_id == student_id,
                StudentSkillStateModel.skill_id == skill_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            model = StudentSkillStateModel(
                student_id=student_id,
                skill_id=skill_id,
                p_mastery=0.0,
                num_attempts=0,
                initialized=False,
            )
            self.session.add(model)
            await self.session.flush()
        return _model_to_skill_state(model)

    async def update_mastery(self, student_id: UUID, skill_id: UUID, p_mastery: float) -> StudentSkillState:
        result = await self.session.execute(
            select(StudentSkillStateModel).where(
                StudentSkillStateModel.student_id == student_id,
                StudentSkillStateModel.skill_id == skill_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            model = StudentSkillStateModel(
                student_id=student_id,
                skill_id=skill_id,
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

    async def list_by_student(self, student_id: UUID) -> list[StudentSkillState]:
        result = await self.session.execute(
            select(StudentSkillStateModel).where(
                StudentSkillStateModel.student_id == student_id
            )
        )
        return [_model_to_skill_state(m) for m in result.scalars().all()]
