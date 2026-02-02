# Daily Ninja - Python Fullstack

A habit tracking application with GitHub-style heatmap visualization and social streak comparison.

## Tech Stack

- **Frontend**: Streamlit/Dash + Bootstrap 5 + Plotly
- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Database**: PostgreSQL (Azure Database)
- **Caching**: Redis (Azure Cache)
- **Task Queue**: Celery + Azure Service Bus
- **Scheduling**: APScheduler
- **Deployment**: Docker + Azure (App Service/AKS)
- **CI/CD**: Azure Pipelines

## Project Structure

```
daily_ninja_python/
├── frontend/                 # Streamlit/Dash UI
│   ├── pages/               # Streamlit pages
│   ├── components/          # Reusable UI components
│   ├── utils/               # Helper functions
│   └── assets/              # CSS, images, static files
├── backend/                 # FastAPI backend
│   └── app/
│       ├── api/             # API routes
│       ├── models/          # SQLAlchemy models
│       ├── schemas/         # Pydantic schemas
│       ├── services/        # Business logic
│       ├── middleware/      # Custom middleware
│       ├── utils/           # Utilities
│       └── core/            # Config, security, constants
├── workers/                 # Celery & APScheduler tasks
│   ├── tasks/              # Async tasks
│   └── schedulers/         # Scheduled jobs
├── database/               # Database setup
│   ├── migrations/         # Alembic migrations
│   └── seeds/              # Sample data
├── docker/                 # Docker configurations
├── azure/                  # Azure deployment configs
├── config/                 # Environment configurations
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── scripts/               # Utility scripts
├── docs/                  # Documentation
└── requirements/          # Dependencies
```

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Redis
- Docker (optional)

### Installation

1. **Clone & Setup**
```bash
cd daily_ninja_python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements/dev.txt
```

3. **Configure Environment**
```bash
cp config/.env.example config/.env
# Edit config/.env with your settings
```

4. **Database Setup**
```bash
alembic upgrade head
```

5. **Run Services**
```bash
# Terminal 1: Backend
uvicorn backend.app.main:app --reload

# Terminal 2: Frontend
streamlit run frontend/app.py

# Terminal 3: Celery Worker
celery -A workers.celery_app worker --loglevel=info

# Terminal 4: APScheduler
python -m workers.schedulers.main
```

## Development

### Code Style
- Black for formatting
- Flake8 for linting
- MyPy for type checking

### Testing
```bash
pytest tests/ -v
pytest tests/unit -v        # Unit tests only
pytest tests/integration -v # Integration tests only
```

### Migrations
```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

## Deployment

See [azure/README.md](azure/README.md) for Azure deployment instructions.

## Contributing

1. Create feature branch (`git checkout -b feature/your-feature`)
2. Follow code style guidelines
3. Add tests for new features
4. Submit PR for review

## License

MIT License
