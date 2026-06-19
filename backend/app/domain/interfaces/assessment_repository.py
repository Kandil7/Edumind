from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.question import Question, Attempt, QuestionType


class QuestionRepository(ABC):
    @abstractmethod
    async def create(self, question: Question) -> Question: ...

    @abstractmethod
    async def create_many(self, questions: list[Question]) -> list[Question]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Question | None: ...

    @abstractmethod
    async def list_by_lesson(self, lesson_id: UUID) -> list[Question]: ...

    @abstractmethod
    async def list_by_skill(self, skill_id: UUID) -> list[Question]: ...

    @abstractmethod
    async def find_for_student(
        self,
        skill_id: UUID,
        student_id: UUID,
        difficulty: int | None = None,
        exclude_recent: int = 5,
    ) -> Question | None: ...


class AttemptRepository(ABC):
    @abstractmethod
    async def create(self, attempt: Attempt) -> Attempt: ...

    @abstractmethod
    async def list_by_student(self, student_id: UUID) -> list[Attempt]: ...

    @abstractmethod
    async def list_by_student_skill(self, student_id: UUID, skill_id: UUID) -> list[Attempt]: ...

    @abstractmethod
    async def get_wrong_attempts_by_skill(self, skill_id: UUID) -> list[Attempt]: ...
