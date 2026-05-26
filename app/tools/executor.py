from app.tools.registry import TOOL_REGISTRY

def execute_tool(tool_name: str, subsystem_id: int):

    tool = TOOL_REGISTRY.get(tool_name)

    if not tool:
        return {
            "status": "error",
            "message": f"Tool '{tool_name}' not found"
        }

    try:
        return tool(subsystem_id)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }