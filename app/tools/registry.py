from app.tools.finance_tools import (
    get_subsystem_cost_tool,
    get_cost_breakdown_tool,
    get_budget_comparison_tool
)

TOOL_REGISTRY = {
    "subsystem_cost": get_subsystem_cost_tool,
    "cost_breakdown": get_cost_breakdown_tool,
    "budget_comparison": get_budget_comparison_tool
}
