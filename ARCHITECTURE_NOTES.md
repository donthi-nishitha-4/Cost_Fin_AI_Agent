# Architecture Notes

## Current validated architecture

User Query
    |
API Layer
    |
Orchestrator
    |
Planner
    |
Validator
    |
Tool Registry
    |
Tool Executor
    |
Finance Tools
    |
Service Layer
    |
Finance Data

## Stabilized routes

- GET /
- GET /agent?query=...
- GET /api/v1/costs/{subsystem_id}
- GET /api/v1/breakdown/{subsystem_id}
- GET /api/v1/budget-comparison/{subsystem_id}

## Current safeguards

- Planner output is validated before tool execution.
- Tool execution goes through registered tool wrappers.
- Finance tool calls emit structured log messages.
- Budget comparison is available through service, tool, API, and agent layers.
