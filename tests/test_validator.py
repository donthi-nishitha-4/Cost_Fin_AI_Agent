from app.core.validator import validate_decision


def test_validate_decision_accepts_valid_tool_decision():
    result = validate_decision({
        "tool": "subsystem_cost",
        "subsystem_id": "1"
    })

    assert result == {
        "valid": True,
        "decision": {
            "tool": "subsystem_cost",
            "subsystem_id": 1
        }
    }

def test_validate_decision_accepts_budget_comparison_tool():
    result = validate_decision({
        "tool": "budget_comparison",
        "subsystem_id": "1"
    })

    assert result == {
        "valid": True,
        "decision": {
            "tool": "budget_comparison",
            "subsystem_id": 1
        }
    }

def test_validate_decision_accepts_overrun_risk_tool():
    result = validate_decision({
        "tool": "overrun_risk",
        "subsystem_id": "1"
    })

    assert result == {
        "valid": True,
        "decision": {
            "tool": "overrun_risk",
            "subsystem_id": 1
        }
    }

def test_validate_decision_accepts_financial_summary_tool():
    result = validate_decision({
        "tool": "financial_summary",
        "subsystem_id": "1"
    })

    assert result == {
        "valid": True,
        "decision": {
            "tool": "financial_summary",
            "subsystem_id": 1
        }
    }

def test_validate_decision_accepts_none_tool_without_subsystem():
    result = validate_decision({
        "tool": "none"
    })

    assert result == {
        "valid": True,
        "decision": {
            "tool": "none",
            "subsystem_id": None
        }
    }


def test_validate_decision_rejects_invalid_tool():
    result = validate_decision({
        "tool": "unknown_tool",
        "subsystem_id": 1
    })

    assert result["valid"] is False
    assert result["message"] == "Planner selected an invalid tool"


def test_validate_decision_rejects_missing_subsystem_id():
    result = validate_decision({
        "tool": "cost_breakdown"
    })

    assert result["valid"] is False
    assert result["message"] == "Planner must provide a numeric subsystem_id"
