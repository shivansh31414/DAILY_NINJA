# Environment Variables & Configuration Guide

This guide covers how to set up environment variables for Daily Ninja across development, testing, and production environments.

## Quick Start

### 1. Copy Environment Template Files

```bash
# From project root
cp .env.example .env
cp backend/.env.example backend/.env
cp config/.env.example config/.env
```

### 2. Update Values for Your Environment

```bash
# Edit the files with your configuration
nano .env                  # Main config
nano backend/.env          # Backend-specific config
nano config/.env           # Application config
```

### 3. Ensure .env Files Are Ignored

The `.gitignore` should already include `*.env` to prevent committing secrets:

```bash
# Verify .gitignore has this:
grep "\.env" .gitignore
```

## Environment Files Overview

### `.env` (Root)
Main application environment configuration. Includes deployment mode, security keys, and service URLs.

### `backend/.env`
Backend (Flask API) specific configuration. Database connections, JWT secrets, and server settings.

### `config/.env`
Additional application configuration used by both frontend and backend. Database details, Redis, Azure keys, etc.

## Configuration Hierarchy

The application loads environment variables in this order:

1. **System Environment Variables** (highest priority)
2. **`.env` files** in each directory (loaded via `python-dotenv`)
3. **Default values in code** (lowest priority)

This means you can override file-based config with system environment variables.

---

## Environment Variables by Scope

### 🔒 Security Variables

**REQUIRED FOR PRODUCTION** - Generate strong random values for these:

```bash
# Generate secure keys (run in Python):
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

**Variables:**

| Variable | Purpose | Dev Default | Production | Required |
|----------|---------|-------------|-----------|----------|
| `SECRET_KEY` | Flask session encryption | `dev-...` | Strong random | ✅ Yes |
| `JWT_SECRET_KEY` | JWT token signing | `jwt-...` | Strong random | ✅ Yes |

⚠️ **DO NOT** use development defaults in production!

### 🗄️ Database Variables

| Variable | Purpose | Dev Default | Production | Example |
|----------|---------|-------------|-----------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///daily_ninja.db` | PostgreSQL/Azure SQL | `postgresql://user:pass@host:5432/daily_ninja` |

**Examples for Different Databases:**

```bash
# SQLite (Development)
DATABASE_URL=sqlite:///daily_ninja.db

# PostgreSQL (Production - Recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/daily_ninja

# Azure SQL Server (Production - Azure)
DATABASE_URL=mssql+pyodbc://user:password@server.database.windows.net/daily_ninja?driver=ODBC+Driver+18+for+SQL+Server

# Remote PostgreSQL (e.g., AWS RDS)
DATABASE_URL=postgresql://user:password@daily-ninja.c123456.us-west-2.rds.amazonaws.com:5432/daily_ninja
```

### 🚀 Server Configuration

| Variable | Purpose | Dev Default | Production |
|----------|---------|-------------|-----------|
| `PORT` | Backend server port | `5000` | `5000` |
| `FLASK_ENV` | Execution environment | `development` | `production` |
| `DEBUG` | Debug mode (Flask) | `true` | `false` |
| `LOG_LEVEL` | Logging verbosity | `DEBUG` | `INFO` |

### 🔄 Caching & Message Queue (Optional)

These are optional for development but **recommended for production**:

```bash
# Redis cache
REDIS_URL=redis://localhost:6379/0

# Celery task queue
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### 🌐 API & Frontend URLs

| Variable | Purpose | Dev Example | Production |
|----------|---------|-------------|-----------|
| `API_BASE_URL` | Backend API URL (used by frontend) | `http://localhost:5000` | `https://api.yourdomain.com` |
| `FRONTEND_BASE_URL` | Frontend URL | `http://localhost:8501` | `https://yourdomain.com` |
| `CORS_ORIGINS` | Allowed request origins | `*` | `https://yourdomain.com` |

### 🛡️ CORS Configuration

**Development (Permissive):**
```env
CORS_ORIGINS=*
```

**Production (Restrictive):**
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://app.yourdomain.com
```

### ☁️ Azure Configuration (If Using Azure)

```env
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_STORAGE_ACCOUNT=your-storage-account
AZURE_SQL_SERVER=your-sql-server.database.windows.net
AZURE_SQL_DATABASE=daily_ninja
```

---

## Setup by Environment

### 📝 Development Setup

```bash
# 1. Copy templates
cp .env.example .env
cp backend/.env.example backend/.env

# 2. Edit for local development (backend/. senv)
FLASK_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///daily_ninja.db
SECRET_KEY=dev-secret-key-123
JWT_SECRET_KEY=jwt-secret-key-123

# 3. Backend should auto-create SQLite database
python backend/run.py
```

### 🧪 Testing Setup

```bash
# Copy config
cp config/.env.example config/.env

# Edit config/.env for testing
ENV=testing
DATABASE_URL=sqlite:///:memory:  # In-memory database for tests
DEBUG=true
```

Run tests:
```bash
pytest tests/ --env testing
```

### 🔒 Production Setup (Docker)

**Create `.env` for production secrets:**

```bash
cat > .env << 'EOF'
FLASK_ENV=production
DEBUG=false
LOG_LEVEL=WARNING

# GENERATE NEW SECURE VALUES
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Database (e.g., Azure SQL)
DATABASE_URL=mssql+pyodbc://user:password@server.database.windows.net/daily_ninja?driver=ODBC+Driver+18+for+SQL+Server

# URLs for production
API_BASE_URL=https://api.yourdomain.com
FRONTEND_BASE_URL=https://yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# Caching (recommended)
REDIS_URL=redis://cache-server:6379/0
CELERY_BROKER_URL=redis://cache-server:6379/1
EOF
```

**Build and run Docker:**

```bash
# Build images with environment from .env
docker-compose --env-file .env build

# Start services
docker-compose --env-file .env up -d

# View logs
docker-compose logs -f backend
```

### ☁️ Azure App Service Deployment

In Azure Portal, set environment variables in **Configuration > Application settings:**

1. Go to your App Service
2. Navigate to **Settings > Configuration**
3. Add each environment variable as an **Application setting** (not Connection string):

```
+---------------------------+-----------------------------+
| Name                      | Value                       |
+---------------------------+-----------------------------+
| FLASK_ENV                 | production                  |
| SECRET_KEY                | (generated strong value)    |
| JWT_SECRET_KEY            | (generated strong value)    |
| DATABASE_URL              | mssql+pyodbc://...          |
| REDIS_URL                 | (if using Azure Cache)      |
| CORS_ORIGINS              | https://yourdomain.com      |
+---------------------------+-----------------------------+
```

Then deploy:
```bash
az webapp deployment source config-zip --resource-group mygroup --name myapp --src app.zip
```

---

## 🔐 Security Best Practices

### 1. Generate Strong Secrets

```bash
# Generate a 32-character URL-safe random string (use in both commands)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Example output: "AbCd1234EfGhIjKlMnOpQrStUvWxYz_-"
```

### 2. Never Commit Secrets

```bash
# Verify .gitignore includes .env files
grep "\.env" .gitignore

# If not already there, add:
echo "*.env" >> .gitignore
echo ".env*" >> .gitignore
echo "!.env.example" >> .gitignore

# Remove any .env files from git history (if accidentally committed)
git rm --cached .env backend/.env config/.env
git commit -m "Remove .env files from git history"
```

### 3. Use Environment Variables in Production

Instead of .env files in production, use your platform's secret management:

- **Azure**: Azure Key Vault
- **AWS**: AWS Secrets Manager / Parameter Store
- **Heroku**: Config Vars
- **Docker**: Docker secrets (for Swarm) or stack secrets

### 4. Rotate Secrets Regularly

In production, periodically rotate:
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- Database passwords
- API keys

### 5. Audit Access

Log who accesses sensitive resources:
```bash
# Example: Monitor database connections
audit_log="var/log/database_audit.log"
echo "User $USER connected to database at $(date)" >> $audit_log
```

---

## Loading Environment Variables Programmatically

### In Python Code

```python
import os
from dotenv import load_dotenv

# Load from .env file (development)
load_dotenv()

# Access environment variables
database_url = os.getenv("DATABASE_URL", "sqlite:///daily_ninja.db")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG", "false").lower() == "true"

# Require specific variables in production
if os.getenv("FLASK_ENV") == "production":
    if not os.getenv("SECRET_KEY"):
        raise ValueError("SECRET_KEY must be set in production!")
```

### In Docker

```dockerfile
# Set defaults in Dockerfile
ENV FLASK_ENV=development
ENV PORT=5000

# Override with --env-file or -e flag when running
# docker run --env-file .env myapp
# docker run -e SECRET_KEY=xyz myapp
```

### In docker-compose.yml

```yaml
services:
  backend:
    environment:
      FLASK_ENV: ${FLASK_ENV:-development}
      SECRET_KEY: ${SECRET_KEY}
      DATABASE_URL: ${DATABASE_URL}
    env_file:
      - .env
```

---

## Troubleshooting

### ❌ "SECRET_KEY not set" error in production

**Problem**: Application requires `SECRET_KEY` in production config.

**Solution**: Make sure `SECRET_KEY` is set as an environment variable:
```bash
# Local .env file
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" >> .env

# Or set in environment before running
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
python backend/run.py
```

### ❌ Database connection refused

**Problem**: `DATABASE_URL` is incorrect or service isn't running.

**Solution**: Check the connection string format:
```bash
# Test PostgreSQL connection
psql "${DATABASE_URL}"

# Test SQLite file exists
ls -la daily_ninja.db

# Check .env has correct DATABASE_URL
grep DATABASE_URL backend/.env
```

### ❌ CORS errors in browser

**Problem**: Frontend can't access backend API (CORS blocked).

**Solution**: Ensure `CORS_ORIGINS` includes your frontend URL:
```bash
# backend/.env
CORS_ORIGINS=http://localhost:8501,https://yourdomain.com
```

### ❌ PORT already in use

**Problem**: Can't start server on configured PORT.

**Solution**: Check what's using the port:
```bash
# Linux/macOS
lsof -i :5000

# Windows
netstat -ano | findstr :5000

# Change PORT in .env
echo "PORT=5001" >> .env
```

---

## References

- [python-dotenv Documentation](https://github.com/thixel/python-dotenv)
- [Flask Configuration](https://flask.palletsprojects.com/config/)
- [Azure Key Vault](https://azure.microsoft.com/services/key-vault/)
- [Docker Secrets Management](https://docs.docker.com/engine/swarm/secrets/)

---

**Last Updated**: February 10, 2026
