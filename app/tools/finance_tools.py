from app.services.finance_service import (
    get_subsystem_cost,
    get_cost_breakdown
)


# ----------------------------
# TOOL 1: Subsystem Cost
# ----------------------------
def get_subsystem_cost_tool(subsystem_id: int):
    subsystem_id = int(subsystem_id)

    result = get_subsystem_cost(subsystem_id)

    if not result:
        return {"status": "error", "message": "Subsystem not found"}

    return {
        "tool": "subsystem_cost",
        "status": "success",
        "subsystem_id": subsystem_id,
        "data": result
    }


# ----------------------------
# TOOL 2: Cost Breakdown
# ----------------------------
def get_cost_breakdown_tool(subsystem_id: int):
    subsystem_id = int(subsystem_id)

    result = get_cost_breakdown(subsystem_id)

    if not result:
        return {"status": "error", "message": "Breakdown not found"}

    return {
        "tool": "cost_breakdown",
        "status": "success",
        "subsystem_id": subsystem_id,
        "data": result
    }


# ----------------------------
# TOOL REGISTRY (IMPORTANT)
# ----------------------------
TOOLS = {
    "subsystem_cost": get_subsystem_cost_tool,
    "cost_breakdown": get_cost_breakdown_tool
}