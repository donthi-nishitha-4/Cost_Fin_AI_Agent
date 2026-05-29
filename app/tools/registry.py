from app.tools.finance_tools import (
    get_subsystem_cost_tool,
    get_cost_breakdown_tool,
    get_budget_comparison_tool,
    get_overrun_risk_tool,
    get_financial_summary_tool
)

TOOL_REGISTRY = {
    "subsystem_cost": get_subsystem_cost_tool,
    "cost_breakdown": get_cost_breakdown_tool,
    "budget_comparison": get_budget_comparison_tool,
    "overrun_risk": get_overrun_risk_tool,
    "financial_summary": get_financial_summary_tool
}
