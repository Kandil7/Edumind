import re
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.question import Question, QuestionType
from app.domain.entities.content import ContentChunk
from app.infrastructure.db.repositories import SQLContentChunkRepository, SQLQuestionRepository


class QuestionGeneratorService:
    """Generates assessment questions from lesson content."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.chunk_repo = SQLContentChunkRepository(db)
        self.question_repo = SQLQuestionRepository(db)

    async def generate_for_concept(
        self,
        lesson_id: UUID,
        concept_id: UUID,
        num_questions: int = 5,
    ) -> list[Question]:
        chunks = await self.chunk_repo.list_by_lesson(lesson_id)
        concept_chunks = [c for c in chunks if c.concept_id == concept_id]

        if not concept_chunks:
            return []

        questions = []

        # Generate cloze (fill-in-the-blank) questions
        cloze_count = min(num_questions // 2 + 1, len(concept_chunks))
        for chunk in concept_chunks[:cloze_count]:
            cloze = self._generate_cloze(chunk)
            if cloze:
                questions.append(cloze)

        # Generate MCQ questions
        mcq_count = min(num_questions - len(questions), len(concept_chunks))
        for chunk in concept_chunks[:mcq_count]:
            mcq = self._generate_mcq(chunk)
            if mcq:
                questions.append(mcq)

        # Generate open text questions from remaining chunks
        remaining = num_questions - len(questions)
        for chunk in concept_chunks[:remaining]:
            open_q = self._generate_open_text(chunk)
            if open_q:
                questions.append(open_q)

        # Store questions
        if questions:
            await self.question_repo.create_many(questions)

        return questions[:num_questions]

    def _generate_cloze(self, chunk: ContentChunk) -> Question | None:
        """Generate a cloze (fill-in-the-blank) question from text."""
        text = chunk.content
        sentences = [s.strip() for s in re.split(r'[.!?؟]', text) if len(s.strip()) > 20]

        if not sentences:
            return None

        sentence = sentences[0]
        words = sentence.split()
        if len(words) < 4:
            return None

        # Pick a meaningful word to mask (prefer nouns/technical terms)
        mask_idx = len(words) // 2
        masked_word = words[mask_idx]
        words[mask_idx] = "_____"
        stem = " ".join(words)

        return Question(
            id=uuid4(),
            type=QuestionType.CLOZE,
            lesson_id=chunk.lesson_id,
            concept_id=chunk.concept_id,
            skill_id=chunk.skill_id or chunk.concept_id,
            stem=f"أكمل الفراغ: {stem}",
            correct_answer=masked_word,
            difficulty=1,
            options=[],
            source_chunk_ids=[chunk.id],
            generator_metadata={"method": "heuristic_cloze"},
        )

    def _generate_mcq(self, chunk: ContentChunk) -> Question | None:
        """Generate a multiple choice question from text."""
        text = chunk.content
        sentences = [s.strip() for s in re.split(r'[.!?؟]', text) if len(s.strip()) > 20]

        if not sentences:
            return None

        sentence = sentences[0]
        words = sentence.split()
        if len(words) < 4:
            return None

        # Create a question about the content
        key_phrase = " ".join(words[:min(6, len(words))])

        return Question(
            id=uuid4(),
            type=QuestionType.MCQ,
            lesson_id=chunk.lesson_id,
            concept_id=chunk.concept_id,
            skill_id=chunk.skill_id or chunk.concept_id,
            stem=f"ما المقصود بـ '{key_phrase}'؟",
            correct_answer=sentence,
            difficulty=1,
            options=[
                {"id": 0, "text": sentence},
                {"id": 1, "text": "خيار بديل 1"},
                {"id": 2, "text": "خيار بديل 2"},
            ],
            source_chunk_ids=[chunk.id],
            generator_metadata={"method": "heuristic_mcq"},
        )

    def _generate_open_text(self, chunk: ContentChunk) -> Question | None:
        """Generate an open-text question from content."""
        text = chunk.content
        sentences = [s.strip() for s in re.split(r'[.!?؟]', text) if len(s.strip()) > 20]

        if not sentences:
            return None

        return Question(
            id=uuid4(),
            type=QuestionType.OPEN_TEXT,
            lesson_id=chunk.lesson_id,
            concept_id=chunk.concept_id,
            skill_id=chunk.skill_id or chunk.concept_id,
            stem="اشرح المحتوى التالي بإيجاز:",
            correct_answer=sentences[0],
            difficulty=2,
            options=[],
            source_chunk_ids=[chunk.id],
            generator_metadata={"method": "heuristic_open_text"},
        )
