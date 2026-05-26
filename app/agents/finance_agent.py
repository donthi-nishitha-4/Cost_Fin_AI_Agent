import json
import re
from langchain_ollama import OllamaLLM
from app.tools.finance_tools import TOOLS

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


def ask_finance_agent(query: str):

    print("QUERY:", query)

    prompt = f"""
You are a finance AI agent.

Return ONLY JSON:
{{
  "tool": "subsystem_cost or cost_breakdown or none",
  "subsystem_id": 1
}}

User query: {query}
"""

    response = llm.invoke(prompt).strip()

    print("RAW LLM:", response)

    # SAFE PARSING
    decision = extract_json(response)

    # 🔥 CRITICAL FIX (this prevents crash)
    if not decision:
        return {
            "status": "error",
            "message": "Failed to parse LLM response",
            "raw": response
        }

    print("TOOL DECISION:", decision)

    tool = decision.get("tool")

    if tool in TOOLS:
        return TOOLS[tool](decision.get("subsystem_id"))

    return {
    "status": "success",
    "tool": "none",
    "message": "I can help only with finance subsystem queries. Try asking about cost or breakdown.",
    "query": query
}