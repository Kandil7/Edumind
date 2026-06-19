from pydantic import BaseModel


class QuestionCreate(BaseModel):
    lesson_id: str
    concept_ids: list[str]
    num_questions_per_concept: int = 5


class QuestionResponse(BaseModel):
    id: str
    type: str
    lesson_id: str
    concept_id: str
    skill_id: str
    stem: str
    options: list[dict]
    difficulty: int
    source_chunk_ids: list[str]


class GradeRequest(BaseModel):
    student_id: str
    question_id: str
    response_text: str = ""
    response_audio_path: str | None = None


class GradeResponse(BaseModel):
    attempt_id: str
    correct: bool
    question_id: str
    skill_id: str
    p_mastery_new: float | None = None
