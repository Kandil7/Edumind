# EduMind

Adaptive Multimodal Learning & Assessment Platform

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for frontend)

### Development

```bash
# Start infrastructure (Postgres + Redis)
make up

# Run backend
make dev

# Run tests
make test

# Lint
make lint
```

### Docker

```bash
make up    # Start all services
make down  # Stop all services
```

## Architecture

See [docs/architecture.md](docs/architecture.md)

## API Docs

Once running, visit: http://localhost:8000/docs
