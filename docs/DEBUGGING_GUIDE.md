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

Run LLM Shootout Benchmark (Ollama vs Groq):
```powershell
.\.venv\Scripts\python.exe scripts\compare_llms.py
```

Evaluate Agent Accuracy (V5 Project-Grade):
```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate_v5
```

## Common Issues

### Groq Model Decommissioned Error
**Probable cause:**
- Groq constantly updates their ultra-fast models. If you see `model_decommissioned`, the `llama-3.1-8b-instant` endpoint might be deprecated.
**Checks:**
- Check [Groq Docs](https://console.groq.com/docs/models) for the newest model ID and update `app/core/llm_factory.py`.

### Agent Endpoint Fails or Times Out
**Probable causes:**
- Groq API key is missing from `.env` (if `LLM_PROVIDER=groq`).
- Ollama is not running locally (if `LLM_PROVIDER=ollama`).
- The PostgreSQL connection pool is exhausted.
- Planner returned invalid JSON.

**Checks:**
- Ensure `GROQ_API_KEY` is correctly pasted without quotes if running Groq.
- Run `ollama list` to verify your local model is downloaded if running Ollama.
- Ensure database connections are NOT being held open during `llm.invoke()` calls.

### Tool Not Found or Hallucinated Subsystem IDs
**Probable causes:**
- The LLM failed to route the logic correctly.
- Tool wrapper exists but is not registered in `app/tools/registry.py`.

**Checks:**
- Upgrade `LLM_PROVIDER` to `groq` to take advantage of significantly better logic processing.
- Open your LangSmith UI, find the trace, and inspect the raw text output of the `planner_node` to see exactly how the LLM evaluated the boolean flags.

### Fixing Sub-63% Evaluation Accuracy
If your evaluation script (`evaluate_v5.py`) drops below 63%:
1. Check the Markdown Report (`docs/evaluation_reports/eval_report_v5_100.md`) for Intent-based failures.
2. If `cost_lookup` fails heavily, ensure the Planner prompt explicitly clarifies the difference between specific cost queries and `cost_breakdown`.
3. **CRITICAL Failures**: If V5 reports a CRITICAL error, check if the LLM output reversed a sign (e.g., `-27000` instead of `+27000`), or check if `response_formatter.py` is formatting a logic contradiction.

### The Evaluation Tautology
If you see **100% Accuracy**, check `generate_golden_dataset.py`. If the ground truth was generated using the same LLM being evaluated, you have created a tautology ("grading its own homework"). Use the Strict Dataset generator to bypass the LLM and mathematically prove the agent.

### Regex Routing False Failures
If you see a `CRITICAL: Wrong budget status` on a Risk query (e.g., "Is subsystem 70 low risk?"), the V5 Evaluator's Python regex is likely broken. The regex `["is subsystem"]` falsely flags Risk queries as Budget queries. Do not punish the Agent; the LLM logic is actually correct. The true fix is replacing `evaluate_v5.py`'s regex router with LLM-as-a-Judge tool calling (planned for Phase 7).

## Pytest Cache Warning
If tests pass but show a warning about `.pytest_cache`, ignore it or clean it up:
```powershell
Remove-Item -Recurse -Force .pytest_cache
```
Make sure `.gitignore` includes `.pytest_cache/`.
