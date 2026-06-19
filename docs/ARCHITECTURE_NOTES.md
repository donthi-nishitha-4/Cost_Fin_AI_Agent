# Architecture Notes

## Current Validated Architecture

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
Tool Executor  --------> [If Text-to-SQL] ----> SQL Generator LLM -> Database
    |
Finance Tools
    |
Service Layer
    |
Finance Data (PostgreSQL)


## V2 - Stateful Graph Orchestration (LangGraph)
Migrated from LangChain's linear `AgentExecutor` to LangGraph's `StateGraph`. Explicit control flow:
1. **Planner Node (Chain of Thought)**: Evaluates boolean properties of the query first to determine scope, then selects the appropriate tool and extracts `subsystem_id`.
2. **Validator Node**: Catches LLM hallucinations before executing tools, safely rejecting or re-prompting.
3. **Executor Node**: Runs the requested backend tool safely.
4. **Formatter Node**: Converts JSON responses into human-readable text.

## Text-to-SQL Flow (Phase 5)
For aggregate queries (e.g., "Find severe overruns"), the architecture bypasses static REST logic:
1. The Planner routes to `system_analytics_tool`.
2. The `execute_system_query` function invokes the LLM with the database schema.
3. The LLM translates the query into raw PostgreSQL.
4. The database is queried natively (opening the connection pool *only* during execution).
5. The Formatter summarizes the dynamic JSON payload.

## Evaluation Architecture (LLM-as-a-Judge)
Evaluation runs via LangSmith test datasets (`evaluate_v2.py`) using a custom `semantic_match` evaluator. The Judge prompt mathematically verifies names, costs, and variances identically before issuing a `CORRECT` verdict. Current accuracy is 94%.

## Persistence & Config Layer
- `.env` -> `app/core/settings.py` -> app title, log level, LLM model, database URL
- PostgreSQL is the primary database, seeded automatically via `app/core/seed_database.py`.
- `app/core/database.py` manages the SQLAlchemy engine.

## Current Safeguards
- Planner output must pass JSON validation before tool execution.
- If Llama3 hallucinates non-JSON, a fallback mechanism instantly returns `tool: none` to fail safely.
- Database connections are strictly managed to prevent exhaustion during long external LLM inferences.
