import enum
from datetime import datetime
from uuid import UUID


class QuestionType(str, enum.Enum):
    CLOZE = "cloze"
    MCQ = "mcq"
    OPEN_TEXT = "open_text"
    VQA = "vqa"
    TABLE_QA = "table_qa"
    ORAL = "oral"


class Modality(str, enum.Enum):
    TEXT = "text"
    ORAL = "oral"
    VISUAL = "visual"
    TABLE = "table"


class Question:
    def __init__(
        self,
        id: UUID,
        type: QuestionType,
        lesson_id: UUID,
        concept_id: UUID,
        skill_id: UUID,
        stem: str,
        correct_answer: str,
        difficulty: int = 1,
        options: list[dict] | None = None,
        source_chunk_ids: list[UUID] | None = None,
        generator_metadata: dict | None = None,
    ):
        self.id = id
        self.type = type
        self.lesson_id = lesson_id
        self.concept_id = concept_id
        self.skill_id = skill_id
        self.stem = stem
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.options = options or []
        self.source_chunk_ids = source_chunk_ids or []
        self.generator_metadata = generator_metadata or {}


class Attempt:
    def __init__(
        self,
        id: UUID,
        student_id: UUID,
        question_id: UUID,
        skill_id: UUID,
        correct: bool,
        response_text: str = "",
        response_audio_path: str | None = None,
        modality: Modality = Modality.TEXT,
        created_at: datetime | None = None,
        metadata: dict | None = None,
    ):
        self.id = id
        self.student_id = student_id
        self.question_id = question_id
        self.skill_id = skill_id
        self.correct = correct
        self.response_text = response_text
        self.response_audio_path = response_audio_path
        self.modality = modality
        self.created_at = created_at or datetime.now()
        self.metadata = metadata or {}
