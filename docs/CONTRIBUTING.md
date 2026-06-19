# Contributing to EduMind

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for frontend)

## Getting Started

```bash
# Clone the repo
git clone <repo-url>
cd edumind

# Start infrastructure
make up

# Run backend in dev mode
make dev

# Run frontend
cd frontend && npm install && npm run dev
```

## Running Tests

```bash
# Backend tests
make test

# Lint
make lint

# Format
make format
```

## Project Structure

See [architecture.md](architecture.md) for the full system design.

## Development Workflow

1. Create a feature branch from `main`
2. Make changes in small, focused commits
3. Write tests for new functionality
4. Run `make test && make lint` before committing
5. Merge to `main` and delete your branch

## Adding a New Feature

1. Plan in `docs/` (API contracts, data model)
2. Implement domain entities and interfaces
3. Add repository implementations
4. Create application service
5. Add API routes and schemas
6. Write tests
7. Document in relevant `docs/*.md`

## Code Style

- Python: Ruff (line length 100)
- TypeScript: ESLint
- Follow Clean Architecture: no business logic in routes
- Use type hints everywhere
- Docstrings for public functions
