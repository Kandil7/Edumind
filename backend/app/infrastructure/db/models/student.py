import uuid as _uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


def _uuid_col():
    return str(_uuid.uuid4())


class StudentModel(Base):
    __tablename__ = "students"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    name = Column(String(300), nullable=False)
    email = Column(String(300), unique=True, nullable=False)
    preferred_language = Column(String(10), default="ar")
    level = Column(String(20), default="beginner")
    created_at = Column(DateTime, default=datetime.utcnow)

    skill_states = relationship("StudentSkillStateModel", back_populates="student")


class StudentSkillStateModel(Base):
    __tablename__ = "student_skill_state"

    student_id = Column(String(36), ForeignKey("students.id"), primary_key=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), primary_key=True)
    p_mastery = Column(Float, default=0.0)
    num_attempts = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    initialized = Column(Boolean, default=False)

    student = relationship("StudentModel", back_populates="skill_states")
