"""initial schema

Revision ID: 001_initial
Revises:
Create Date: 2025-01-01
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # content_sources
    op.create_table(
        "content_sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("origin", sa.String(30), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, server_default=""),
        sa.Column("language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("url", sa.String(1000), nullable=True),
        sa.Column("file_path", sa.String(1000), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # lessons
    op.create_table(
        "lessons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("grade_level", sa.String(50), nullable=False),
        sa.Column("language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("description", sa.Text, server_default=""),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # concepts
    op.create_table(
        "concepts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("description", sa.Text, server_default=""),
        sa.Column("difficulty_level", sa.Integer, server_default="1"),
    )

    # skills
    op.create_table(
        "skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("concept_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("concepts.id"), nullable=False),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("description", sa.Text, server_default=""),
    )

    # content_chunks
    op.create_table(
        "content_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("content_sources.id"), nullable=False),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=True),
        sa.Column("concept_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("concepts.id"), nullable=True),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), nullable=True),
        sa.Column("language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("embedding", sa.String, nullable=True),
        sa.Column("source_type", sa.String(20), nullable=False, server_default="text"),
        sa.Column("start_offset", sa.Float, nullable=True),
        sa.Column("end_offset", sa.Float, nullable=True),
        sa.Column("metadata", postgresql.JSON, server_default="{}"),
    )
    op.create_index("ix_chunks_lesson_concept", "content_chunks", ["lesson_id", "concept_id"])

    # students
    op.create_table(
        "students",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("email", sa.String(300), unique=True, nullable=False),
        sa.Column("preferred_language", sa.String(10), server_default="ar"),
        sa.Column("level", sa.String(20), server_default="beginner"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # student_skill_state
    op.create_table(
        "student_skill_state",
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), primary_key=True),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), primary_key=True),
        sa.Column("p_mastery", sa.Float, server_default="0.0"),
        sa.Column("num_attempts", sa.Integer, server_default="0"),
        sa.Column("last_updated", sa.DateTime, server_default=sa.func.now()),
        sa.Column("initialized", sa.Boolean, server_default="false"),
    )

    # questions
    op.create_table(
        "questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("concept_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("concepts.id"), nullable=False),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), nullable=False),
        sa.Column("stem", sa.Text, nullable=False),
        sa.Column("options", postgresql.JSON, server_default="[]"),
        sa.Column("correct_answer", sa.Text, nullable=False),
        sa.Column("difficulty", sa.Integer, server_default="1"),
        sa.Column("source_chunk_ids", postgresql.JSON, server_default="[]"),
        sa.Column("generator_metadata", postgresql.JSON, server_default="{}"),
    )

    # attempts
    op.create_table(
        "attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("questions.id"), nullable=False),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), nullable=False),
        sa.Column("correct", sa.Boolean, nullable=False),
        sa.Column("response_text", sa.Text, server_default=""),
        sa.Column("response_audio_path", sa.String(1000), nullable=True),
        sa.Column("modality", sa.String(20), server_default="text"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("metadata", postgresql.JSON, server_default="{}"),
    )
    op.create_index("ix_attempts_student_time", "attempts", ["student_id", "created_at"])

    # misconceptions
    op.create_table(
        "misconceptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("centroid_embedding", sa.String, nullable=True),
        sa.Column("metadata", postgresql.JSON, server_default="{}"),
    )

    # misconception_instances
    op.create_table(
        "misconception_instances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("misconception_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("misconceptions.id"), nullable=False),
        sa.Column("first_seen_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("last_seen_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("num_occurrences", sa.Integer, server_default="1"),
    )


def downgrade() -> None:
    op.drop_table("misconception_instances")
    op.drop_table("misconceptions")
    op.drop_table("attempts")
    op.drop_table("questions")
    op.drop_table("student_skill_state")
    op.drop_table("students")
    op.drop_index("ix_chunks_lesson_concept", "content_chunks")
    op.drop_table("content_chunks")
    op.drop_table("skills")
    op.drop_table("concepts")
    op.drop_table("lessons")
    op.drop_table("content_sources")
