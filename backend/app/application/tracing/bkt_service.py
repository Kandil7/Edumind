from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.student import StudentSkillState
from app.infrastructure.db.repositories import SQLStudentSkillStateRepository


class KnowledgeTracingService:
    """Bayesian Knowledge Tracing service using pyBKT principles."""

    # Default BKT parameters (from educational research)
    DEFAULT_P_KNOW = 0.3  # Prior probability of knowing
    DEFAULT_P_LEARN = 0.4  # Probability of learning from practice
    DEFAULT_P_GUESS = 0.2  # Probability of guessing correctly
    DEFAULT_P_SLIP = 0.1   # Probability of slipping (wrong when known)

    def __init__(self, db: AsyncSession):
        self.db = db
        self.state_repo = SQLStudentSkillStateRepository(db)

    async def update_mastery(
        self,
        student_id: UUID,
        skill_id: UUID,
        correct: bool,
    ) -> StudentSkillState:
        state = await self.state_repo.get_or_create(student_id, skill_id)

        if not state.initialized:
            # Initialize with prior
            state.p_mastery = self.DEFAULT_P_KNOW
            state.initialized = True

        # Apply BKT update
        p = state.p_mastery
        p_l = self.DEFAULT_P_LEARN
        p_g = self.DEFAULT_P_GUESS
        p_s = self.DEFAULT_P_SLIP

        if correct:
            # P(known | correct) via Bayes
            p_correct_known = p * (1 - p_s)
            p_correct_unknown = (1 - p) * p_g
            p_correct = p_correct_known + p_correct_unknown
            p_new = p_correct_known / p_correct if p_correct > 0 else p
        else:
            # P(known | incorrect) via Bayes
            p_wrong_known = p * p_s
            p_wrong_unknown = (1 - p) * (1 - p_g)
            p_wrong = p_wrong_known + p_wrong_unknown
            p_new = p_wrong_known / p_wrong if p_wrong > 0 else p

        # Apply learning transition
        p_final = p_new + (1 - p_new) * p_l

        # Clamp to [0, 1]
        p_final = max(0.0, min(1.0, p_final))

        updated = await self.state_repo.update_mastery(
            student_id=student_id,
            skill_id=skill_id,
            p_mastery=p_final,
        )

        return updated

    async def get_profile(self, student_id: UUID) -> list[StudentSkillState]:
        return await self.state_repo.list_by_student(student_id)
