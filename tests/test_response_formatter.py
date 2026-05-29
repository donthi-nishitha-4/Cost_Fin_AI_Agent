from app.core.response_formatter import format_agent_response


def test_format_agent_response_adds_subsystem_cost_answer():
    result = format_agent_response({
        "status": "success",
        "tool": "subsystem_cost",
        "subsystem_id": 1,
        "data": {
            "tool": "subsystem_cost",
            "status": "success",
            "subsystem_id": 1,
            "data": {
                "subsystem": "Foundation",
                "planned_cost": 50000,
                "actual_cost": 42000,
                "remaining_budget": 8000
            }
        }
    })

    assert result["answer"] == (
        "Foundation has a planned cost of 50000, actual cost of 42000, "
        "and remaining budget of 8000."
    )


def test_format_agent_response_adds_financial_summary_answer():
    result = format_agent_response({
        "status": "success",
        "tool": "financial_summary",
        "subsystem_id": 1,
        "data": {
            "tool": "financial_summary",
            "status": "success",
            "subsystem_id": 1,
            "data": {
                "subsystem": "Foundation",
                "cost": {
                    "planned_cost": 50000,
                    "actual_cost": 42000,
                    "remaining_budget": 8000
                },
                "breakdown": {
                    "labor_cost": 15000,
                    "material_cost": 22000,
                    "equipment_cost": 5000
                },
                "budget_comparison": {
                    "planned_cost": 50000,
                    "actual_cost": 42000,
                    "variance": 8000,
                    "budget_status": "under_budget"
                },
                "overrun_risk": {
                    "utilization_percent": 84.0,
                    "risk_level": "medium"
                }
            }
        }
    })

    assert result["answer"] == (
        "Foundation has planned cost 50000, actual cost 42000, and remaining "
        "budget 8000. It is under_budget by 8000 and has used 84.0% of planned "
        "cost, giving it medium overrun risk."
    )


def test_format_agent_response_keeps_error_response_unchanged():
    result = {
        "status": "error",
        "message": "Planner failed"
    }

    assert format_agent_response(result) == result