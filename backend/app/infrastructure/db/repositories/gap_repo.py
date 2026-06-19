from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.misconception import Misconception, MisconceptionInstance
from app.domain.interfaces.gap_repository import MisconceptionRepository, MisconceptionInstanceRepository
from app.infrastructure.db.models.misconception import MisconceptionModel, MisconceptionInstanceModel


def _model_to_misconception(m: MisconceptionModel) -> Misconception:
    return Misconception(
        id=m.id,
        skill_id=m.skill_id,
        description=m.description,
        centroid_embedding=None,
        metadata=m.metadata_ or {},
    )


def _model_to_instance(m: MisconceptionInstanceModel) -> MisconceptionInstance:
    return MisconceptionInstance(
        id=m.id,
        student_id=m.student_id,
        misconception_id=m.misconception_id,
        first_seen_at=m.first_seen_at,
        last_seen_at=m.last_seen_at,
        num_occurrences=m.num_occurrences,
    )


class SQLMisconceptionRepository(MisconceptionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, misconception: Misconception) -> Misconception:
        model = MisconceptionModel(
            id=misconception.id,
            skill_id=misconception.skill_id,
            description=misconception.description,
            centroid_embedding=str(misconception.centroid_embedding) if misconception.centroid_embedding else None,
            metadata_=misconception.metadata,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_misconception(model)

    async def get_by_id(self, id: UUID) -> Misconception | None:
        result = await self.session.execute(
            select(MisconceptionModel).where(MisconceptionModel.id == id)
        )
        model = result.scalar_one_or_none()
        return _model_to_misconception(model) if model else None

    async def list_by_skill(self, skill_id: UUID) -> list[Misconception]:
        result = await self.session.execute(
            select(MisconceptionModel).where(MisconceptionModel.skill_id == skill_id)
        )
        return [_model_to_misconception(m) for m in result.scalars().all()]

    async def find_similar(
        self, embedding: list[float], skill_id: UUID, threshold: float = 0.8
    ) -> Misconception | None:
        embedding_str = str(embedding)
        query = (
            select(MisconceptionModel)
            .where(
                MisconceptionModel.skill_id == skill_id,
                MisconceptionModel.centroid_embedding.cosine_distance(embedding_str) < (1 - threshold),
            )
            .limit(1)
        )
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return _model_to_misconception(model) if model else None


class SQLMisconceptionInstanceRepository(MisconceptionInstanceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, instance: MisconceptionInstance) -> MisconceptionInstance:
        model = MisconceptionInstanceModel(
            id=instance.id,
            student_id=instance.student_id,
            misconception_id=instance.misconception_id,
            first_seen_at=instance.first_seen_at,
            last_seen_at=instance.last_seen_at,
            num_occurrences=instance.num_occurrences,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_instance(model)

    async def upsert(self, student_id: UUID, misconception_id: UUID) -> MisconceptionInstance:
        result = await self.session.execute(
            select(MisconceptionInstanceModel).where(
                MisconceptionInstanceModel.student_id == student_id,
                MisconceptionInstanceModel.misconception_id == misconception_id,
            )
        )
        model = result.scalar_one_or_none()
        if model:
            model.num_occurrences += 1
        else:
            model = MisconceptionInstanceModel(
                student_id=student_id,
                misconception_id=misconception_id,
                num_occurrences=1,
            )
            self.session.add(model)
        await self.session.flush()
        return _model_to_instance(model)

    async def list_by_student(self, student_id: UUID) -> list[MisconceptionInstance]:
        result = await self.session.execute(
            select(MisconceptionInstanceModel)
            .where(MisconceptionInstanceModel.student_id == student_id)
            .order_by(MisconceptionInstanceModel.num_occurrences.desc())
        )
        return [_model_to_instance(m) for m in result.scalars().all()]
