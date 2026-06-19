from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.content import (
    ContentSource, Lesson, Concept, Skill, ContentChunk, SourceType, SourceOrigin,
)
from app.domain.interfaces.repositories import (
    ContentSourceRepository, LessonRepository, ConceptRepository,
    SkillRepository, ContentChunkRepository,
)
from app.infrastructure.db.models.content import (
    ContentSourceModel, LessonModel, ConceptModel, SkillModel, ContentChunkModel,
)


def _to_str(val) -> str:
    return str(val) if isinstance(val, UUID) else val


def _model_to_source(m: ContentSourceModel) -> ContentSource:
    return ContentSource(
        id=m.id,
        type=SourceType(m.type),
        origin=SourceOrigin(m.origin),
        title=m.title,
        language=m.language,
        description=m.description or "",
        url=m.url,
        file_path=m.file_path,
        created_by=m.created_by,
        created_at=m.created_at,
    )


def _model_to_lesson(m: LessonModel) -> Lesson:
    return Lesson(
        id=m.id,
        title=m.title,
        subject=m.subject,
        grade_level=m.grade_level,
        language=m.language,
        description=m.description or "",
        is_active=m.is_active,
        created_at=m.created_at,
    )


def _model_to_concept(m: ConceptModel) -> Concept:
    return Concept(
        id=m.id,
        lesson_id=m.lesson_id,
        name=m.name,
        description=m.description or "",
        difficulty_level=m.difficulty_level,
    )


def _model_to_skill(m: SkillModel) -> Skill:
    return Skill(
        id=m.id,
        concept_id=m.concept_id,
        name=m.name,
        description=m.description or "",
    )


def _model_to_chunk(m: ContentChunkModel) -> ContentChunk:
    return ContentChunk(
        id=m.id,
        source_id=m.source_id,
        lesson_id=m.lesson_id,
        concept_id=m.concept_id,
        skill_id=m.skill_id,
        content=m.content,
        language=m.language,
        source_type=SourceType(m.source_type),
        start_offset=m.start_offset,
        end_offset=m.end_offset,
        metadata=m.metadata_ or {},
    )


class SQLContentSourceRepository(ContentSourceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, source: ContentSource) -> ContentSource:
        model = ContentSourceModel(
            id=source.id,
            type=source.type.value,
            origin=source.origin.value,
            title=source.title,
            language=source.language,
            description=source.description,
            url=source.url,
            file_path=source.file_path,
            created_by=source.created_by,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_source(model)

    async def get_by_id(self, id: UUID) -> ContentSource | None:
        result = await self.session.execute(
            select(ContentSourceModel).where(ContentSourceModel.id == _to_str(id))
        )
        model = result.scalar_one_or_none()
        return _model_to_source(model) if model else None

    async def list_by_lesson(self, lesson_id: UUID) -> list[ContentSource]:
        result = await self.session.execute(
            select(ContentSourceModel)
            .join(ContentChunkModel, ContentChunkModel.source_id == ContentSourceModel.id)
            .where(ContentChunkModel.lesson_id == _to_str(lesson_id))
            .distinct()
        )
        return [_model_to_source(m) for m in result.scalars().all()]


class SQLLessonRepository(LessonRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, lesson: Lesson) -> Lesson:
        model = LessonModel(
            id=lesson.id,
            title=lesson.title,
            subject=lesson.subject,
            grade_level=lesson.grade_level,
            language=lesson.language,
            description=lesson.description,
            is_active=lesson.is_active,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_lesson(model)

    async def get_by_id(self, id: UUID) -> Lesson | None:
        result = await self.session.execute(
            select(LessonModel).where(LessonModel.id == _to_str(id))
        )
        model = result.scalar_one_or_none()
        return _model_to_lesson(model) if model else None

    async def list_active(self) -> list[Lesson]:
        result = await self.session.execute(
            select(LessonModel).where(LessonModel.is_active == True)
        )
        return [_model_to_lesson(m) for m in result.scalars().all()]


class SQLConceptRepository(ConceptRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, concept: Concept) -> Concept:
        model = ConceptModel(
            id=concept.id,
            lesson_id=concept.lesson_id,
            name=concept.name,
            description=concept.description,
            difficulty_level=concept.difficulty_level,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_concept(model)

    async def get_by_id(self, id: UUID) -> Concept | None:
        result = await self.session.execute(
            select(ConceptModel).where(ConceptModel.id == _to_str(id))
        )
        model = result.scalar_one_or_none()
        return _model_to_concept(model) if model else None

    async def list_by_lesson(self, lesson_id: UUID) -> list[Concept]:
        result = await self.session.execute(
            select(ConceptModel).where(ConceptModel.lesson_id == _to_str(lesson_id))
        )
        return [_model_to_concept(m) for m in result.scalars().all()]


class SQLSkillRepository(SkillRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, skill: Skill) -> Skill:
        model = SkillModel(
            id=skill.id,
            concept_id=skill.concept_id,
            name=skill.name,
            description=skill.description,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_skill(model)

    async def get_by_id(self, id: UUID) -> Skill | None:
        result = await self.session.execute(
            select(SkillModel).where(SkillModel.id == _to_str(id))
        )
        model = result.scalar_one_or_none()
        return _model_to_skill(model) if model else None

    async def list_by_concept(self, concept_id: UUID) -> list[Skill]:
        result = await self.session.execute(
            select(SkillModel).where(SkillModel.concept_id == _to_str(concept_id))
        )
        return [_model_to_skill(m) for m in result.scalars().all()]


class SQLContentChunkRepository(ContentChunkRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, chunk: ContentChunk) -> ContentChunk:
        model = ContentChunkModel(
            id=chunk.id,
            source_id=chunk.source_id,
            lesson_id=chunk.lesson_id,
            concept_id=chunk.concept_id,
            skill_id=chunk.skill_id,
            content=chunk.content,
            embedding=str(chunk.embedding) if chunk.embedding else None,
            language=chunk.language,
            source_type=chunk.source_type.value,
            start_offset=chunk.start_offset,
            end_offset=chunk.end_offset,
            metadata_=chunk.metadata,
        )
        self.session.add(model)
        await self.session.flush()
        return _model_to_chunk(model)

    async def create_many(self, chunks: list[ContentChunk]) -> list[ContentChunk]:
        models = []
        for chunk in chunks:
            model = ContentChunkModel(
                id=chunk.id,
                source_id=chunk.source_id,
                lesson_id=chunk.lesson_id,
                concept_id=chunk.concept_id,
                skill_id=chunk.skill_id,
                content=chunk.content,
                embedding=str(chunk.embedding) if chunk.embedding else None,
                language=chunk.language,
                source_type=chunk.source_type.value,
                start_offset=chunk.start_offset,
                end_offset=chunk.end_offset,
                metadata_=chunk.metadata,
            )
            self.session.add(model)
            models.append(model)
        await self.session.flush()
        return [_model_to_chunk(m) for m in models]

    async def search_similar(
        self,
        embedding: list[float],
        lesson_id: UUID | None = None,
        language: str | None = None,
        k: int = 8,
    ) -> list[tuple[ContentChunk, float]]:
        # pgvector cosine similarity search
        embedding_str = str(embedding)
        query = select(
            ContentChunkModel,
            (1 - ContentChunkModel.embedding.cosine_distance(embedding_str)).label("similarity"),
        )
        if lesson_id:
            query = query.where(ContentChunkModel.lesson_id == _to_str(lesson_id))
        if language:
            query = query.where(ContentChunkModel.language == language)
        query = query.order_by("similarity").limit(k)

        result = await self.session.execute(query)
        rows = result.all()
        return [(_model_to_chunk(row[0]), float(row[1])) for row in rows]

    async def list_by_source(self, source_id: UUID) -> list[ContentChunk]:
        result = await self.session.execute(
            select(ContentChunkModel).where(ContentChunkModel.source_id == _to_str(source_id))
        )
        return [_model_to_chunk(m) for m in result.scalars().all()]

    async def list_by_lesson(self, lesson_id: UUID) -> list[ContentChunk]:
        result = await self.session.execute(
            select(ContentChunkModel).where(ContentChunkModel.lesson_id == _to_str(lesson_id))
        )
        return [_model_to_chunk(m) for m in result.scalars().all()]
