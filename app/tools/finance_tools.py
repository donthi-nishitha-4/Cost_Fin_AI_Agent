from app.services.finance_service import (
    get_subsystem_cost
)


def get_subsystem_cost_tool(subsystem_id: int):
    """
    Tool function used by LangChain agent to fetch subsystem cost details.

    Args:
        subsystem_id (int): ID of subsystem

    Returns:
        dict: subsystem cost details or error message
    """

    try:
        # ----------------------------
        # INPUT VALIDATION
        # ----------------------------
        subsystem_id = int(subsystem_id)

        if subsystem_id <= 0:
            return {
                "status": "error",
                "message": "subsystem_id must be a positive integer"
            }

        # ----------------------------
        # SERVICE CALL
        # ----------------------------
        result = get_subsystem_cost(subsystem_id)

        # ----------------------------
        # RESPONSE HANDLING
        # ----------------------------
        if not result:
            return {
                "status": "error",
                "message": f"No data found for subsystem_id={subsystem_id}"
            }

        return {
            "status": "success",
            "subsystem_id": subsystem_id,
            "data": result
        }

    except ValueError:
        return {
            "status": "error",
            "message": "Invalid subsystem_id format. Must be integer."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }