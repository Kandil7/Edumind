from pydantic import BaseModel


class TracingUpdateRequest(BaseModel):
    student_id: str
    skill_id: str
    correct: bool


class TracingUpdateResponse(BaseModel):
    student_id: str
    skill_id: str
    p_mastery_new: float
    num_attempts: int


class MasteryEntry(BaseModel):
    skill_id: str
    skill_name: str
    concept_name: str
    p_mastery: float
    num_attempts: int


class StudentProfileResponse(BaseModel):
    student_id: str
    mastery: list[MasteryEntry]


class TutorStepRequest(BaseModel):
    student_id: str
    lesson_id: str
    last_question_id: str | None = None
    last_response: str | None = None


class TutorStepResponse(BaseModel):
    action: str  # EXPLAIN, QUESTION, FINISHED
    skill_id: str | None = None
    explanation: str | None = None
    sources: list[dict] | None = None
    question: dict | None = None
