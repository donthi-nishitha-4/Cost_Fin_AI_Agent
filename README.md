# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking, and finance analytics in construction and project management systems.

## Current Version

**Phase 5 (System-Wide Analytics & Text-to-SQL)** is complete. The project utilizes LangGraph, LangSmith, and a strict LLM-as-a-judge Semantic Evaluation suite.
- **Accuracy**: 94.0% across 100 complex conversational queries.
- **New Capabilities**: A Text-to-SQL engine now safely translates natural language into aggregate PostgreSQL queries.
- **Next Up**: Phase 6 (Groq LLM Migration for ultra-fast cloud inference).

## Features Implemented

### Backend & Data Foundation
- FastAPI backend with versioned REST APIs (`/api/v1/...`)
- PostgreSQL database integration with automated seeding (`app/core/seed_database.py`)
- Config management through `.env` and Pydantic (`app/core/settings.py`)
- Global error handling, request correlation IDs, and structured logging

### AI Agent Layer (LangGraph)
- **Stateful Orchestration**: Built on LangGraph `StateGraph` for deterministic node execution (Planner -> Validator -> Executor -> Formatter).
- **Chain of Thought Planner**: The LLM parses user intent logically to prevent routing hallucinations.
- **Text-to-SQL Engine**: Dynamically executes safe, read-only aggregate queries.
- **Tool Registry**: Modular finance tools to fetch live database records.
- **Generative Formatter**: Converts raw JSON database output into polished conversational sentences.

### Observability & Testing
- Natively integrated with LangSmith Tracing (`LANGCHAIN_TRACING_V2`)
- 100-item realistic evaluation dataset with extreme edge cases
- Automated LLM-as-a-judge semantic evaluation suite (`scripts/evaluate_v2.py`)
- Automated Markdown Evaluation Reporting (`scripts/generate_report.py`)
- Pytest coverage synchronized to the 100-item dataset

## Finance Capabilities

- Subsystem Cost Summary
- Detailed Cost Breakdown (Labor, Material, Equipment)
- Budget Comparison (Planned vs Actual)
- Overrun Risk Analysis
- Full Financial Summary
- **[NEW]** System-Wide Analytics (Cross-subsystem queries)

## Main API Endpoints

- `GET /` (Healthcheck)
- `GET /agent?query=...` (AI Agent interface)
- `GET /api/v1/costs/{subsystem_id}`
- `GET /api/v1/breakdown/{subsystem_id}`
- `GET /api/v1/budget-comparison/{subsystem_id}`
- `GET /api/v1/overrun-risk/{subsystem_id}`
- `GET /api/v1/financial-summary/{subsystem_id}`

*(Note: Aggregate queries are handled dynamically via the `/agent` endpoint and do not have static REST routes).*

## Run Locally

Start the backend:
```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Run unit tests:
```powershell
.\.venv\Scripts\python.exe -m pytest
```

Evaluate the Agent (LangSmith):
```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate_v2
```

Generate Markdown Evaluation Report:
```powershell
.\.venv\Scripts\python.exe -m scripts.generate_report
```

## Demo Query

```powershell
curl "http://127.0.0.1:8000/agent?query=Find%20severe%20overruns"
```

## Config Variables

Environment values are loaded from `.env`:
- `PROJECT_NAME`, `ENVIRONMENT`, `LOG_LEVEL`
- `LLM_MODEL`
- `DATABASE_URL`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `LANGSMITH_TRACING_V2`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`