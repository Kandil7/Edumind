# Branching Strategy

## Trunk-Based Development

EduMind uses trunk-based development with short-lived feature branches.

### Branch Types

| Branch | Purpose | Lifetime |
|--------|---------|----------|
| `main` | Always stable, deployable | Permanent |
| `feature/*` | Single feature implementation | Days |

### Branch Names

```
feature/backend-core       # Core infrastructure
feature/rag-content        # RAG + content ingestion
feature/assessment-engine  # Question generation + grading
feature/tracing-tutor      # BKT + adaptive tutoring
feature/frontend-student   # Student UI
feature/frontend-teacher   # Teacher UI
feature/multimodal-speech  # ASR/TTS + i18n
feature/deployment         # Docker + CI
```

### Workflow

1. Create feature branch from `main`
2. Implement in small, incremental steps
3. Commit after each logical unit with clear message
4. Run `make test && make lint`
5. Merge to `main` with `--no-ff`
6. Delete feature branch

### Commit Message Format

```
<type>: <description>

Types: feat, fix, chore, docs, test, refactor
```

Examples:
- `feat: add content_sources and lessons models`
- `feat: implement pgvector-based content retrieval`
- `feat: add cloze question generation and grading`
- `docs: document RAG design and provenance model`
