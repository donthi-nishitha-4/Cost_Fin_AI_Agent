import json
import re
from langchain_ollama import OllamaLLM

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
  "tool": "cost_breakdown or subsystem_cost or budget_comparison or overrun_risk or none",
  "subsystem_id": 1
}}

Use subsystem_cost for cost, planned cost, actual cost, or remaining budget.
Use cost_breakdown for labor, material, equipment, or breakdown questions.
Use budget_comparison for over budget, under budget, variance, planned vs actual questions.
Use overrun_risk for risk, overrun risk, high risk, medium risk, or low risk questions.
If not finance related, tool = none.

Query: {query}
"""

    response = llm.invoke(prompt).strip()

    return extract_json(response)