# EduMind Architecture

## System Overview

EduMind is an **Adaptive Multimodal Learning & Assessment Platform** that provides personalized education through knowledge tracing, multimodal assessment, and RAG-based content retrieval with provenance tracking.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (React)                    │
│  Student Session │ Dashboard │ Teacher Panel │ i18n/RTL  │
└────────────────────────┬────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Content  │  │ Assess-  │  │ Tracing  │  │ Tutor  │  │
│  │ Service  │  │  ment    │  │ Service  │  │ Agent  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│  ┌──────────┐  ┌──────────┐                             │
│  │   Gap    │  │  Speech  │                             │
│  │ Detector │  │ Service  │                             │
│  └──────────┘  └──────────┘                             │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│              Infrastructure Layer                        │
│  PostgreSQL + pgvector │ Redis │ Celery Workers          │
└─────────────────────────────────────────────────────────┘
```

## Clean Architecture Layers

### Domain Layer (`app/domain/`)
- **Entities**: ContentSource, Lesson, Concept, Skill, ContentChunk, Student, Question, Attempt, Misconception
- **Interfaces**: Repository ports, Model service ports (Embedding, LLM, Speech)
- **Value Objects**: MasteryScore, SourceLocator, QuestionType

### Application Layer (`app/application/`)
- **Content**: RAGService (retrieval + answer generation with provenance)
- **Assessment**: QuestionGeneratorService, GradingService
- **Tracing**: KnowledgeTracingService (pyBKT wrapper)
- **Tutor**: TutorOrchestrator (adaptive session state machine)
- **Gap Detector**: GapDetectorService (misconception clustering)
- **Speech**: SpeechServiceImpl (ASR/TTS stubs)

### Infrastructure Layer (`app/infrastructure/`)
- **DB Models**: SQLAlchemy ORM models for all tables
- **Repositories**: SQL implementations of domain interfaces
- **Model Adapters**: Pluggable adapters for ML models

### API Layer (`app/api/`)
- **Routes**: Thin FastAPI routers delegating to application services
- **Schemas**: Pydantic request/response models

## Data Flow

### Learning Session Flow
1. Student selects a lesson
2. Tutor Orchestrator checks student's mastery profile
3. If mastery < threshold → RAG generates explanation with source citations
4. If mastery >= threshold → Assessment Engine generates question
5. Student answers → Grading Service evaluates
6. BKT updates mastery probability
7. Gap Detector collects wrong answers for clustering
8. Loop continues until session complete

### Content Ingestion Flow
1. Teacher uploads content (PDF/Slides/Audio/Video)
2. Content Source created in DB
3. Celery worker chunks content (text/audio/video)
4. Embeddings computed and stored in pgvector
5. Chunks linked to lessons, concepts, skills with provenance metadata

## Key Design Decisions

1. **Provenance-first**: Every question and answer traces back to source chunks
2. **Pluggable Models**: ML models behind adapter interfaces for easy swapping
3. **Feature Flags**: `ENABLE_VQA`, `ENABLE_TABLE_QA`, `ENABLE_ORAL` for incremental rollout
4. **Async-first**: All DB operations use async SQLAlchemy
