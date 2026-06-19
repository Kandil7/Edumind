import uuid as _uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON
from app.core.database import Base


def _uuid_col():
    return str(_uuid.uuid4())


class MisconceptionModel(Base):
    __tablename__ = "misconceptions"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    description = Column(Text, nullable=False)
    centroid_embedding = Column(String, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)


class MisconceptionInstanceModel(Base):
    __tablename__ = "misconception_instances"

    id = Column(String(36), primary_key=True, default=_uuid_col)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    misconception_id = Column(String(36), ForeignKey("misconceptions.id"), nullable=False)
    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    num_occurrences = Column(Integer, default=1)
