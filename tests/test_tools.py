from app.tools.executor import execute_tool
from app.tools.finance_tools import get_subsystem_cost_tool, get_budget_comparison_tool, get_overrun_risk_tool,get_financial_summary_tool


def test_subsystem_cost_tool_returns_structured_success_response():
    result = get_subsystem_cost_tool(1)

    assert result["status"] == "success"
    assert result["tool"] == "subsystem_cost"
    assert result["subsystem_id"] == 1
    assert result["data"]["remaining_budget"] == 0.0


def test_subsystem_cost_tool_returns_error_for_unknown_subsystem():
    result = get_subsystem_cost_tool(999)

    assert result == {
        "status": "error",
        "message": "Subsystem not found"
    }


def test_execute_tool_uses_registered_tool_wrapper():
    result = execute_tool("cost_breakdown", 1)

    assert result["status"] == "success"
    assert result["tool"] == "cost_breakdown"
    assert result["data"]["subsystem"] == "Fire Protection - Tower A"

def test_budget_comparison_tool_returns_budget_status():
    result = get_budget_comparison_tool(1)

    assert result["status"] == "success"
    assert result["tool"] == "budget_comparison"
    assert result["data"]["budget_status"] == "under_budget"


def test_execute_tool_runs_budget_comparison():
    result = execute_tool("budget_comparison", 1)

    assert result["status"] == "success"
    assert result["tool"] == "budget_comparison"
    assert result["data"]["subsystem"] == "Fire Protection - Tower A"
    assert result["data"]["budget_status"] == "under_budget"

def test_overrun_risk_tool_returns_structured_success_response():
    result = get_overrun_risk_tool(1)

    assert result["status"] == "success"
    assert result["tool"] == "overrun_risk"
    assert result["subsystem_id"] == 1
    assert result["data"]["utilization_percent"] == 100.0
    assert result["data"]["risk_level"] == "high"


def test_execute_tool_runs_overrun_risk():
    result = execute_tool("overrun_risk", 1)

    assert result["status"] == "success"
    assert result["tool"] == "overrun_risk"
    assert result["data"]["subsystem"] == "Fire Protection - Tower A"
    assert result["data"]["risk_level"] == "high"

def test_financial_summary_tool_returns_structured_success_response():
    result = get_financial_summary_tool(1)

    assert result["status"] == "success"
    assert result["tool"] == "financial_summary"
    assert result["subsystem_id"] == 1
    assert result["data"]["subsystem"] == "Fire Protection - Tower A"
    assert result["data"]["cost"]["remaining_budget"] == 0.0
    assert result["data"]["overrun_risk"]["risk_level"] == "high"


def test_execute_tool_runs_financial_summary():
    result = execute_tool("financial_summary", 1)

    assert result["status"] == "success"
    assert result["tool"] == "financial_summary"
    assert result["data"]["subsystem"] == "Fire Protection - Tower A"
    assert result["data"]["budget_comparison"]["budget_status"] == "under_budget"