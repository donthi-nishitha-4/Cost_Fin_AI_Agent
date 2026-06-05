# Debugging Guide

## Initial Debugging Strategy

1. Validate environment setup
2. Verify FastAPI startup
3. Verify endpoint responses
4. Check structured logs

## Current Verification Commands

Run automated tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run API locally:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Manual endpoint checks:

```powershell
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/v1/costs/1
curl http://127.0.0.1:8000/api/v1/breakdown/1
curl http://127.0.0.1:8000/api/v1/budget-comparison/1
curl http://127.0.0.1:8000/api/v1/overrun-risk/1
curl http://127.0.0.1:8000/api/v1/financial-summary/1
curl "http://127.0.0.1:8000/agent?query=what%20is%20cost%20of%20subsystem%201"
```

## Demo Verification Flow

1. Start server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

2. Verify full financial summary API:

```powershell
curl http://127.0.0.1:8000/api/v1/financial-summary/1
```

Expected response should include:

```json
"subsystem": "Foundation"
```

and:

```json
"risk_level": "medium"
```

3. Verify agent formatted response:

```powershell
curl "http://127.0.0.1:8000/agent?query=give%20me%20full%20financial%20summary%20of%20subsystem%201"
```

Expected agent response should include:

```json
"tool": "financial_summary"
```

and:

```json
"answer": "Foundation has planned cost..."
```

4. Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected:

```text
47 passed
```

## Config Notes

- `.env` now drives `PROJECT_NAME`, `ENVIRONMENT`, `LOG_LEVEL`, and `LLM_MODEL`
- PostgreSQL settings are staged in `.env` but not yet active at runtime
- `app/core/settings.py` is the single source of truth for app configuration
- If the app title or model changes, update `.env` first

## Common Issues

### Agent endpoint fails

Probable causes:

- Ollama is not running
- `llama3` model is not available locally
- Planner returned invalid JSON

Checks:

```powershell
ollama list
ollama run llama3
```

### API route returns 404

Probable causes:

- Router is not included in `app/main.py`
- Endpoint path is typed incorrectly
- Server was not restarted after code changes

Check that `app/main.py` includes:

```python
app.include_router(subsystem_router, prefix="/api/v1", tags=["finance"])
```

### Tool not found

Probable causes:

- Tool wrapper exists but is not registered
- Tool name in planner does not match tool name in registry
- Validator allows a tool that executor does not know

Check:

```text
app/tools/registry.py
app/core/validator.py
app/core/planner.py
```

### Missing formatted answer

Probable causes:

- `format_agent_response` is not called in orchestrator
- Tool result shape changed
- Formatter does not support selected tool

Check:

```text
app/core/orchestrator.py
app/core/response_formatter.py
```

### Pytest cache warning

If tests pass but show a warning about `.pytest_cache`, it is usually safe to ignore.

Optional cleanup:

```powershell
Remove-Item -Recurse -Force .pytest_cache
```

Make sure `.gitignore` includes:

```gitignore
.pytest_cache/
__pycache__/
*.pyc
```

## Phase 3 Database Check

Run the SQLite initializer:

```powershell
.\.venv\Scripts\python.exe -m scripts.init_db
```

Expected:

```text
Database initialized and seeded.
```

Then verify the app still passes tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected:

```text
47 passed
```
