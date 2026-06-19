from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.misconception import Misconception, MisconceptionInstance
from app.infrastructure.db.repositories import (
    SQLAttemptRepository,
    SQLMisconceptionRepository,
    SQLMisconceptionInstanceRepository,
)


class GapDetectorService:
    """Detects misconceptions by clustering wrong answer patterns."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.attempt_repo = SQLAttemptRepository(db)
        self.misconception_repo = SQLMisconceptionRepository(db)
        self.instance_repo = SQLMisconceptionInstanceRepository(db)

    async def analyze_skill_gaps(self, skill_id: UUID) -> list[dict]:
        wrong_attempts = await self.attempt_repo.get_wrong_attempts_by_skill(skill_id)

        if not wrong_attempts:
            return []

        # Group by response pattern (simplified clustering)
        patterns: dict[str, list] = {}
        for attempt in wrong_attempts:
            key = attempt.response_text[:50].lower().strip()
            if key not in patterns:
                patterns[key] = []
            patterns[key].append(attempt)

        # Create/update misconceptions for each pattern
        misconceptions = []
        for pattern_key, attempts in patterns.items():
            if len(attempts) < 2:
                continue  # Need at least 2 occurrences

            # Check if similar misconception exists
            description = f"خطأ شائع: {pattern_key}"
            existing = await self.misconception_repo.find_similar(
                embedding=None,  # Would use real embedding in production
                skill_id=skill_id,
            )

            if existing:
                misconception = existing
            else:
                misconception = Misconception(
                    id=uuid4(),
                    skill_id=skill_id,
                    description=description,
                )
                misconception = await self.misconception_repo.create(misconception)

            # Track instances per student
            students_seen = set()
            for attempt in attempts:
                if attempt.student_id not in students_seen:
                    await self.instance_repo.upsert(
                        student_id=attempt.student_id,
                        misconception_id=misconception.id,
                    )
                    students_seen.add(attempt.student_id)

            misconceptions.append({
                "misconception_id": str(misconception.id),
                "description": description,
                "occurrences": len(attempts),
                "students_affected": len(students_seen),
            })

        return misconceptions

    async def get_student_gaps(self, student_id: UUID) -> list[dict]:
        instances = await self.instance_repo.list_by_student(student_id)
        results = []
        for inst in instances:
            misconception = await self.misconception_repo.get_by_id(inst.misconception_id)
            if misconception:
                results.append({
                    "misconception_id": str(inst.misconception_id),
                    "description": misconception.description,
                    "num_occurrences": inst.num_occurrences,
                    "first_seen": inst.first_seen_at.isoformat(),
                    "last_seen": inst.last_seen_at.isoformat(),
                })
        return results
