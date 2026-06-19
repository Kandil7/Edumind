import uuid as _uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    DateTime, ForeignKey, JSON,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


def _uuid_col():
    return str(_uuid.uuid4())


class ContentSourceModel(Base):
    __tablename__ = "content_sources"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    type = Column(String(20), nullable=False)
    origin = Column(String(30), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    language = Column(String(10), nullable=False, default="en")
    url = Column(String(1000), nullable=True)
    file_path = Column(String(1000), nullable=True)
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chunks = relationship("ContentChunkModel", back_populates="source")


class LessonModel(Base):
    __tablename__ = "lessons"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    title = Column(String(500), nullable=False)
    subject = Column(String(200), nullable=False)
    grade_level = Column(String(50), nullable=False)
    language = Column(String(10), nullable=False, default="en")
    description = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    concepts = relationship("ConceptModel", back_populates="lesson", cascade="all, delete-orphan")
    chunks = relationship("ContentChunkModel", back_populates="lesson")


class ConceptModel(Base):
    __tablename__ = "concepts"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text, default="")
    difficulty_level = Column(Integer, default=1)

    lesson = relationship("LessonModel", back_populates="concepts")
    skills = relationship("SkillModel", back_populates="concept", cascade="all, delete-orphan")


class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text, default="")

    concept = relationship("ConceptModel", back_populates="skills")


class ContentChunkModel(Base):
    __tablename__ = "content_chunks"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    source_id = Column(String(36), ForeignKey("content_sources.id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=True)
    language = Column(String(10), nullable=False, default="en")
    content = Column(Text, nullable=False)
    embedding = Column(String, nullable=True)
    source_type = Column(String(20), nullable=False, default="text")
    start_offset = Column(Float, nullable=True)
    end_offset = Column(Float, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    source = relationship("ContentSourceModel", back_populates="chunks")
    lesson = relationship("LessonModel", back_populates="chunks")
