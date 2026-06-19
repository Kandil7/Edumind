from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"
    preferred_language: str = "ar"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str


class ContentSourceCreate(BaseModel):
    type: str  # text, audio, video, image, table
    origin: str  # book, slides, youtube, teacher_upload
    title: str
    language: str = "en"
    description: str = ""
    url: str | None = None


class ContentSourceResponse(BaseModel):
    id: str
    type: str
    origin: str
    title: str
    language: str
    description: str
    created_at: str


class LessonCreate(BaseModel):
    title: str
    subject: str
    grade_level: str
    language: str = "en"
    description: str = ""


class LessonResponse(BaseModel):
    id: str
    title: str
    subject: str
    grade_level: str
    language: str
    description: str
    is_active: bool
    created_at: str


class ConceptCreate(BaseModel):
    name: str
    description: str = ""
    difficulty_level: int = 1


class ConceptResponse(BaseModel):
    id: str
    lesson_id: str
    name: str
    description: str
    difficulty_level: int


class SkillCreate(BaseModel):
    name: str
    description: str = ""


class SkillResponse(BaseModel):
    id: str
    concept_id: str
    name: str
    description: str


class IndexRequest(BaseModel):
    source_id: str
    lesson_id: str | None = None
    concept_ids_map: dict[str, str] | None = None


class SourceLocatorResponse(BaseModel):
    source_id: str
    source_name: str
    source_type: str
    start_offset: float | None = None
    end_offset: float | None = None


class RAGAnswerResponse(BaseModel):
    answer: str
    sources: list[SourceLocatorResponse]
