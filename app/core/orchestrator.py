from app.core.planner import plan
from app.tools.executor import execute_tool


def run_agent(query: str):

    print("\n====================")
    print("USER QUERY:", query)

    decision = plan(query)

    if not decision:
        return {
            "status": "error",
            "message": "Planner failed",
            "query": query
        }

    print("DECISION:", decision)

    tool = decision.get("tool")

    if tool == "none":
        return {
            "status": "success",
            "tool": "none",
            "message": "Ask about subsystem cost or breakdown"
        }

    subsystem_id = decision.get("subsystem_id")

    result = execute_tool(tool, subsystem_id)

    return {
        "status": "success",
        "tool": tool,
        "subsystem_id": subsystem_id,
        "data": result
    }