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