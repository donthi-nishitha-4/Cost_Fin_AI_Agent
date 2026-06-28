# API Contracts

*(Note: Phase 4 & 5 introduced LangGraph Agent V2 which processes natural language queries through `finance_agent_v2.py`. The HTTP contract remains identical, but the internal routing is now stateful. System-wide aggregate queries are supported dynamically via the `/agent` endpoint).*

## Health Check API
GET `/`

Response:
```json
{
  "status": "running",
  "service": "Cost Finance AI Agent",
  "environment": "development"
}
```

## Agent API (NLP Interface)
GET `/agent?query=give me full financial summary of subsystem 1`
*(Supports specific subsystem questions AND global aggregate system analytics)*

Response:
```json
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
        "planned_cost": 150000.0,
        "actual_cost": 150000.0,
        "remaining_budget": 0.0
      }
      // ... breakdown, budget_comparison, overrun_risk objects included
    }
  }
}
```

## Subsystem Cost API
GET `/api/v1/costs/{subsystem_id}`

Success response:
```json
{
  "subsystem": "Fire Protection - Tower A",
  "planned_cost": 150000.0,
  "actual_cost": 150000.0,
  "remaining_budget": 0.0
}
```

## Cost Breakdown API
GET `/api/v1/breakdown/{subsystem_id}`

Success response:
```json
{
  "subsystem": "Structural Steel - Tower B",
  "labor_cost": 160822.07,
  "material_cost": 201265.22,
  "equipment_cost": 543532.47
}
```

## Budget Comparison API
GET `/api/v1/budget-comparison/{subsystem_id}`

Success response:
```json
{
  "subsystem": "Fire Protection - Tower A",
  "planned_cost": 150000.0,
  "actual_cost": 150000.0,
  "variance": 0.0,
  "budget_status": "under_budget"
}
```

## Overrun Risk API
GET `/api/v1/overrun-risk/{subsystem_id}`

Success response:
```json
{
  "subsystem": "Fire Protection - Tower A",
  "planned_cost": 150000.0,
  "actual_cost": 150000.0,
  "utilization_percent": 100.0,
  "risk_level": "high"
}
```

## Financial Summary API
GET `/api/v1/financial-summary/{subsystem_id}`

Success response:
```json
{
  "subsystem": "Fire Protection - Tower A",
  "cost": {},
  "breakdown": {},
  "budget_comparison": {},
  "overrun_risk": {}
}
```

## NLP Agent Dynamic Tool Executions (V1.2 Overrides)
For natural language queries processed through `/agent?query=...`:
1. **Aggregate Override**: Queries asking for sums, averages, counts, or severe overruns are dynamically rewritten inside `planner.py` to target the `"system_analytics"` tool, forcing `subsystem_id: 1` as default.
2. **Comparison Override**: Queries comparing multiple subsystems (e.g. subsystem 12 and 19) are routed to `"system_analytics"` using SQL-level standard `WHERE id IN (12, 19)`.
3. **Single-Subsystem Summary Override**: Queries asking for a summary of exactly 1 subsystem (e.g. `financial summary of subsystem 17`) are intercepted and routed straight to the `"financial_summary"` tool, guaranteeing 100% formatted template accuracy.
