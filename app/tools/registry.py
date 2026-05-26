from app.tools.finance_tools import (
    get_subsystem_cost,
    get_cost_breakdown
)

TOOL_REGISTRY = {
    "subsystem_cost": get_subsystem_cost,
    "cost_breakdown": get_cost_breakdown
}