from app.core.database import get_db
from app.repositories.finance_repository import get_finance_subsystem_by_id


def get_subsystem_cost(subsystem_id: int):
    return get_subsystem_cost_from_db(subsystem_id)


def get_subsystem_cost_from_db(subsystem_id: int):
    db = next(get_db())
    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        remaining_budget = row.planned_cost - row.actual_cost

        return {
            "subsystem": row.subsystem_name,
            "planned_cost": row.planned_cost,
            "actual_cost": row.actual_cost,
            "remaining_budget": remaining_budget
        }
    finally:
        db.close()


def get_cost_breakdown_from_db(subsystem_id: int):
    db = next(get_db())
    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        return {
            "subsystem": row.subsystem_name,
            "labor_cost": row.labor_cost,
            "material_cost": row.material_cost,
            "equipment_cost": row.equipment_cost
        }
    finally:
        db.close()


def get_budget_comparison_from_db(subsystem_id: int):
    db = next(get_db())
    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        variance = row.planned_cost - row.actual_cost

        if variance >= 0:
            budget_status = "under_budget"
        else:
            budget_status = "over_budget"

        return {
            "subsystem": row.subsystem_name,
            "planned_cost": row.planned_cost,
            "actual_cost": row.actual_cost,
            "variance": variance,
            "budget_status": budget_status
        }
    finally:
        db.close()


def get_overrun_risk_from_db(subsystem_id: int):
    db = next(get_db())
    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        utilization_percent = round((row.actual_cost / row.planned_cost) * 100, 2)

        if utilization_percent >= 90:
            risk_level = "high"
        elif utilization_percent >= 75:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "subsystem": row.subsystem_name,
            "planned_cost": row.planned_cost,
            "actual_cost": row.actual_cost,
            "utilization_percent": utilization_percent,
            "risk_level": risk_level
        }
    finally:
        db.close()


def get_cost_breakdown(subsystem_id: int):
    return get_cost_breakdown_from_db(subsystem_id)


def get_budget_comparison(subsystem_id: int):
    return get_budget_comparison_from_db(subsystem_id)


def get_overrun_risk(subsystem_id: int):
    return get_overrun_risk_from_db(subsystem_id)


def get_financial_summary(subsystem_id: int):
    cost = get_subsystem_cost(subsystem_id)
    breakdown = get_cost_breakdown(subsystem_id)
    budget_comparison = get_budget_comparison(subsystem_id)
    overrun_risk = get_overrun_risk(subsystem_id)

    if not cost:
        return None

    return {
        "subsystem": cost["subsystem"],
        "cost": cost,
        "breakdown": breakdown,
        "budget_comparison": budget_comparison,
        "overrun_risk": overrun_risk
    }
