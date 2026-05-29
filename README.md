# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking,
and finance analytics in construction/project systems.

## Current Version

Phase 2 multi-tool finance agent foundation.

## Features implemented

- FastAPI backend
- Health check endpoint
- Versioned finance APIs
- LangChain/Ollama-based planner
- Tool registry and executor
- Planner decision validation
- Structured logging foundation
- Mock finance dataset integration
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
```
.\.venv\Scripts\python.exe -m pytest
```
### Current status:
    38 passed

## Demo query
```
curl "http://127.0.0.1:8000/agent?query=give%20me%20full%20financial%20summary%20of%20subsystem%201"
```

### The agent response includes: A human-readable answer & raw structured finance data