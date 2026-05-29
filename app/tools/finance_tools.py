from app.services.finance_service import (
    get_subsystem_cost,
    get_cost_breakdown,
    get_budget_comparison,
    get_overrun_risk
)

from app.core.logger import logger


# ----------------------------
# TOOL 1: Subsystem Cost
# ----------------------------
def get_subsystem_cost_tool(subsystem_id: int):

    subsystem_id = int(subsystem_id)

    logger.info(
        f"Executing subsystem cost tool for subsystem_id={subsystem_id}"
    )

    result = get_subsystem_cost(subsystem_id)

    if not result:

        logger.error(
            f"Subsystem not found for id={subsystem_id}"
        )

        return {
            "status": "error",
            "message": "Subsystem not found"
        }

    logger.info(
        f"Subsystem cost retrieved successfully"
    )

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

    logger.info(
        f"Executing cost breakdown tool for subsystem_id={subsystem_id}"
    )

    result = get_cost_breakdown(subsystem_id)

    if not result:

        logger.error(
            f"Breakdown not found for id={subsystem_id}"
        )

        return {
            "status": "error",
            "message": "Breakdown not found"
        }

    logger.info(
        f"Cost breakdown retrieved successfully"
    )

    return {
        "tool": "cost_breakdown",
        "status": "success",
        "subsystem_id": subsystem_id,
        "data": result
    }

# ----------------------------
# TOOL 3: Budget Comparison
# ----------------------------
def get_budget_comparison_tool(subsystem_id: int):

    subsystem_id = int(subsystem_id)

    logger.info(
        f"Executing budget comparison tool for subsystem_id={subsystem_id}"
    )

    result = get_budget_comparison(subsystem_id)

    if not result:

        logger.error(
            f"Budget comparison not found for id={subsystem_id}"
        )

        return {
            "status": "error",
            "message": "Budget comparison not found"
        }

    logger.info(
        "Budget comparison retrieved successfully"
    )

    return {
        "tool": "budget_comparison",
        "status": "success",
        "subsystem_id": subsystem_id,
        "data": result
    }


# ----------------------------
# TOOL 4: Overrun Risk
# ----------------------------
def get_overrun_risk_tool(subsystem_id: int):

    subsystem_id = int(subsystem_id)

    logger.info(
        f"Executing overrun risk tool for subsystem_id={subsystem_id}"
    )

    result = get_overrun_risk(subsystem_id)

    if not result:

        logger.error(
            f"Overrun risk not found for id={subsystem_id}"
        )

        return {
            "status": "error",
            "message": "Overrun risk not found"
        }

    logger.info(
        "Overrun risk retrieved successfully"
    )

    return {
        "tool": "overrun_risk",
        "status": "success",
        "subsystem_id": subsystem_id,
        "data": result
    }


# ----------------------------
# TOOL REGISTRY
# ----------------------------
TOOLS = {
    "subsystem_cost": get_subsystem_cost_tool,
    "cost_breakdown": get_cost_breakdown_tool,
    "budget_comparison": get_budget_comparison_tool,
    "overrun_risk": get_overrun_risk_tool
}