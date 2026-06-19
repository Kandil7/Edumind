import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class MisconceptionModel(Base):
    __tablename__ = "misconceptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    description = Column(Text, nullable=False)
    centroid_embedding = Column(String, nullable=True)  # VECTOR stored as string
    metadata_ = Column("metadata", JSON, default=dict)


class MisconceptionInstanceModel(Base):
    __tablename__ = "misconception_instances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    misconception_id = Column(UUID(as_uuid=True), ForeignKey("misconceptions.id"), nullable=False)
    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    num_occurrences = Column(Integer, default=1)
