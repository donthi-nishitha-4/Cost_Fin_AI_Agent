# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking, and finance analytics in construction and project management systems.

## Current Version

**v1.2 (Phase 1 Freeze - Local Model Stable Optimization)** is complete.
- **Local Model Accuracy**: Local evaluation benchmark using Ollama `llama3` local model achieves a mathematically proven **98.9% Overall Score** (99.2% Math, 97.6% Semantic Match) across **124 golden queries** via the hardened V5 evaluator.
- **Safe SQL Translation**: Restructured prompts ban table joins and aliases for multi-subsystem lookups, ensuring psycopg compatibility and preventing SQL injection/hallucinations.
- **Deterministic Routing**: Integrated split-word keyword checks (e.g. `average`, `total`, `sum`, `count`) and single-subsystem summary checks directly in `planner.py` to route queries flawlessly without relying on LLM inference.
- **Observability**: Programmatically integrated with LangSmith for production-grade agent run tracing.

## Features Implemented

### Backend & Data Foundation
- FastAPI backend with versioned REST APIs (`/api/v1/...`)
- PostgreSQL database integration with automated seeding (`app/core/seed_database.py`)
- Config management through `.env` and Pydantic (`app/core/settings.py`)
- Global error handling, request correlation IDs, and structured logging

### AI Agent Layer (LangGraph)
- **Stateful Orchestration**: Built on LangGraph `StateGraph` for deterministic node execution (Planner -> Validator -> Executor -> Formatter).
- **Dynamic LLM Factory**: `app/core/llm_factory.py` seamlessly checks `LLM_PROVIDER` to inject the correct LLM anywhere in the stack.
- **Chain of Thought Planner**: The LLM parses user intent logically to prevent routing hallucinations.
- **Text-to-SQL Engine**: Dynamically executes safe, read-only aggregate queries against PostgreSQL.
- **Generative Formatter**: Converts raw JSON database output into polished conversational sentences.

### Observability & Testing
- Natively integrated with LangSmith Tracing (`LANGCHAIN_TRACING_V2`)
- 100-item realistic evaluation dataset with extreme edge cases
- **V5 Project-Grade Evaluator**: (`scripts/evaluate_v5.py`) A 5-Layer framework testing Intent Classification, Targeted Extraction, Math Precision, and Business Logic safely independently of semantic scoring.
- **Automated Shootout**: (`scripts/compare_llms.py`) to directly benchmark latency and quality between Ollama and Groq.
- Automated Markdown Evaluation Reporting (`scripts/generate_report_v5.py`)

## Finance Capabilities

- Subsystem Cost Summary
- Detailed Cost Breakdown (Labor, Material, Equipment)
- Budget Comparison (Planned vs Actual)
- Overrun Risk Analysis
- Full Financial Summary
- System-Wide Analytics (Cross-subsystem queries)

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

Run the LLM Shootout (Ollama vs Groq):
```powershell
.\.venv\Scripts\python.exe scripts\compare_llms.py
```

Evaluate the Agent Locally (Ollama Llama3):
```powershell
.\.venv\Scripts\python.exe scripts/evaluate_v5_local.py
```

## Config Variables

Environment values are loaded from `.env`:
- `PROJECT_NAME`, `ENVIRONMENT`, `LOG_LEVEL`
- `LLM_PROVIDER` (e.g. `groq` or `ollama`)
- `GROQ_API_KEY` (Required if using groq)
- `DATABASE_URL`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `LANGSMITH_TRACING_V2`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`