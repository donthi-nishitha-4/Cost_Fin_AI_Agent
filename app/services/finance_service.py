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