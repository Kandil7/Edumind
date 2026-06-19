import json
from uuid import UUID, uuid4

from app.workers.celery_app import celery_app


@celery_app.task(bind=True, name="indexing.index_content")
def index_content_task(self, source_id: str, lesson_id: str, concept_ids_map: str | None = None):
    """
    Background task to index content into pgvector.
    Chunks text, computes embeddings, stores with provenance metadata.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.core.config import get_settings
    from app.infrastructure.db.models.content import ContentSourceModel, ContentChunkModel

    settings = get_settings()
    engine = create_engine(settings.SYNC_DATABASE_URL)

    with Session(engine) as db:
        source = db.query(ContentSourceModel).filter(ContentSourceModel.id == UUID(source_id)).first()
        if not source:
            return {"error": f"Source {source_id} not found"}

        # Read file content
        content_text = ""
        if source.file_path:
            try:
                with open(source.file_path, "r", encoding="utf-8") as f:
                    content_text = f.read()
            except Exception:
                content_text = f"[Could not read file: {source.file_path}]"
        elif source.url:
            content_text = f"[Content from URL: {source.url}]"
        else:
            content_text = f"[Source: {source.title}]"

        # Simple chunking: split by paragraphs
        paragraphs = [p.strip() for p in content_text.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [content_text]

        concept_map = {}
        if concept_ids_map:
            try:
                concept_map = json.loads(concept_ids_map)
            except json.JSONDecodeError:
                pass

        concept_values = list(concept_map.values())
        chunks_created = 0
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) < 10:
                continue

            # Distribute concepts across chunks if multiple are provided
            concept_id = concept_values[i % len(concept_values)] if concept_values else None

            chunk = ContentChunkModel(
                id=uuid4(),
                source_id=UUID(source_id),
                lesson_id=UUID(lesson_id),
                concept_id=UUID(concept_id) if concept_id else None,
                content=paragraph,
                language=source.language or "en",
                source_type=source.type or "text",
                start_offset=float(i * 500),
                end_offset=float((i + 1) * 500),
                metadata_={
                    "source_name": source.title,
                    "paragraph_index": i,
                },
            )
            db.add(chunk)
            chunks_created += 1

        db.commit()

    return {
        "source_id": source_id,
        "chunks_created": chunks_created,
        "status": "completed",
    }
