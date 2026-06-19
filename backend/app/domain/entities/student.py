from datetime import datetime
from uuid import UUID


class Student:
    def __init__(
        self,
        id: UUID,
        name: str,
        email: str,
        preferred_language: str = "ar",
        level: str = "beginner",
        created_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.preferred_language = preferred_language
        self.level = level
        self.created_at = created_at or datetime.now()


class StudentSkillState:
    def __init__(
        self,
        student_id: UUID,
        skill_id: UUID,
        p_mastery: float = 0.0,
        num_attempts: int = 0,
        last_updated: datetime | None = None,
        initialized: bool = False,
    ):
        self.student_id = student_id
        self.skill_id = skill_id
        self.p_mastery = p_mastery
        self.num_attempts = num_attempts
        self.last_updated = last_updated or datetime.now()
        self.initialized = initialized


class MasteryScore:
    """Value object representing mastery probability with bounds."""

    def __init__(self, value: float):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Mastery must be between 0 and 1, got {value}")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @property
    def is_mastered(self) -> bool:
        return self._value >= 0.8

    @property
    def needs_remédiation(self) -> bool:
        return self._value < 0.4

    def __repr__(self) -> str:
        return f"MasteryScore({self._value:.3f})"
