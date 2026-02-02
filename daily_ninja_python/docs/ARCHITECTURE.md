# Daily Ninja - Architecture Documentation

## System Design

### Overview
Daily Ninja is a Python fullstack application built with FastAPI backend, Streamlit frontend, PostgreSQL database, and async task processing with Celery.

### Core Components

#### 1. Frontend (Streamlit)
- Multi-page Streamlit application
- Bootstrap 5 styling
- Plotly charts for heatmap visualization
- Real-time leaderboard updates via API

#### 2. Backend (FastAPI)
- RESTful API endpoints
- WebSocket support for real-time features
- JWT authentication
- Rate limiting and CORS handling

#### 3. Database (PostgreSQL)
- User accounts and authentication
- Activity tracking
- Streak calculation
- Leaderboard data

#### 4. Caching (Redis)
- Session caching
- Leaderboard caching
- Real-time data cache

#### 5. Async Processing (Celery)
- Daily streak calculations
- Batch notifications
- Leaderboard updates
- Data aggregation

#### 6. Scheduling (APScheduler)
- Daily streak resets
- Leaderboard generation
- Cleanup jobs

## Data Flow

```
User Action (Frontend)
    ↓
REST API (FastAPI)
    ↓
Database (PostgreSQL)
    ↓
Cache (Redis)
    ↓
Async Task (Celery)
    ↓
Background Processing (APScheduler)
    ↓
Updated Data → Frontend
```

## Key Design Patterns

### Service Layer Pattern
- Separation of concerns
- Reusable business logic
- Easy testing

### Repository Pattern
- Database abstraction
- Consistent data access
- Migration-friendly

### Event-Driven Architecture
- Celery tasks for async operations
- APScheduler for scheduled jobs
- Decoupled services

## Scalability Considerations

- Horizontal scaling via containerization
- Database connection pooling
- Redis caching layers
- Async task processing
- CDN for static assets (future)
