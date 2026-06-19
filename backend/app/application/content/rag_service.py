import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.repositories import ContentChunkRepository
from app.domain.interfaces.model_services import EmbeddingService, LLMService
from app.domain.entities.content import ContentChunk
from app.infrastructure.db.repositories import SQLContentChunkRepository


class RAGService:
    """Retrieval-Augmented Generation with content provenance."""

    def __init__(
        self,
        db: AsyncSession,
        embedding_service: EmbeddingService | None = None,
        llm_service: LLMService | None = None,
    ):
        self.db = db
        self.chunk_repo = SQLContentChunkRepository(db)
        self.embedding_service = embedding_service
        self.llm_service = llm_service

    async def retrieve(
        self,
        query: str,
        lesson_id: UUID | None = None,
        language: str | None = None,
        k: int = 8,
    ) -> list[ContentChunk]:
        if self.embedding_service:
            query_embedding = await self.embedding_service.embed(query)
        else:
            # Fallback: use a simple hash-based pseudo-embedding for MVP
            query_embedding = self._simple_embed(query)

        chunks, _ = zip(
            *await self.chunk_repo.search_similar(
                embedding=query_embedding,
                lesson_id=lesson_id,
                language=language,
                k=k,
            )
        ) if await self.chunk_repo.search_similar(
            embedding=query_embedding,
            lesson_id=lesson_id,
            language=language,
            k=k,
        ) else ([], [])

        return list(chunks)

    async def answer(
        self,
        query: str,
        lesson_id: UUID | None = None,
        student_language: str = "ar",
    ) -> dict:
        chunks = await self.retrieve(query, lesson_id=lesson_id)

        if not chunks:
            return {
                "answer": "لم أجد معلومات كافية للإجابة على هذا السؤال.",
                "sources": [],
            }

        # Build context with source references
        context_parts = []
        sources = []
        for i, chunk in enumerate(chunks):
            context_parts.append(f"[{i}] {chunk.content}")
            source_info = {
                "source_id": str(chunk.source_id),
                "source_name": chunk.metadata.get("source_name", "Unknown"),
                "source_type": chunk.source_type.value,
                "start_offset": chunk.start_offset,
                "end_offset": chunk.end_offset,
            }
            sources.append(source_info)

        context = "\n\n".join(context_parts)

        system_prompt = """You are an educational assistant. Answer the student's question using ONLY the provided context.
For each fact, cite the source using [#index] notation.
At the end, return a JSON block with sources list.
Format your answer in the student's language."""

        user_prompt = f"""Context:
{context}

Question: {query}

Answer with citations, then provide sources as JSON: {{"sources": [{{"source_id": "...", "source_name": "...", "source_type": "...", "locator": "..."}}]}}"""

        if self.llm_service:
            raw_answer = await self.llm_service.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )
        else:
            # MVP fallback: construct answer from chunks directly
            raw_answer = self._build_simple_answer(query, chunks)

        # Parse sources from answer if present
        parsed_sources = sources[:len(chunks)]

        return {
            "answer": raw_answer,
            "sources": parsed_sources,
        }

    def _simple_embed(self, text: str) -> list[float]:
        """Simple hash-based pseudo-embedding for MVP without embedding service."""
        import hashlib
        h = hashlib.sha256(text.encode()).digest()
        return [b / 255.0 for b in h] + [0.0] * (384 - len(h))  # Pad to 384 dims

    def _build_simple_answer(self, query: str, chunks: list[ContentChunk]) -> str:
        """Build a simple answer from chunks when no LLM is available."""
        parts = []
        for i, chunk in enumerate(chunks[:3]):
            parts.append(f"[#{i}] {chunk.content[:200]}")
        return f"بناءً على المحتوى التعليمي:\n\n" + "\n\n".join(parts)
