<div align="center">

# 🎓 EduMind

### Adaptive Multimodal Learning & Assessment Platform

**AI-powered personalized education** — adapts content difficulty to each learner using Bayesian Knowledge Tracing, evaluates understanding through multimodal assessment (text + table + image + speech), and traces every fact back to its source.

[![CI](https://github.com/your-org/edumind/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/edumind/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **🧠 Knowledge Tracing** | Bayesian BKT models per-student mastery across 50+ concepts |
| **📝 Multimodal Assessment** | Cloze, MCQ, Table QA, VQA, and oral questions — auto-generated |
| **🔍 RAG with Provenance** | Every answer links back to its source (page, timecode, paragraph) |
| **🎯 Adaptive Tutoring** | Session state machine: explain → question → evaluate → repeat |
| **🐛 Gap Detection** | Clusters wrong answers to identify systematic misconceptions |
| **🌍 Multilingual + RTL** | Arabic and English UI, content in 10+ languages |
| **👨‍🏫 Teacher Dashboard** | Upload content, view analytics, manage questions |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend                        │
│  Student Session │ Dashboard │ Teacher Panel │ i18n/RTL  │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (JWT)
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

**Clean Architecture** with DDD-inspired layering:
- `domain/` — Entities, repository interfaces, value objects
- `application/` — Use cases and business logic
- `infrastructure/` — Database, external model adapters
- `api/` — Thin FastAPI route handlers

📖 Full details: [docs/architecture.md](docs/architecture.md)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Node.js 18+** (for frontend)
- **Git**

### 1. Clone & Setup

```bash
git clone https://github.com/your-org/edumind.git
cd edumind
cp backend/.env.example backend/.env
```

### 2. Start Infrastructure

```bash
make up
```

This starts:
- **PostgreSQL** (with pgvector + TimescaleDB) on port 5432
- **Redis** on port 6379

### 3. Run Migrations & Seed Data

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python -m scripts.seed_data
cd ..
```

### 4. Start Backend

```bash
make dev
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

### 5. Start Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 6. Try It

1. Open http://localhost:3000
2. Click a lesson from the list
3. Answer questions in the adaptive session
4. View your mastery dashboard
5. Switch language with the 🌐 button (AR ↔ EN)

---

## 📁 Project Structure

```
edumind/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # FastAPI routes (7 modules)
│   │   ├── application/     # Business logic services
│   │   ├── domain/          # Entities & interfaces
│   │   ├── infrastructure/  # DB models & repositories
│   │   ├── core/            # Config, security, middleware
│   │   └── workers/         # Celery background tasks
│   ├── alembic/             # Database migrations
│   ├── scripts/             # Seed data
│   └── tests/               # Unit + integration tests
├── frontend/
│   └── src/
│       ├── pages/           # StudentSession, Dashboard, Teacher
│       ├── components/      # QuestionCard, MasteryHeatmap, etc.
│       ├── api/             # Axios client with JWT auth
│       ├── i18n/            # Arabic + English translations
│       └── types/           # TypeScript interfaces
├── infra/docker/            # Docker Compose, Dockerfile
├── docs/                    # Architecture & design docs
└── .github/workflows/       # CI/CD pipeline
```

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
cd backend && python -m pytest tests/ -v --tb=short

# Run specific test file
cd backend && python -m pytest tests/unit/test_bkt.py -v
```

**Test coverage:**
- `test_bkt.py` — Knowledge tracing update logic
- `test_grading.py` — Answer correctness checking
- `test_rag.py` — Retrieval and provenance
- `test_question_generator.py` — Cloze/MCQ generation
- `test_gap_detector.py` — Misconception clustering
- `test_entities.py` — Domain entity validation
- `test_api.py` — API endpoint integration tests

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login, get JWT token |
| `POST` | `/api/v1/content/sources` | Upload content source |
| `POST` | `/api/v1/content/lessons` | Create lesson |
| `POST` | `/api/v1/content/chunks/index` | Index content (async) |
| `GET`  | `/api/v1/content/lessons` | List all lessons |
| `POST` | `/api/v1/questions/generate-batch` | Generate questions |
| `POST` | `/api/v1/assessments/grade` | Grade answer + update BKT |
| `POST` | `/api/v1/tutor/session/step` | Adaptive tutoring step |
| `POST` | `/api/v1/tutor/ask` | RAG Q&A with sources |
| `GET`  | `/api/v1/students/{id}/profile` | Student mastery profile |
| `POST` | `/api/v1/speech/tts` | Text-to-speech |
| `POST` | `/api/v1/speech/asr` | Speech-to-text |

📖 Full docs: http://localhost:8000/docs (Swagger UI)

---

## 🎯 User Flows

### Student Flow
```
Select Lesson → Adaptive Session → View Mastery Dashboard
                    │
                    ├── EXPLAIN (low mastery)
                    │   └── RAG answer with source citations
                    │
                    └── QUESTION (mastery OK)
                        ├── Cloze / MCQ / Open Text
                        └── Grade → BKT Update → Next Step
```

### Teacher Flow
```
Upload Content → Index into pgvector → Auto-generate Questions
                                              │
View Dashboard ← Aggregate Analytics ← Student Attempts
```

---

## 🛠️ Development

### Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start backend in dev mode (hot reload) |
| `make test` | Run test suite |
| `make lint` | Lint with Ruff |
| `make format` | Format with Ruff |
| `make up` | Start Docker infrastructure |
| `make down` | Stop Docker infrastructure |
| `make migrate-new msg="..."` | Create new Alembic migration |

### Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_HOST` | localhost | Database host |
| `POSTGRES_DB` | edumind | Database name |
| `REDIS_HOST` | localhost | Redis host |
| `JWT_SECRET_KEY` | ... | JWT signing secret |
| `LLM_API_KEY` | (empty) | OpenAI API key (optional) |
| `ENABLE_VQA` | false | Enable visual QA questions |
| `ENABLE_TABLE_QA` | false | Enable table QA questions |
| `ENABLE_ORAL` | false | Enable speech questions |

### Adding a New Feature

1. Create feature branch: `git checkout -b feature/my-feature`
2. Plan in `docs/` (API contracts, data model)
3. Implement: domain → infrastructure → application → API
4. Write tests
5. Commit with clear message
6. Merge to `main`: `git merge --no-ff`

📖 Contributing guide: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI, SQLAlchemy, Celery |
| **Database** | PostgreSQL + pgvector + TimescaleDB |
| **Cache/Queue** | Redis |
| **Frontend** | React, TypeScript, Vite |
| **i18n** | react-i18next (Arabic + English) |
| **Charts** | Recharts |
| **ML Models** | pyBKT, RoBERTa, Whisper (pluggable) |
| **Deployment** | Docker Compose, GitHub Actions CI |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | System overview and design |
| [Backend](docs/backend.md) | Backend layer structure |
| [RAG Design](docs/rag.md) | Retrieval and provenance model |
| [Knowledge Tracing](docs/knowledge_tracing.md) | BKT algorithm and data model |
| [Assessment Engine](docs/assessment_engine.md) | Question types and grading |
| [Frontend](docs/frontend.md) | UI components and routing |
| [Branching Strategy](docs/branching_strategy.md) | Git workflow |
| [Contributing](docs/CONTRIBUTING.md) | How to contribute |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ for personalized education**

</div>
