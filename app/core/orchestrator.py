from app.core.response_formatter import format_agent_response
from app.core.planner import plan
from app.core.validator import validate_decision
from app.core.logger import logger
from app.tools.executor import execute_tool


def run_agent(query: str):

    logger.info(f"Agent query received: {query}")

    decision = plan(query)

    if not decision:
        logger.error("Planner failed to return a valid decision")
        return {
            "status": "error",
            "message": "Planner failed",
            "query": query
        }

    validation = validate_decision(decision)

    if not validation["valid"]:
        logger.error(f"Planner decision validation failed: {validation['message']}")
        return {
            "status": "error",
            "message": validation["message"],
            "query": query
        }

    decision = validation["decision"]

    logger.info(f"Planner decision accepted: {decision}")

    tool = decision.get("tool")

    if tool == "none":
        logger.info("No finance tool selected for query")
        agent_result = {
            "status": "success",
            "tool": "none",
            "message": "Ask about subsystem cost or breakdown"
        }

        return format_agent_response(agent_result)

    subsystem_id = decision.get("subsystem_id")

    result = execute_tool(tool, subsystem_id)

    logger.info(f"Tool execution completed: tool={tool}, subsystem_id={subsystem_id}")

    agent_result= {
        "status": "success",
        "tool": tool,
        "subsystem_id": subsystem_id,
        "data": result
    }
    
    return format_agent_response(agent_result)
