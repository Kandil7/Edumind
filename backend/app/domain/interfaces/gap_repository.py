from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.misconception import Misconception, MisconceptionInstance


class MisconceptionRepository(ABC):
    @abstractmethod
    async def create(self, misconception: Misconception) -> Misconception: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Misconception | None: ...

    @abstractmethod
    async def list_by_skill(self, skill_id: UUID) -> list[Misconception]: ...

    @abstractmethod
    async def find_similar(
        self, embedding: list[float], skill_id: UUID, threshold: float = 0.8
    ) -> Misconception | None: ...


class MisconceptionInstanceRepository(ABC):
    @abstractmethod
    async def create(self, instance: MisconceptionInstance) -> MisconceptionInstance: ...

    @abstractmethod
    async def upsert(self, student_id: UUID, misconception_id: UUID) -> MisconceptionInstance: ...

    @abstractmethod
    async def list_by_student(self, student_id: UUID) -> list[MisconceptionInstance]: ...

    @abstractmethod
    async def list_by_misconception(self, misconception_id: UUID) -> list[MisconceptionInstance]: ...
