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

        # Group by normalized response pattern (simplified clustering)
        patterns: dict[str, list] = {}
        for attempt in wrong_attempts:
            normalized = (attempt.response_text or "").lower().strip()[:80]
            if not normalized:
                continue
            if normalized not in patterns:
                patterns[normalized] = []
            patterns[normalized].append(attempt)

        # Get existing misconceptions for this skill to avoid duplicates
        existing_misconceptions = await self.misconception_repo.list_by_skill(skill_id)
        existing_descriptions = {m.description for m in existing_misconceptions}

        misconceptions = []
        for pattern_key, attempts in patterns.items():
            if len(attempts) < 2:
                continue

            # Build a meaningful description from the pattern
            sample_responses = list({a.response_text for a in attempts})[:3]
            description = f"خطأ شائع: الطلاب يجيبون '{pattern_key}' ({len(attempts)} مرات)"

            # Check if we already have a misconception with this pattern
            existing = None
            for m in existing_misconceptions:
                if pattern_key in m.description:
                    existing = m
                    break

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
                "sample_responses": sample_responses,
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

    async def get_skill_misconceptions(self, skill_id: UUID) -> list[dict]:
        """Get top misconceptions for a skill with student counts."""
        misconceptions = await self.misconception_repo.list_by_skill(skill_id)
        results = []
        for m in misconceptions:
            # Count unique students affected by this misconception
            instances = await self.instance_repo.list_by_misconception(m.id)
            unique_students = len({inst.student_id for inst in instances})
            total_occurrences = sum(inst.num_occurrences for inst in instances)
            results.append({
                "misconception_id": str(m.id),
                "description": m.description,
                "skill_id": str(m.skill_id),
                "students_affected": unique_students,
                "total_occurrences": total_occurrences,
            })
        return results
