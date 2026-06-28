import json
import re

from app.core.llm_factory import get_llm


def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None
    return None


def plan(query: str):
    prompt = f"""
You are a finance AI planner.
Return ONLY JSON:
{{
  "tool": "system_analytics or cost_breakdown or subsystem_cost or budget_comparison or overrun_risk or financial_summary or none",
  "subsystem_id": 1
}}
CRITICAL RULE: If the query asks "Which subsystem", "Find subsystems", "Find severe overruns", or asks an aggregate question about ALL subsystems, you MUST use "system_analytics", even if it contains words like 'budget', 'equipment', or 'risk'.
CRITICAL RULE: If the query asks SPECIFICALLY for "labor", "material", or "equipment" cost, you MUST use "cost_breakdown", NEVER use "subsystem_cost".
CRITICAL RULE: If the query asks for a "percentage" or "ratio" of budget/cost consumed/used (even for a specific subsystem), you MUST use "system_analytics" to calculate it dynamically.
CRITICAL RULE: If the query asks for multiple different types of information (e.g. planned/actual cost AND labor/material breakdown, or summary AND comparison of multiple subsystems), you MUST use "system_analytics" to fetch all required fields dynamically.
CRITICAL RULE: If the query mentions MULTIPLE subsystem IDs (e.g. subsystem 12 and subsystem 19, or compare subsystem 15 and 42), you MUST use "system_analytics", never route to single subsystem tools.
CRITICAL RULE: If the query asks to compare planned and actual cost (or variance/budget status) for a SINGLE subsystem ID (e.g. "Compare planned and actual cost for subsystem 38"), you MUST use "budget_comparison", NOT "system_analytics".
Use system_analytics for system-wide aggregate questions.
Use financial_summary for full summary, complete summary of a SPECIFIC subsystem.
Use subsystem_cost for total cost, planned cost, actual cost, expenditure, spending, or remaining budget of a SPECIFIC subsystem.
Use cost_breakdown for SPECIFIC components like labor cost, material cost, equipment cost, or breakdown of a SPECIFIC subsystem.
Use budget_comparison for over budget, under budget, variance, unused budget, remaining budget, remaining funds, or overspent allocation of a SPECIFIC subsystem.
Use overrun_risk for overrun risk, high risk, medium risk, low risk, burn rate, or budget health of a SPECIFIC subsystem.
If not finance related or out of scope, tool = none.
Extract the subsystem ID number directly from the query (e.g. 'subsystem 17' -> 17).
If a subsystem ID is required (e.g. for subsystem_cost, cost_breakdown, budget_comparison, overrun_risk, financial_summary) but no subsystem ID is specified in the query, you MUST set tool = "none" (as it is ambiguous which subsystem is requested). For system_analytics, default subsystem_id to 1.
Query: {query}
"""
    response = get_llm().invoke(prompt)
    if hasattr(response, "content"):
        # LangChain Chat models return an AIMessage object
        response = response.content
    elif isinstance(response, str):
        # Ollama returns a raw string
        pass
    else:
        response = str(response)
        
    response = response.strip()
    decision = extract_json(response)
    
    # BULLETPROOF FALLBACK: If Llama3 hallucinates and fails to output JSON, assume it's out of scope!
    if not decision:
        decision = {"tool": "none", "subsystem_id": 1}
        
    # Deterministic Planner Override for Aggregates and Comparisons
    q_lower = query.lower()
    subsystem_ids = [int(x) for x in re.findall(r'subsystem\s+(\d+)', query, re.IGNORECASE)]
    words = q_lower.split()
    
    if (any(word in words for word in ["average", "total", "sum", "mean", "all", "count", "bottom", "top", "most", "least"]) or
        "severe overruns" in q_lower or
        len(subsystem_ids) >= 2 or "compare" in q_lower or
        (("which" in q_lower or "find" in q_lower) and len(subsystem_ids) == 0)):
        decision["tool"] = "system_analytics"
        if "subsystem_id" not in decision or decision["subsystem_id"] is None:
            decision["subsystem_id"] = 1
    elif "summary" in q_lower and len(subsystem_ids) == 1:
        decision["tool"] = "financial_summary"
        decision["subsystem_id"] = subsystem_ids[0]
            
    return decision
