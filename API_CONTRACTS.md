# API Contracts

## Health Check API

GET /

Response:
{
  "status": "running",
  "service": "Cost Finance AI Agent"
}

## Agent API

GET /agent?query=what is cost of subsystem 1

Response:
{
  "query": "what is cost of subsystem 1",
  "result": {
    "status": "success",
    "tool": "subsystem_cost",
    "subsystem_id": 1,
    "data": {
      "tool": "subsystem_cost",
      "status": "success",
      "subsystem_id": 1,
      "data": {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "remaining_budget": 8000
      }
    }
  }
}

## Subsystem Cost API

GET /api/v1/costs/{subsystem_id}

Success response:
{
  "subsystem": "Foundation",
  "planned_cost": 50000,
  "actual_cost": 42000,
  "remaining_budget": 8000
}

Error response:
{
  "detail": "Subsystem not found"
}

## Cost Breakdown API

GET /api/v1/breakdown/{subsystem_id}

Success response:
{
  "subsystem": "Electrical",
  "labor_cost": 25000,
  "material_cost": 35000,
  "equipment_cost": 8000
}

Error response:
{
  "detail": "Subsystem not found"
}

## Budget Comparison API

GET /api/v1/budget-comparison/{subsystem_id}

Success response:
{
  "subsystem": "Foundation",
  "planned_cost": 50000,
  "actual_cost": 42000,
  "variance": 8000,
  "budget_status": "under_budget"
}

Error response:
{
  "detail": "Subsystem not found"
}

## Overrun Risk API

GET /api/v1/overrun-risk/{subsystem_id}

Success response:
{
  "subsystem": "Foundation",
  "planned_cost": 50000,
  "actual_cost": 42000,
  "utilization_percent": 84.0,
  "risk_level": "medium"
}

Error response:
{
  "detail": "Subsystem not found"
}