# Directory Structure Overview

```
daily_ninja_python/                          # Root project directory
├── README.md                                 # Project overview & getting started
├── .gitignore                               # Git ignore rules
├── .env.example                             # Environment variables template
├── .pre-commit-config.yaml                  # Pre-commit hooks configuration
├── Makefile                                 # Development shortcuts
├── pyproject.toml                           # Python project configuration
│
├── frontend/                                # Streamlit Frontend
│   ├── app.py                              # Main Streamlit entry point
│   ├── pages/                              # Multi-page app
│   │   ├── 01_dashboard.py                # Main heatmap page
│   │   ├── 02_leaderboard.py              # Global streaks
│   │   └── 03_profile.py                  # User profile
│   ├── components/                        # Reusable UI components
│   │   ├── heatmap.py                    # GitHub-style heatmap
│   │   ├── streak_card.py                # Streak display
│   │   └── leaderboard_table.py          # Leaderboard component
│   ├── utils/                            # Helper functions
│   │   ├── api_client.py                # API calls
│   │   └── formatters.py                # Data formatting
│   └── assets/                          # Static files
│       ├── custom.css                  # Bootstrap overrides
│       └── logo.png                    # App logo
│
├── backend/                             # FastAPI Backend
│   ├── app/
│   │   ├── main.py                     # FastAPI app initialization
│   │   ├── api/                        # API endpoints
│   │   │   ├── routes/
│   │   │   │   ├── users.py           # User endpoints
│   │   │   │   ├── activities.py      # Activity tracking
│   │   │   │   ├── streaks.py         # Streak endpoints
│   │   │   │   └── leaderboard.py     # Leaderboard endpoints
│   │   │   └── deps.py                # Dependency injection
│   │   ├── models/                    # SQLAlchemy ORM models
│   │   │   ├── user.py               # User model
│   │   │   ├── activity.py           # Activity model
│   │   │   └── streak.py             # Streak model
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   │   ├── user.py              # User schemas
│   │   │   ├── activity.py          # Activity schemas
│   │   │   └── streak.py            # Streak schemas
│   │   ├── services/                # Business logic
│   │   │   ├── user_service.py      # User operations
│   │   │   ├── activity_service.py  # Activity operations
│   │   │   ├── streak_service.py    # Streak calculations
│   │   │   └── leaderboard_service.py # Leaderboard logic
│   │   ├── middleware/              # Custom middleware
│   │   │   ├── auth.py             # Authentication
│   │   │   └── error_handler.py    # Error handling
│   │   ├── utils/                  # Utilities
│   │   │   ├── security.py         # JWT & hashing
│   │   │   ├── decorators.py       # Custom decorators
│   │   │   └── constants.py        # Constants
│   │   └── core/                   # Configuration
│   │       ├── config.py           # App configuration
│   │       ├── database.py         # Database setup
│   │       └── logging.py          # Logging configuration
│   └── requirements.txt            # Backend dependencies
│
├── workers/                        # Celery & APScheduler
│   ├── celery_app.py              # Celery configuration
│   ├── tasks/                     # Async tasks
│   │   ├── streak_tasks.py        # Streak calculations
│   │   ├── notification_tasks.py  # Notifications
│   │   └── leaderboard_tasks.py   # Leaderboard generation
│   └── schedulers/                # Scheduled jobs
│       ├── config.py             # Scheduler configuration
│       └── main.py               # APScheduler entry point
│
├── database/                      # Database management
│   ├── migrations/               # Alembic migrations
│   │   ├── versions/            # Migration files
│   │   ├── env.py              # Migration environment
│   │   └── script.py.mako      # Migration template
│   └── seeds/                   # Sample data
│       ├── users.py            # Sample users
│       └── activities.py        # Sample activities
│
├── docker/                       # Container configuration
│   ├── Dockerfile.backend       # FastAPI container
│   ├── Dockerfile.frontend      # Streamlit container
│   ├── Dockerfile.celery        # Celery worker container
│   └── docker-compose.yml       # Multi-container setup
│
├── azure/                       # Azure deployment
│   ├── README.md               # Deployment guide
│   ├── azure-pipelines.yml     # CI/CD pipeline
│   └── terraform/              # Infrastructure as Code (future)
│
├── config/                      # Configuration files
│   ├── .env.example            # Environment template
│   ├── settings.py             # Pydantic settings
│   └── logging.yaml            # Logging configuration
│
├── tests/                      # Test suite
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/                  # Unit tests
│   │   ├── test_services.py   # Service tests
│   │   ├── test_models.py     # Model tests
│   │   └── test_utils.py      # Utility tests
│   └── integration/           # Integration tests
│       ├── test_api.py        # API endpoint tests
│       └── test_workflows.py  # Full workflow tests
│
├── scripts/                   # Utility scripts
│   ├── init_db.py           # Database initialization
│   ├── seed_data.py         # Data seeding
│   └── cleanup.py           # Cleanup tasks
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md      # System design
│   ├── API.md              # API documentation
│   ├── SETUP.md            # Local setup guide
│   └── DEPLOYMENT.md       # Deployment guide
│
└── requirements/            # Dependency management
    ├── base.txt            # Core dependencies
    ├── dev.txt             # Development dependencies
    └── prod.txt            # Production dependencies
```

## Key Features of This Structure

✅ **Separation of Concerns** - Clear division between frontend, backend, workers, and database
✅ **Scalability** - Easy to add new routes, services, models, and tasks
✅ **Testability** - Organized test structure mirrors production code
✅ **DevOps Ready** - Docker and Azure configurations included
✅ **Code Quality** - Pre-commit hooks, linting, and formatting setup
✅ **Documentation** - Comprehensive guides and architecture docs
✅ **Production Ready** - Environment management, error handling, logging

## Quick Navigation

| Layer | Location | Purpose |
|-------|----------|---------|
| **Frontend** | `frontend/` | Streamlit UI with heatmap & leaderboard |
| **API Server** | `backend/app/` | FastAPI endpoints |
| **Business Logic** | `backend/app/services/` | Core operations |
| **Database Models** | `backend/app/models/` | Data schemas |
| **Async Tasks** | `workers/tasks/` | Background processing |
| **Scheduled Jobs** | `workers/schedulers/` | Daily operations |
| **Tests** | `tests/` | Unit & integration tests |
| **Deployment** | `docker/` + `azure/` | Container & cloud setup |
