import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    DateTime, ForeignKey, Enum as SAEnum, JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ContentSourceModel(Base):
    __tablename__ = "content_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(20), nullable=False)  # text, audio, video, image, table
    origin = Column(String(30), nullable=False)  # book, slides, youtube, teacher_upload
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    language = Column(String(10), nullable=False, default="en")
    url = Column(String(1000), nullable=True)
    file_path = Column(String(1000), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chunks = relationship("ContentChunkModel", back_populates="source")


class LessonModel(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text, default="")
    difficulty_level = Column(Integer, default=1)

    lesson = relationship("LessonModel", back_populates="concepts")
    skills = relationship("SkillModel", back_populates="concept", cascade="all, delete-orphan")


class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concept_id = Column(UUID(as_uuid=True), ForeignKey("concepts.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text, default="")

    concept = relationship("ConceptModel", back_populates="skills")


class ContentChunkModel(Base):
    __tablename__ = "content_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("content_sources.id"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    concept_id = Column(UUID(as_uuid=True), ForeignKey("concepts.id"), nullable=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=True)
    language = Column(String(10), nullable=False, default="en")
    content = Column(Text, nullable=False)
    embedding = Column(String, nullable=True)  # pgvector VECTOR stored as string for now
    source_type = Column(String(20), nullable=False, default="text")
    start_offset = Column(Float, nullable=True)
    end_offset = Column(Float, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    source = relationship("ContentSourceModel", back_populates="chunks")
    lesson = relationship("LessonModel", back_populates="chunks")
