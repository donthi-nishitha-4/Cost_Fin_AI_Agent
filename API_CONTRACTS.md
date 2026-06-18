# API Contracts

*(Note: Phase 4 introduces LangGraph Agent V2 which processes queries through `finance_agent_v2.py`. The HTTP contract remains identical, but the internal routing is now stateful.)*

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
  "answer": "Fire Protection - Tower A has planned cost 150000.0, actual cost 150000.0, and remaining budget 0.0. It is under_budget by 0.0 and has used 100.0% of planned cost, giving it high overrun risk.",
  "result": {
    "status": "success",
    "tool": "financial_summary",
    "subsystem_id": 1,
    "data": {
      "subsystem": "Fire Protection - Tower A",
      "cost": {
        "subsystem": "Fire Protection - Tower A",
        "planned_cost": 150000.0,
        "actual_cost": 150000.0,
        "remaining_budget": 0.0
      },
      "breakdown": {
        "subsystem": "Fire Protection - Tower A",
        "labor_cost": 45303.24,
        "material_cost": 57287.05,
        "equipment_cost": 31635.68
      },
      "budget_comparison": {
        "subsystem": "Fire Protection - Tower A",
        "planned_cost": 150000.0,
        "actual_cost": 150000.0,
        "variance": 0.0,
        "budget_status": "under_budget"
      },
      "overrun_risk": {
        "subsystem": "Fire Protection - Tower A",
        "planned_cost": 150000.0,
        "actual_cost": 150000.0,
        "utilization_percent": 100.0,
        "risk_level": "high"
      }
    }
  }
}

## Subsystem Cost API

GET /api/v1/costs/{subsystem_id}

Success response:
{
  "subsystem": "Fire Protection - Tower A",
  "planned_cost": 150000.0,
  "actual_cost": 150000.0,
  "remaining_budget": 0.0
}

Error response:
{
  "detail": "Subsystem not found"
}

## Cost Breakdown API

GET /api/v1/breakdown/{subsystem_id}

Success response:
{
  "subsystem": "Structural Steel - Tower B",
  "labor_cost": 160822.07,
  "material_cost": 201265.22,
  "equipment_cost": 543532.47
}

Error response:
{
  "detail": "Subsystem not found"
}

## Budget Comparison API

GET /api/v1/budget-comparison/{subsystem_id}

Success response:
{
  "subsystem": "Fire Protection - Tower A",
  "planned_cost": 150000.0,
  "actual_cost": 150000.0,
  "variance": 0.0,
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
  "subsystem": "Fire Protection - Tower A",
  "planned_cost": 150000.0,
  "actual_cost": 150000.0,
  "utilization_percent": 100.0,
  "risk_level": "high"
}

Error response:
{
  "detail": "Subsystem not found"
}

## Financial Summary API

GET /api/v1/financial-summary/{subsystem_id}

Success response:
{
  "subsystem": "Fire Protection - Tower A",
  "cost": {
    "subsystem": "Fire Protection - Tower A",
    "planned_cost": 150000.0,
    "actual_cost": 150000.0,
    "remaining_budget": 0.0
  },
  "breakdown": {
    "subsystem": "Fire Protection - Tower A",
    "labor_cost": 45303.24,
    "material_cost": 57287.05,
    "equipment_cost": 31635.68
  },
  "budget_comparison": {
    "subsystem": "Fire Protection - Tower A",
    "planned_cost": 150000.0,
    "actual_cost": 150000.0,
    "variance": 0.0,
    "budget_status": "under_budget"
  },
  "overrun_risk": {
    "subsystem": "Fire Protection - Tower A",
    "planned_cost": 150000.0,
    "actual_cost": 150000.0,
    "utilization_percent": 100.0,
    "risk_level": "high"
  }
}

Error response:
{
  "detail": "Subsystem not found"
}
