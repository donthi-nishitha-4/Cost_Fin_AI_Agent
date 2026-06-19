# Debugging Guide

## Initial Debugging Strategy
1. Validate environment setup (`.env` file)
2. Verify FastAPI startup (`python -m uvicorn app.main:app --reload`)
3. Verify endpoint responses
4. Check structured logs

## Current Verification Commands

Run automated tests:
```powershell
.\.venv\Scripts\python.exe -m pytest
```

Evaluate Agent Accuracy (LangSmith):
```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate_v2
```

## Common Issues

### Agent Endpoint Fails or Times Out
**Probable causes:**
- Ollama is not running.
- The PostgreSQL connection pool is exhausted.
- Planner returned invalid JSON.

**Checks:**
- Run `ollama list` to verify your model is downloaded.
- Ensure database connections are NOT being held open during `llm.invoke()` calls in `finance_service.py`. Connections should only be opened immediately before `db.execute()`.

### Tool Not Found or Hallucinated Subsystem IDs
**Probable causes:**
- Tool wrapper exists but is not registered in `app/tools/registry.py`.
- Planner is bypassing the *Chain of Thought* prompt.

**Checks:**
- Open your LangSmith UI, find the trace, and inspect the raw text output of the `planner_node` to see exactly how the LLM evaluated the boolean flags.

### Fixing Sub-94% Evaluation Accuracy
If your evaluation script (`evaluate_v2.py`) scores lower than 94%:
1. Check the Markdown Report (`docs/evaluation_reports/eval_report_v2_100.md`) for failures.
2. **Routing Failures**: If the Agent picked `subsystem_cost` instead of `cost_breakdown`, adjust the `CRITICAL RULE` keywords in `app/core/planner.py`.
3. **SQL Logic Failures**: If `system_analytics` returns empty data, the LLM generated incorrect SQL. Add explicit definitions to the "Hints" section of the Text-to-SQL prompt in `app/services/finance_service.py`.

### Missing Formatted Answer
If the final output is raw JSON without a conversational sentence:
- Check `app/core/response_formatter.py`. The LLM might have failed to format the SQL data.

## Pytest Cache Warning
If tests pass but show a warning about `.pytest_cache`, ignore it or clean it up:
```powershell
Remove-Item -Recurse -Force .pytest_cache
```
Make sure `.gitignore` includes `.pytest_cache/`.
