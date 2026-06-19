import uuid as _uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON,
)
from app.core.database import Base


def _uuid_col():
    return str(_uuid.uuid4())


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    type = Column(String(20), nullable=False)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    stem = Column(Text, nullable=False)
    options = Column(JSON, default=list)
    correct_answer = Column(Text, nullable=False)
    difficulty = Column(Integer, default=1)
    source_chunk_ids = Column(JSON, default=list)
    generator_metadata = Column(JSON, default=dict)


class AttemptModel(Base):
    __tablename__ = "attempts"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    response_text = Column(Text, default="")
    response_audio_path = Column(String(1000), nullable=True)
    modality = Column(String(20), default="text")
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_ = Column("metadata", JSON, default=dict)
