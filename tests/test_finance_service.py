from app.services.finance_service import get_cost_breakdown, get_subsystem_cost


def test_get_subsystem_cost_returns_remaining_budget():
    result = get_subsystem_cost(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "remaining_budget": 8000
    }


def test_get_subsystem_cost_returns_none_for_unknown_subsystem():
    assert get_subsystem_cost(999) is None


def test_get_cost_breakdown_returns_cost_categories():
    result = get_cost_breakdown(2)

    assert result == {
        "subsystem": "Electrical",
        "labor_cost": 25000,
        "material_cost": 35000,
        "equipment_cost": 8000
    }

def test_get_budget_comparison_returns_budget_status():
    from app.services.finance_service import get_budget_comparison

    result = get_budget_comparison(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "variance": 8000,
        "budget_status": "under_budget"
    }


def test_get_budget_comparison_returns_none_for_unknown_subsystem():
    from app.services.finance_service import get_budget_comparison

    assert get_budget_comparison(999) is None

def test_get_overrun_risk_returns_risk_level():
    from app.services.finance_service import get_overrun_risk

    result = get_overrun_risk(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "utilization_percent": 84.0,
        "risk_level": "medium"
    }


def test_get_overrun_risk_returns_none_for_unknown_subsystem():
    from app.services.finance_service import get_overrun_risk

    assert get_overrun_risk(999) is None