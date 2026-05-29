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

class FinancialSummaryResponse(BaseModel):
    subsystem: str
    cost: CostResponse
    breakdown: CostBreakdownResponse
    budget_comparison: BudgetComparisonResponse
    overrun_risk: OverrunRiskResponse