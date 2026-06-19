import enum
from datetime import datetime
from uuid import UUID


class SourceType(str, enum.Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    TABLE = "table"


class SourceOrigin(str, enum.Enum):
    BOOK = "book"
    SLIDES = "slides"
    YOUTUBE = "youtube"
    TEACHER_UPLOAD = "teacher_upload"
    OTHER = "other"


class ContentSource:
    def __init__(
        self,
        id: UUID,
        type: SourceType,
        origin: SourceOrigin,
        title: str,
        language: str,
        description: str = "",
        url: str | None = None,
        file_path: str | None = None,
        created_by: UUID | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.type = type
        self.origin = origin
        self.title = title
        self.language = language
        self.description = description
        self.url = url
        self.file_path = file_path
        self.created_by = created_by
        self.created_at = created_at or datetime.now()


class Lesson:
    def __init__(
        self,
        id: UUID,
        title: str,
        subject: str,
        grade_level: str,
        language: str,
        description: str = "",
        is_active: bool = True,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.title = title
        self.subject = subject
        self.grade_level = grade_level
        self.language = language
        self.description = description
        self.is_active = is_active
        self.created_at = created_at or datetime.now()


class Concept:
    def __init__(
        self,
        id: UUID,
        lesson_id: UUID,
        name: str,
        description: str = "",
        difficulty_level: int = 1,
    ):
        self.id = id
        self.lesson_id = lesson_id
        self.name = name
        self.description = description
        self.difficulty_level = difficulty_level


class Skill:
    def __init__(
        self,
        id: UUID,
        concept_id: UUID,
        name: str,
        description: str = "",
    ):
        self.id = id
        self.concept_id = concept_id
        self.name = name
        self.description = description


class ContentChunk:
    def __init__(
        self,
        id: UUID,
        source_id: UUID,
        lesson_id: UUID,
        concept_id: UUID,
        content: str,
        embedding: list[float] | None = None,
        skill_id: UUID | None = None,
        language: str = "en",
        source_type: SourceType = SourceType.TEXT,
        start_offset: float | None = None,
        end_offset: float | None = None,
        metadata: dict | None = None,
    ):
        self.id = id
        self.source_id = source_id
        self.lesson_id = lesson_id
        self.concept_id = concept_id
        self.skill_id = skill_id
        self.content = content
        self.embedding = embedding
        self.language = language
        self.source_type = source_type
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.metadata = metadata or {}


class SourceLocator:
    """Provenance reference attached to RAG answers and questions."""

    def __init__(
        self,
        source_id: UUID,
        source_name: str,
        source_type: SourceType,
        start_offset: float | None = None,
        end_offset: float | None = None,
    ):
        self.source_id = source_id
        self.source_name = source_name
        self.source_type = source_type
        self.start_offset = start_offset
        self.end_offset = end_offset

    def to_dict(self) -> dict:
        return {
            "source_id": str(self.source_id),
            "source_name": self.source_name,
            "source_type": self.source_type.value,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
        }
