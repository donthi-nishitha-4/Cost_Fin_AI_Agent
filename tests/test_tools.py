from app.tools.executor import execute_tool
from app.tools.finance_tools import get_subsystem_cost_tool


def test_subsystem_cost_tool_returns_structured_success_response():
    result = get_subsystem_cost_tool(1)

    assert result["status"] == "success"
    assert result["tool"] == "subsystem_cost"
    assert result["subsystem_id"] == 1
    assert result["data"]["remaining_budget"] == 8000


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
    assert result["data"]["subsystem"] == "Foundation"


def test_execute_tool_returns_error_for_unknown_tool():
    result = execute_tool("missing_tool", 1)

    assert result == {
        "status": "error",
        "message": "Tool 'missing_tool' not found"
    }
