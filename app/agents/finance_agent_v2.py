from typing import TypedDict, Optional, Dict, Any
# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, END

from app.core.planner import plan
from app.core.validator import validate_decision
from app.tools.executor import execute_tool
from app.core.response_formatter import format_agent_response
from app.core.logger import logger

# 1. Define the State
class AgentState(TypedDict):
    query: str
    decision: Optional[Dict[str, Any]]
    validation_error: Optional[str]
    tool_result: Optional[Dict[str, Any]]
    final_response: Optional[Dict[str, Any]]

# 2. Define the Nodes
def planner_node(state: AgentState) -> AgentState:
    logger.info(f"[V2] Planner Node: Analyzing query: {state['query']}")
    decision = plan(state["query"])
    return {"decision": decision}

def validator_node(state: AgentState) -> AgentState:
    logger.info("[V2] Validator Node: Validating decision")
    decision = state.get("decision")
    
    if not decision:
        return {"validation_error": "Planner failed to return a valid decision"}
        
    validation = validate_decision(decision)
    if not validation["valid"]:
        return {"validation_error": validation["message"]}
        
    return {"decision": validation["decision"], "validation_error": None}

def executor_node(state: AgentState) -> AgentState:
    logger.info("[V2] Executor Node: Running tool")
    decision = state["decision"]
    tool = decision.get("tool")
    query = state["query"]
    
    if tool == "none":
        return {"tool_result": {"status": "success", "tool": "none", "message": "Ask about subsystem cost or breakdown"}}
        
    subsystem_id = decision.get("subsystem_id")
    result = execute_tool(tool, subsystem_id,query)
    
    if result.get("status") == "error":
        return {"tool_result": {
            "status": "error",
            "tool": tool,
            "message": result.get("message")
        }}
        
    return {"tool_result": {
        "status": "success",
        "tool": tool,
        "subsystem_id": subsystem_id,
        "data": result.get("data")
    }}

def formatter_node(state: AgentState) -> AgentState:
    logger.info("[V2] Formatter Node: Formatting final response")
    
    # If validation failed, return error formatting
    if state.get("validation_error"):
        error_result = {
            "status": "error",
            "message": state["validation_error"],
            "query": state["query"]
        }
        # Assuming format_agent_response handles errors gracefully, otherwise just return it directly
        # Let's return raw error for simplicity if validation failed
        return {"final_response": error_result}
        
    # Otherwise format successful tool execution
    tool_result = state.get("tool_result")
    final = format_agent_response(tool_result)
    return {"final_response": final}

# 3. Define Conditional Routing
def route_after_validation(state: AgentState) -> str:
    if state.get("validation_error"):
        return "formatter"
    return "executor"

# 4. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("validator", validator_node)
workflow.add_node("executor", executor_node)
workflow.add_node("formatter", formatter_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "validator")
workflow.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "executor": "executor",
        "formatter": "formatter"
    }
)
workflow.add_edge("executor", "formatter")
workflow.add_edge("formatter", END)

# Compile the graph
finance_agent_v2 = workflow.compile()

# Provide a helper function identical to v1 for easy swapping
def ask_finance_agent_v2(query: str):
    logger.info("--- Starting V2 LangGraph Agent ---")
    initial_state = {
        "query": query, 
        "decision": None, 
        "validation_error": None, 
        "tool_result": None, 
        "final_response": None
    }
    
    # Run the graph
    result = finance_agent_v2.invoke(initial_state)
    
    return result["final_response"]
