# Development Setup Guide

## Prerequisites

- Python 3.9+ installed
- PostgreSQL 13+ 
- Redis 6+
- Docker & Docker Compose (for containerized development)
- Git

## Local Development Setup

### 1. Clone & Navigate

```bash
cd daily_ninja_python
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements/dev.txt
```

### 4. Configure Environment

```bash
cp config/.env.example config/.env
```

Edit `config/.env` with your local database and Redis credentials:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/daily_ninja
REDIS_URL=redis://localhost:6379/0
ENV=development
DEBUG=true
```

### 5. Setup Database

```bash
# Run migrations
alembic upgrade head

# (Optional) Seed sample data
python scripts/seed_data.py
```

### 6. Start Services (Terminal 1 - Backend)

```bash
make run-backend
# OR
uvicorn backend.app.main:app --reload
```

Backend will be available at: **http://localhost:8000**

### 7. Start Services (Terminal 2 - Frontend)

```bash
make run-frontend
# OR
streamlit run frontend/app.py
```

Frontend will be available at: **http://localhost:8501**

### 8. Start Services (Terminal 3 - Celery Worker)

```bash
make run-celery
# OR
celery -A workers.celery_app worker --loglevel=info
```

### 9. Start Services (Terminal 4 - Scheduler)

```bash
make run-scheduler
# OR
python -m workers.schedulers.main
```

## Docker Development (Recommended)

Single command to run everything:

```bash
make docker-up
```

This starts:
- PostgreSQL database
- Redis cache
- FastAPI backend
- Streamlit frontend
- Celery worker

View logs:
```bash
make docker-logs
```

Stop services:
```bash
make docker-down
```

## Common Development Tasks

### Run Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests only
make test-integration
```

### Code Quality

```bash
# Check formatting & linting
make lint

# Auto-format code
make format
```

### Database Migrations

```bash
# Create new migration
make migrate-create name=add_new_field

# Apply migrations
make migrate
```

### Install Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Useful Make Commands

```bash
make help                  # List all commands
make install-dev          # Install dev dependencies
make test                 # Run all tests
make lint                 # Check code quality
make format               # Format code
make run-backend          # Start FastAPI
make run-frontend         # Start Streamlit
make docker-build         # Build Docker images
make docker-up            # Start containers
make clean                # Clean cache files
```

## API Documentation

FastAPI provides automatic documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # for backend
lsof -i :8501  # for frontend
lsof -i :6379  # for Redis

# Kill process (get PID from above)
kill -9 PID
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U postgres -d daily_ninja

# Check Redis is running
redis-cli ping
```

### Celery Not Working

```bash
# Check Redis connection
redis-cli ping  # Should return "PONG"

# Check Celery broker URL in .env
echo $CELERY_BROKER_URL
```

### Virtual Environment Issues

```bash
# Deactivate and recreate
deactivate
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
```

## Next Steps

1. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Check [API.md](API.md) for API endpoints
3. Read `README.md` in each module for specific documentation

## Support

For issues or questions:
1. Check existing documentation in `docs/`
2. Review test files for usage examples
3. Check FastAPI/Streamlit documentation
