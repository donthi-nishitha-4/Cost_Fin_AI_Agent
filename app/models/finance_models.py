from pydantic import BaseModel


class CostResponse(BaseModel):
    subsystem: str
    planned_cost: float
    actual_cost: float
    remaining_budget: float


class CostBreakdownResponse(BaseModel):
    subsystem: str
    labor_cost: float
    material_cost: float
    equipment_cost: float

class BudgetComparisonResponse(BaseModel):
    subsystem: str
    planned_cost: float
    actual_cost: float
    variance: float
    budget_status: str

class OverrunRiskResponse(BaseModel):
    subsystem: str
    planned_cost: float
    actual_cost: float
    utilization_percent: float
    risk_level: str