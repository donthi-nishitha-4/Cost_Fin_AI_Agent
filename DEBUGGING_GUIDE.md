# Debugging Guide

## Quick Verification Checklist

Before investigating a bug, verify the project baseline.

### Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected:

```text
44 passed
```

### Start the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Verify Health Endpoint

```powershell
curl http://127.0.0.1:8000/
```

Expected:

* HTTP 200
* Application responds successfully

---

## Core Endpoint Verification

### Cost Summary

```powershell
curl http://127.0.0.1:8000/api/v1/costs/1
```

### Cost Breakdown

```powershell
curl http://127.0.0.1:8000/api/v1/breakdown/1
```

### Budget Comparison

```powershell
curl http://127.0.0.1:8000/api/v1/budget-comparison/1
```

### Overrun Risk

```powershell
curl http://127.0.0.1:8000/api/v1/overrun-risk/1
```

### Financial Summary

```powershell
curl http://127.0.0.1:8000/api/v1/financial-summary/1
```

Expected response includes:

```json
{
  "subsystem": "Foundation"
}
```

and

```json
{
  "risk_level": "medium"
}
```

---

## Agent Verification

### Example Query

```powershell
curl "http://127.0.0.1:8000/agent?query=give%20me%20full%20financial%20summary%20of%20subsystem%201"
```

Expected:

```json
{
  "tool": "financial_summary"
}
```

and

```json
{
  "answer": "Foundation has planned cost..."
}
```

---

## Configuration Troubleshooting

### Environment Variables Not Loading

Check:

```text
.env
app/core/settings.py
```

Verify:

* PROJECT_NAME
* ENVIRONMENT
* LOG_LEVEL
* LLM_MODEL
* DATABASE_URL

Settings should be loaded only through:

```text
app/core/settings.py
```

---

## Agent Issues

### Agent Endpoint Fails

Possible causes:

* Ollama is not running
* Llama3 is unavailable
* Planner generated invalid output

Checks:

```powershell
ollama list
ollama run llama3
```

---

### Tool Not Found

Possible causes:

* Tool exists but is not registered
* Planner tool name mismatch
* Validator and registry are out of sync

Check:

```text
app/tools/registry.py
app/core/planner.py
app/core/validator.py
```

---

### Missing Human-Readable Answer

Possible causes:

* Response formatter not invoked
* Tool response shape changed
* Formatter logic missing support

Check:

```text
app/core/orchestrator.py
app/core/response_formatter.py
```

---

## API Issues

### Route Returns 404

Possible causes:

* Router not registered
* Incorrect URL path
* Server restart required

Verify:

```python
app.include_router(
    subsystem_router,
    prefix="/api/v1",
    tags=["finance"]
)
```

---

## Database Troubleshooting

### Initialize Database

```powershell
.\.venv\Scripts\python.exe -m scripts.init_db
```

Expected:

```text
Database initialized and seeded.
```

---

### SQLite Validation

After initialization:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected:

```text
44 passed
```

---

## PostgreSQL Migration Checklist

Before switching endpoints:

* PostgreSQL URL configured
* Connection test successful
* Session dependency verified
* Repository queries validated
* Pilot endpoint selected

Recommended migration order:

1. costs/{subsystem_id}
2. breakdown/{subsystem_id}
3. budget-comparison/{subsystem_id}
4. overrun-risk/{subsystem_id}
5. financial-summary/{subsystem_id}

Test after each migration step.

---

## Development Cleanup

### Pytest Cache Warning

Optional cleanup:

```powershell
Remove-Item -Recurse -Force .pytest_cache
```

Recommended `.gitignore` entries:

```gitignore
.pytest_cache/
__pycache__/
*.pyc
```
