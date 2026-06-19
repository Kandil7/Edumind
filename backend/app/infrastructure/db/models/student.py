import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class StudentModel(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(300), nullable=False)
    email = Column(String(300), unique=True, nullable=False)
    preferred_language = Column(String(10), default="ar")
    level = Column(String(20), default="beginner")
    created_at = Column(DateTime, default=datetime.utcnow)

    skill_states = relationship("StudentSkillStateModel", back_populates="student")


class StudentSkillStateModel(Base):
    __tablename__ = "student_skill_state"

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True)
    p_mastery = Column(Float, default=0.0)
    num_attempts = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    initialized = Column(Boolean, default=False)

    student = relationship("StudentModel", back_populates="skill_states")
