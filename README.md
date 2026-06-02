# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking,
and finance analytics in construction/project systems.

## Current Version

Phase 3 configuration and SQLite persistence foundation.

## Features implemented

- FastAPI backend
- Health check endpoint
- Versioned finance APIs
- Config management through `.env`
- SQLite database foundation
- SQLAlchemy engine and session setup
- Database seeding from mock finance data
- LangChain/Ollama-based planner
- Tool registry and executor
- Planner decision validation
- Structured logging foundation
- Request correlation IDs
- Global error handling
- Human-readable agent response formatting
- Automated pytest coverage

## Finance capabilities

- Subsystem cost summary
- Cost breakdown
- Budget comparison
- Overrun risk analysis
- Full financial summary

## Main API endpoints

- GET /
- GET /agent?query=...
- GET /api/v1/costs/{subsystem_id}
- GET /api/v1/breakdown/{subsystem_id}
- GET /api/v1/budget-comparison/{subsystem_id}
- GET /api/v1/overrun-risk/{subsystem_id}
- GET /api/v1/financial-summary/{subsystem_id}

## Run locally

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Current status

```text
44 passed
```

## Demo query

```powershell
curl "http://127.0.0.1:8000/agent?query=give%20me%20full%20financial%20summary%20of%20subsystem%201"
```

The agent response includes:

- a human-readable answer
- raw structured finance data

## Config

Environment values are loaded from `.env`:

- `PROJECT_NAME`
- `ENVIRONMENT`
- `LOG_LEVEL`
- `LLM_MODEL`
- `DATABASE_URL`
- `DB_ECHO`

## Persistence

SQLite is used as the first Phase 3 persistence layer.

Initialize the database manually with:

```powershell
.\.venv\Scripts\python.exe -m scripts.init_db

SQLite is the first Phase 3 persistence layer.