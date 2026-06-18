# Architecture Notes

## Current validated architecture

User Query
    |
API Layer
    |
Agent V2 (LangGraph StateGraph)
    |-- Planner Node
    |-- Validator Node
    |-- Executor Node
    |-- Formatter Node
    |
Tool Registry
    |
Tool Executor
    |
Finance Tools
    |
Response Formatter
    |
Service Layer
    |
Finance Data

## V2 - Stateful Graph Orchestration (LangGraph)
Migrated from LangChain's linear `AgentExecutor` to LangGraph's `StateGraph`. This allows explicit control flow:
1. **Planner Node**: Determines intent and extracts the exact `subsystem_id` directly from the user query.
2. **Validator Node**: Catches LLM hallucinations (e.g. invalid tool names) before executing tools, safely rejecting or re-prompting.
3. **Executor Node**: Runs the requested backend tool safely.
4. **Formatter Node**: Converts JSON responses into human-readable text.

## Evaluation Architecture (LLM-as-a-Judge)
Evaluation runs via LangSmith test datasets using a custom `semantic_match` evaluator. 
Because small LLMs are highly prone to "false positives" in evaluation, the Judge prompt enforces extreme strictness: it mathematically verifies the subsystem name and all financial costs/variances match identically before issuing a `CORRECT` verdict.

## Observability (LangSmith)

- LangSmith Tracing is natively integrated via `LANGCHAIN_TRACING_V2` environment variables.
- The `evaluate_v2.py` script leverages LangSmith Datasets and an LLM-as-a-Judge semantic evaluator.

## Config layer

`.env` -> `app/core/settings.py` -> app title, log level, LLM model, database URL

## Persistence layer

`app/core/database.py` -> SQLAlchemy engine/session (configured via DATABASE_URL)
`app/core/dependencies.py` -> Database session helpers
`app/repositories/finance_repository.py` -> database reads

## Persistence tools

- `app/core/database.py` creates the SQLAlchemy engine and session factory based on the active `DATABASE_URL`.
- PostgreSQL is the primary database, but the system remains provider-agnostic.
- `app/core/seed_database.py` seeds the database from the mock finance data on startup.
- `app/repositories/finance_repository.py` handles finance table reads.
- `app/core/dependencies.py` exposes DB session helpers for route injection.

## Stabilized routes

- GET /
- GET /agent?query=...
- GET /api/v1/costs/{subsystem_id}
- GET /api/v1/breakdown/{subsystem_id}
- GET /api/v1/budget-comparison/{subsystem_id}
- GET /api/v1/overrun-risk/{subsystem_id}
- GET /api/v1/financial-summary/{subsystem_id}

## Current safeguards

- Planner output is validated before tool execution.
- Tool execution goes through registered tool wrappers.
- Finance tool calls emit structured log messages.
- Budget comparison is available through service, tool, API, and agent layers.
- Overrun risk is available through service, tool, API, and agent layers.
- Financial summary combines cost, breakdown, budget comparison, and overrun risk into one response.
- Agent responses include both human-readable answers and raw structured data.
- Application behavior is driven from a single settings object loaded from `.env`.
- Database is seeded automatically from the mock finance dataset.
- Service functions now read finance cost data through the repository layer.
- Database session helpers are available for route injection.
