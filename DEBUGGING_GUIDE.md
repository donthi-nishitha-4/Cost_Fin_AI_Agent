# Debugging Guide

## Initial Debugging Strategy

1. Validate environment setup
2. Verify FastAPI startup
3. Verify endpoint responses
4. Use structured logging later

## Current Verification Commands

Run automated tests:

pytest

Run API locally:

uvicorn app.main:app --reload

Manual endpoint checks:

- GET http://127.0.0.1:8000/
- GET http://127.0.0.1:8000/api/v1/costs/1
- GET http://127.0.0.1:8000/api/v1/breakdown/1
- GET http://127.0.0.1:8000/agent?query=what%20is%20cost%20of%20subsystem%201

## Common Issues

- If /agent fails, confirm Ollama is running and llama3 is available locally.
- If /api/v1 routes return 404, confirm subsystem_router is included in app/main.py.
- If tool output is missing status/tool fields, confirm app/tools/registry.py points to tool wrapper functions.
