# API Contracts

## Health Check API

GET /

Response:
{
  "status": "running",
  "service": "Cost Finance AI Agent",
  "environment": "development"
}

## Agent API

GET /agent?query=give me full financial summary of subsystem 1

Response:
{
  "query": "give me full financial summary of subsystem 1",
  "answer": "Foundation has planned cost 50000, actual cost 42000, and remaining budget 8000. It is under_budget by 8000 and has used 84.0% of planned cost, giving it medium overrun risk.",
  "result": {
    "status": "success",
    "tool": "financial_summary",
    "subsystem_id": 1,
    "data": {
      "subsystem": "Foundation",
      "cost": {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "remaining_budget": 8000
      },
      "breakdown": {
        "subsystem": "Foundation",
        "labor_cost": 15000,
        "material_cost": 22000,
        "equipment_cost": 5000
      },
      "budget_comparison": {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "variance": 8000,
        "budget_status": "under_budget"
      },
      "overrun_risk": {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "utilization_percent": 84.0,
        "risk_level": "medium"
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

## Financial Summary API

GET /api/v1/financial-summary/{subsystem_id}

Success response:
{
  "subsystem": "Foundation",
  "cost": {
    "subsystem": "Foundation",
    "planned_cost": 50000,
    "actual_cost": 42000,
    "remaining_budget": 8000
  },
  "breakdown": {
    "subsystem": "Foundation",
    "labor_cost": 15000,
    "material_cost": 22000,
    "equipment_cost": 5000
  },
  "budget_comparison": {
    "subsystem": "Foundation",
    "planned_cost": 50000,
    "actual_cost": 42000,
    "variance": 8000,
    "budget_status": "under_budget"
  },
  "overrun_risk": {
    "subsystem": "Foundation",
    "planned_cost": 50000,
    "actual_cost": 42000,
    "utilization_percent": 84.0,
    "risk_level": "medium"
  }
}

Error response:
{
  "detail": "Subsystem not found"
}
