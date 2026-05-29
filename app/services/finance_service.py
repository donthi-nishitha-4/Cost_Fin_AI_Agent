from app.data.mock_finance_data import SUBSYSTEM_DATA


def get_subsystem_cost(subsystem_id: int):
    data = SUBSYSTEM_DATA.get(subsystem_id)

    if not data:
        return None

    remaining_budget = (
        data["planned_cost"] - data["actual_cost"]
    )

    return {
        "subsystem": data["subsystem"],
        "planned_cost": data["planned_cost"],
        "actual_cost": data["actual_cost"],
        "remaining_budget": remaining_budget
    }


def get_cost_breakdown(subsystem_id: int):
    data = SUBSYSTEM_DATA.get(subsystem_id)

    if not data:
        return None

    return {
        "subsystem": data["subsystem"],
        "labor_cost": data["labor_cost"],
        "material_cost": data["material_cost"],
        "equipment_cost": data["equipment_cost"]
    }

def get_budget_comparison(subsystem_id: int):
    data = SUBSYSTEM_DATA.get(subsystem_id)

    if not data:
        return None

    planned_cost = data["planned_cost"]
    actual_cost = data["actual_cost"]
    variance = planned_cost - actual_cost

    if variance >= 0:
        budget_status = "under_budget"
    else:
        budget_status = "over_budget"

    return {
        "subsystem": data["subsystem"],
        "planned_cost": planned_cost,
        "actual_cost": actual_cost,
        "variance": variance,
        "budget_status": budget_status
    }

def get_overrun_risk(subsystem_id: int):
    data = SUBSYSTEM_DATA.get(subsystem_id)

    if not data:
        return None

    planned_cost = data["planned_cost"]
    actual_cost = data["actual_cost"]

    utilization_percent = round((actual_cost / planned_cost) * 100, 2)

    if utilization_percent >= 90:
        risk_level = "high"
    elif utilization_percent >= 75:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "subsystem": data["subsystem"],
        "planned_cost": planned_cost,
        "actual_cost": actual_cost,
        "utilization_percent": utilization_percent,
        "risk_level": risk_level
    }
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


