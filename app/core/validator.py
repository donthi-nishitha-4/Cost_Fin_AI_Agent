VALID_TOOLS = {
    "subsystem_cost",
    "cost_breakdown",
    "budget_comparison",
    "none"
}


def validate_decision(decision):
    if not isinstance(decision, dict):
        return {
            "valid": False,
            "message": "Planner response must be a JSON object"
        }

    tool = decision.get("tool")

    if tool not in VALID_TOOLS:
        return {
            "valid": False,
            "message": "Planner selected an invalid tool"
        }

    if tool == "none":
        return {
            "valid": True,
            "decision": {
                "tool": "none",
                "subsystem_id": None
            }
        }

    subsystem_id = decision.get("subsystem_id")

    try:
        subsystem_id = int(subsystem_id)
    except (TypeError, ValueError):
        return {
            "valid": False,
            "message": "Planner must provide a numeric subsystem_id"
        }

    return {
        "valid": True,
        "decision": {
            "tool": tool,
            "subsystem_id": subsystem_id
        }
    }
