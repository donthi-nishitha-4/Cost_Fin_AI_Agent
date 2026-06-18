# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking,
and finance analytics in construction/project systems.

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
- Full PostgreSQL persistence migration
- Config-driven database connections
- 100-item realistic dataset with automatic seeding


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

## Persistence (PostgreSQL)

The application has fully migrated to a PostgreSQL persistence layer. The database schema is automatically generated and seeded with a 100-item evaluation dataset upon server startup if it is empty.

To manually re-seed or reset the database with the 100-item dataset:

```powershell
.\.venv\Scripts\python.exe -m app.core.seed_database
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
- `LANGSMITH_TRACING_V2`
- `LANGSMITH_API_KEY`
- `LANGSMITH_PROJECT`
- `LANGSMITH_ENDPOINT`

## DB Access
- `app/core/dependencies.py` exposes the active PostgreSQL session get_db.
- `app/core/postgres_database.py` manages the SQLAlchemy engine and session factory.