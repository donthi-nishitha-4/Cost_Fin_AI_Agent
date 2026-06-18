# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking,
and finance analytics in construction/project systems.

## Current Version

## Current Version

Phase 4 (Advanced AI & Production Readiness) is complete. The project utilizes LangGraph, LangSmith, and a strict LLM-as-a-judge Semantic Evaluation suite.
- **Accuracy**: 77.0% across 100 conversational queries.
- **Failures**: Identified exclusively as aggregate analytics queries (e.g. "Which subsystem has the most cost?").
- **Next Up**: Phase 5 (Text-to-SQL System-Wide Analytics Tool).

## Features implemented

- FastAPI backend
- Health check endpoint
- Versioned finance APIs
- Config management through `.env`
- SQLite database foundation
- SQLAlchemy engine and session setup
- Database seeding from mock finance data
- Dependency helpers for SQLite and PostgreSQL sessions
- LangChain/Ollama-based planner
- Tool registry and executor
- Planner decision validation
- Structured logging foundation
- Request correlation IDs
- Global error handling
- Human-readable agent response formatting
- Automated pytest coverage synchronized to the 100-item dataset
- Automated evaluation markdown reporting (`generate_report.py`)
- Completed SQLite foundation
- PostgreSQL session path is wired for the finance endpoints
- Manual API verification passed

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
49 passed
```

## Evaluate the Agent

To run the full 100-item LangSmith semantic evaluation locally:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate_v2
```

To automatically generate the markdown report (saved to `docs/evaluation_reports/`):

```powershell
.\.venv\Scripts\python.exe -m scripts.generate_report
```

## Persistence

SQLite is the first Phase 3 persistence layer.

Initialize the database manually with:

```powershell
.\.venv\Scripts\python.exe -m scripts.init_db
```

This creates the schema and seeds the database from the mock finance dataset.

## PostgreSQL Pilot

The finance API routes are currently wired to the PostgreSQL session path for the pilot migration.

Use the following manual checks:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/costs/1
Invoke-RestMethod http://127.0.0.1:8000/api/v1/breakdown/1
Invoke-RestMethod http://127.0.0.1:8000/api/v1/budget-comparison/1
Invoke-RestMethod http://127.0.0.1:8000/api/v1/overrun-risk/1
Invoke-RestMethod http://127.0.0.1:8000/api/v1/financial-summary/1
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
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DRIVER`

## Persistence

SQLite is the first Phase 3 persistence layer.

Initialize the database manually with:

```powershell
.\.venv\Scripts\python.exe -m scripts.init_db
```

This creates the schema and seeds the database from the mock finance dataset.

## DB Access

- `app/core/dependencies.py` exposes SQLite and PostgreSQL session helpers.
- `app/core/postgres_database.py` prepares the PostgreSQL engine and session factory.
