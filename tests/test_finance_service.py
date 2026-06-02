from app.core.database import engine
from app.core.seed_database import seed_finance_database
from app.models.db_base import Base
from app.services.finance_service import (
    get_budget_comparison,
    get_budget_comparison_from_db,
    get_cost_breakdown,
    get_cost_breakdown_from_db,
    get_financial_summary,
    get_overrun_risk,
    get_overrun_risk_from_db,
    get_subsystem_cost,
    get_subsystem_cost_from_db,
)

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
    result = get_budget_comparison(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "variance": 8000,
        "budget_status": "under_budget"
    }


def test_get_budget_comparison_returns_none_for_unknown_subsystem():
    assert get_budget_comparison(999) is None

def test_get_overrun_risk_returns_risk_level():
    result = get_overrun_risk(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "utilization_percent": 84.0,
        "risk_level": "medium"
    }


def test_get_overrun_risk_returns_none_for_unknown_subsystem():
    assert get_overrun_risk(999) is None



def test_get_financial_summary_returns_all_finance_sections():
    result = get_financial_summary(1)

    assert result["subsystem"] == "Foundation"
    assert result["cost"]["remaining_budget"] == 8000
    assert result["breakdown"]["labor_cost"] == 15000
    assert result["budget_comparison"]["budget_status"] == "under_budget"
    assert result["overrun_risk"]["risk_level"] == "medium"


def test_get_financial_summary_returns_none_for_unknown_subsystem():
    assert get_financial_summary(999) is None

def test_get_subsystem_cost_from_db_returns_remaining_budget():
    Base.metadata.create_all(bind=engine)
    seed_finance_database()

    result = get_subsystem_cost_from_db(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "remaining_budget": 8000
    }

def test_get_cost_breakdown_from_db_returns_cost_categories():
    Base.metadata.create_all(bind=engine)
    seed_finance_database()

    result = get_cost_breakdown_from_db(2)

    assert result == {
        "subsystem": "Electrical",
        "labor_cost": 25000,
        "material_cost": 35000,
        "equipment_cost": 8000
    }

def test_get_budget_comparison_from_db_returns_budget_status():
    Base.metadata.create_all(bind=engine)
    seed_finance_database()

    result = get_budget_comparison_from_db(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "variance": 8000,
        "budget_status": "under_budget"
    }


def test_get_overrun_risk_from_db_returns_risk_level():
    Base.metadata.create_all(bind=engine)
    seed_finance_database()

    result = get_overrun_risk_from_db(1)

    assert result == {
        "subsystem": "Foundation",
        "planned_cost": 50000,
        "actual_cost": 42000,
        "utilization_percent": 84.0,
        "risk_level": "medium"
    }
