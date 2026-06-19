# Backend Architecture

## Structure

```
backend/app/
├── api/                    # FastAPI routers (thin controllers)
│   ├── v1/
│   │   ├── content.py      # Content CRUD + indexing
│   │   ├── questions.py    # Question generation + retrieval
│   │   ├── students.py     # Student profiles + summaries
│   │   ├── tracing.py      # BKT update + grading
│   │   ├── tutor.py        # Adaptive session + RAG QA
│   │   ├── speech.py       # TTS/ASR endpoints
│   │   └── auth.py         # JWT authentication
│   └── schemas/            # Pydantic request/response models
├── domain/                 # Business entities and interfaces
│   ├── entities/           # Domain models
│   ├── interfaces/         # Repository + service ports
│   └── value_objects/      # Immutable value types
├── application/            # Use cases / business logic
│   ├── content/            # RAGService
│   ├── assessment/         # QuestionGenerator, GradingService
│   ├── tracing/            # KnowledgeTracingService (BKT)
│   ├── tutor/              # TutorOrchestrator
│   ├── gap_detector/       # GapDetectorService
│   └── speech/             # SpeechServiceImpl
├── infrastructure/         # External implementations
│   └── db/
│       ├── models/         # SQLAlchemy ORM models
│       └── repositories/   # SQL repository implementations
├── core/                   # Cross-cutting concerns
│   ├── config.py           # Settings (pydantic-settings)
│   ├── database.py         # Async engine + session factory
│   ├── security.py         # JWT auth + password hashing
│   └── logging.py          # Structured logging
└── workers/                # Celery background tasks
    ├── celery_app.py
    └── tasks/
        ├── indexing.py     # Content chunking + embedding
        └── gap_analysis.py # Misconception clustering
```

## Dependency Injection

Routes depend on services via FastAPI's `Depends()`:
```python
@router.post("/tutor/session/step")
async def step(
    body: TutorStepRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    orchestrator = TutorOrchestrator(db)
    return await orchestrator.step(...)
```

## Error Handling

- Domain errors raised as exceptions
- Routes catch and map to HTTP status codes
- Structured logging with request IDs
