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
