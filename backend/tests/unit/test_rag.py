"""Tests for RAG service."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.application.content.rag_service import RAGService
from app.domain.entities.content import ContentChunk, SourceType


class TestRAGService:
    """Test RAG retrieval and answer generation."""

    def setup_method(self):
        self.rag = RAGService.__new__(RAGService)
        self.rag.chunk_repo = AsyncMock()
        self.rag.embedding_service = None
        self.rag.llm_service = None

    def test_simple_embed_deterministic(self):
        """Same input should produce same embedding."""
        emb1 = self.rag._simple_embed("hello world")
        emb2 = self.rag._simple_embed("hello world")
        assert emb1 == emb2

    def test_simple_embed_different_inputs(self):
        """Different inputs should produce different embeddings."""
        emb1 = self.rag._simple_embed("hello")
        emb2 = self.rag._simple_embed("world")
        assert emb1 != emb2

    def test_simple_embed_dimension(self):
        """Embedding should be 384-dimensional."""
        emb = self.rag._simple_embed("test")
        assert len(emb) == 384

    def test_build_simple_answer(self):
        """Answer should reference source chunks."""
        chunks = [
            ContentChunk(
                id=uuid4(),
                source_id=uuid4(),
                lesson_id=uuid4(),
                concept_id=uuid4(),
                content="The derivative of x² is 2x",
                source_type=SourceType.TEXT,
            ),
            ContentChunk(
                id=uuid4(),
                source_id=uuid4(),
                lesson_id=uuid4(),
                concept_id=uuid4(),
                content="This is a key rule in calculus",
                source_type=SourceType.TEXT,
            ),
        ]
        answer = self.rag._build_simple_answer("What is the derivative?", chunks)
        assert "[#0]" in answer
        assert "[#1]" in answer
        assert "derivative" in answer.lower() or "x²" in answer

    @pytest.mark.asyncio
    async def test_answer_with_no_chunks_returns_message(self):
        """When no chunks found, should return a helpful message."""
        self.rag.chunk_repo.search_similar = AsyncMock(return_value=[])

        result = await self.rag.answer("test query", lesson_id=uuid4())

        assert "answer" in result
        assert "sources" in result
        assert len(result["sources"]) == 0

    @pytest.mark.asyncio
    async def test_answer_with_chunks_returns_sources(self):
        """When chunks found, should return sources list."""
        chunk = ContentChunk(
            id=uuid4(),
            source_id=uuid4(),
            lesson_id=uuid4(),
            concept_id=uuid4(),
            content="Test content about derivatives",
            source_type=SourceType.TEXT,
            metadata={"source_name": "Calculus Book"},
        )
        self.rag.chunk_repo.search_similar = AsyncMock(
            return_value=[(chunk, 0.9)]
        )

        result = await self.rag.answer("What is a derivative?", lesson_id=uuid4())

        assert len(result["sources"]) == 1
        assert result["sources"][0]["source_name"] == "Calculus Book"
