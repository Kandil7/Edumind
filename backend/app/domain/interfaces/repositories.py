from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.content import (
    ContentSource,
    Lesson,
    Concept,
    Skill,
    ContentChunk,
)
from app.domain.entities.student import Student, StudentSkillState


class ContentSourceRepository(ABC):
    @abstractmethod
    async def create(self, source: ContentSource) -> ContentSource: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> ContentSource | None: ...

    @abstractmethod
    async def list_by_lesson(self, lesson_id: UUID) -> list[ContentSource]: ...


class LessonRepository(ABC):
    @abstractmethod
    async def create(self, lesson: Lesson) -> Lesson: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Lesson | None: ...

    @abstractmethod
    async def list_active(self) -> list[Lesson]: ...


class ConceptRepository(ABC):
    @abstractmethod
    async def create(self, concept: Concept) -> Concept: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Concept | None: ...

    @abstractmethod
    async def list_by_lesson(self, lesson_id: UUID) -> list[Concept]: ...


class SkillRepository(ABC):
    @abstractmethod
    async def create(self, skill: Skill) -> Skill: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Skill | None: ...

    @abstractmethod
    async def list_by_concept(self, concept_id: UUID) -> list[Skill]: ...


class ContentChunkRepository(ABC):
    @abstractmethod
    async def create(self, chunk: ContentChunk) -> ContentChunk: ...

    @abstractmethod
    async def create_many(self, chunks: list[ContentChunk]) -> list[ContentChunk]: ...

    @abstractmethod
    async def search_similar(
        self,
        embedding: list[float],
        lesson_id: UUID | None = None,
        language: str | None = None,
        k: int = 8,
    ) -> list[tuple[ContentChunk, float]]: ...

    @abstractmethod
    async def list_by_source(self, source_id: UUID) -> list[ContentChunk]: ...

    @abstractmethod
    async def list_by_lesson(self, lesson_id: UUID) -> list[ContentChunk]: ...


class StudentRepository(ABC):
    @abstractmethod
    async def create(self, student: Student) -> Student: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Student | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Student | None: ...


class StudentSkillStateRepository(ABC):
    @abstractmethod
    async def get_or_create(self, student_id: UUID, skill_id: UUID) -> StudentSkillState: ...

    @abstractmethod
    async def update_mastery(self, student_id: UUID, skill_id: UUID, p_mastery: float) -> StudentSkillState: ...

    @abstractmethod
    async def list_by_student(self, student_id: UUID) -> list[StudentSkillState]: ...
