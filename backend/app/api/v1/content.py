from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, require_role, UserRole
from app.domain.entities.content import ContentSource, Lesson, Concept, Skill, SourceType, SourceOrigin
from app.infrastructure.db.repositories import (
    SQLContentSourceRepository,
    SQLLessonRepository,
    SQLConceptRepository,
    SQLSkillRepository,
)
from app.api.schemas.content import (
    ContentSourceCreate, ContentSourceResponse,
    LessonCreate, LessonResponse,
    ConceptCreate, ConceptResponse,
    SkillCreate, SkillResponse,
    IndexRequest, RAGAnswerResponse, SourceLocatorResponse,
)

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/sources", response_model=ContentSourceResponse)
async def create_content_source(
    body: ContentSourceCreate,
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    repo = SQLContentSourceRepository(db)
    source = ContentSource(
        id=uuid4(),
        type=SourceType(body.type),
        origin=SourceOrigin(body.origin),
        title=body.title,
        language=body.language,
        description=body.description,
        url=body.url,
        created_by=user.get("user_id"),
    )
    created = await repo.create(source)
    return ContentSourceResponse(
        id=str(created.id),
        type=created.type.value,
        origin=created.origin.value,
        title=created.title,
        language=created.language,
        description=created.description,
        created_at=created.created_at.isoformat(),
    )


@router.post("/sources/upload", response_model=ContentSourceResponse)
async def upload_content_source(
    file: UploadFile = File(...),
    origin: str = "teacher_upload",
    language: str = "en",
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    import os
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{uuid4()}_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    source_type = "text"
    if file.content_type and "audio" in file.content_type:
        source_type = "audio"
    elif file.content_type and "video" in file.content_type:
        source_type = "video"
    elif file.content_type and "image" in file.content_type:
        source_type = "image"

    repo = SQLContentSourceRepository(db)
    source = ContentSource(
        id=uuid4(),
        type=SourceType(source_type),
        origin=SourceOrigin(origin),
        title=file.filename or "uploaded",
        language=language,
        file_path=file_path,
        created_by=user.get("user_id"),
    )
    created = await repo.create(source)
    return ContentSourceResponse(
        id=str(created.id),
        type=created.type.value,
        origin=created.origin.value,
        title=created.title,
        language=created.language,
        description=created.description,
        created_at=created.created_at.isoformat(),
    )


@router.post("/lessons", response_model=LessonResponse)
async def create_lesson(
    body: LessonCreate,
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    repo = SQLLessonRepository(db)
    lesson = Lesson(
        id=uuid4(),
        title=body.title,
        subject=body.subject,
        grade_level=body.grade_level,
        language=body.language,
        description=body.description,
    )
    created = await repo.create(lesson)
    return LessonResponse(
        id=str(created.id),
        title=created.title,
        subject=created.subject,
        grade_level=created.grade_level,
        language=created.language,
        description=created.description,
        is_active=created.is_active,
        created_at=created.created_at.isoformat(),
    )


@router.get("/lessons", response_model=list[LessonResponse])
async def list_lessons(db: AsyncSession = Depends(get_db)):
    repo = SQLLessonRepository(db)
    lessons = await repo.list_active()
    return [
        LessonResponse(
            id=str(l.id), title=l.title, subject=l.subject,
            grade_level=l.grade_level, language=l.language,
            description=l.description, is_active=l.is_active,
            created_at=l.created_at.isoformat(),
        )
        for l in lessons
    ]


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    repo = SQLLessonRepository(db)
    from uuid import UUID
    lesson = await repo.get_by_id(UUID(lesson_id))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return LessonResponse(
        id=str(lesson.id), title=lesson.title, subject=lesson.subject,
        grade_level=lesson.grade_level, language=lesson.language,
        description=lesson.description, is_active=lesson.is_active,
        created_at=lesson.created_at.isoformat(),
    )


@router.post("/lessons/{lesson_id}/concepts", response_model=ConceptResponse)
async def add_concept(
    lesson_id: str,
    body: ConceptCreate,
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    repo = SQLConceptRepository(db)
    concept = Concept(
        id=uuid4(),
        lesson_id=UUID(lesson_id),
        name=body.name,
        description=body.description,
        difficulty_level=body.difficulty_level,
    )
    created = await repo.create(concept)
    return ConceptResponse(
        id=str(created.id),
        lesson_id=str(created.lesson_id),
        name=created.name,
        description=created.description,
        difficulty_level=created.difficulty_level,
    )


@router.get("/lessons/{lesson_id}/concepts", response_model=list[ConceptResponse])
async def list_concepts(lesson_id: str, db: AsyncSession = Depends(get_db)):
    from uuid import UUID
    repo = SQLConceptRepository(db)
    concepts = await repo.list_by_lesson(UUID(lesson_id))
    return [
        ConceptResponse(
            id=str(c.id), lesson_id=str(c.lesson_id),
            name=c.name, description=c.description,
            difficulty_level=c.difficulty_level,
        )
        for c in concepts
    ]


@router.post("/concepts/{concept_id}/skills", response_model=SkillResponse)
async def add_skill(
    concept_id: str,
    body: SkillCreate,
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    repo = SQLSkillRepository(db)
    skill = Skill(
        id=uuid4(),
        concept_id=UUID(concept_id),
        name=body.name,
        description=body.description,
    )
    created = await repo.create(skill)
    return SkillResponse(
        id=str(created.id),
        concept_id=str(created.concept_id),
        name=created.name,
        description=created.description,
    )


@router.post("/chunks/index")
async def index_content(
    body: IndexRequest,
    user: dict = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    from app.workers.tasks.indexing import index_content_task
    task = index_content_task.delay(body.source_id, body.lesson_id, str(body.concept_ids_map) if body.concept_ids_map else None)
    return {"task_id": task.id, "status": "queued"}
