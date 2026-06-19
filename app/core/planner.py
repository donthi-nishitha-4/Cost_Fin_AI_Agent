import json
import re

from langchain_ollama import OllamaLLM  # type: ignore

llm = OllamaLLM(model="llama3")


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
Use system_analytics for system-wide aggregate questions.
Use financial_summary for full summary, complete summary of a SPECIFIC subsystem.
Use subsystem_cost for total cost, planned cost, actual cost, or remaining budget of a SPECIFIC subsystem.
Use cost_breakdown for SPECIFIC components like labor cost, material cost, equipment cost, or breakdown of a SPECIFIC subsystem.
Use budget_comparison for over budget, under budget, variance of a SPECIFIC subsystem.
Use overrun_risk for overrun risk, high risk, medium risk, or low risk of a SPECIFIC subsystem.
If not finance related or out of scope, tool = none.
Extract the subsystem ID number directly from the query (e.g. 'subsystem 17' -> 17).
If no subsystem ID is specified or you are using system_analytics, default to 1.
Query: {query}
"""
    response = llm.invoke(prompt).strip()
    decision = extract_json(response)
    
    # BULLETPROOF FALLBACK: If Llama3 hallucinates and fails to output JSON, assume it's out of scope!
    if not decision:
        return {"tool": "none", "subsystem_id": 1}
        
    return decision
