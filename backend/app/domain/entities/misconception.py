from datetime import datetime
from uuid import UUID


class Misconception:
    def __init__(
        self,
        id: UUID,
        skill_id: UUID,
        description: str,
        centroid_embedding: list[float] | None = None,
        metadata: dict | None = None,
    ):
        self.id = id
        self.skill_id = skill_id
        self.description = description
        self.centroid_embedding = centroid_embedding
        self.metadata = metadata or {}


class MisconceptionInstance:
    def __init__(
        self,
        id: UUID,
        student_id: UUID,
        misconception_id: UUID,
        first_seen_at: datetime | None = None,
        last_seen_at: datetime | None = None,
        num_occurrences: int = 1,
    ):
        self.id = id
        self.student_id = student_id
        self.misconception_id = misconception_id
        self.first_seen_at = first_seen_at or datetime.now()
        self.last_seen_at = last_seen_at or datetime.now()
        self.num_occurrences = num_occurrences
