from langchain_ollama import OllamaLLM

from app.tools.finance_tools import get_subsystem_cost_tool


# ----------------------------
# LLM INIT
# ----------------------------
llm = OllamaLLM(model="llama3")


# ----------------------------
# AGENT FUNCTION
# ----------------------------
def ask_finance_agent(query: str):
    """
    LLM-driven finance agent (Phase 2 upgrade)
    """

    # STEP 1: Ask LLM to extract intent / subsystem id
    prompt = f"""
You are a finance assistant for a construction cost system.

You have ONE tool:
- SubsystemCostTool: returns cost details for a subsystem ID

Task:
- If query is about subsystem cost, extract ONLY the subsystem ID (integer).
- If not related or unclear, return INVALID.

Rules:
- Output ONLY number or INVALID
- No explanation
- No extra text

User query: {query}
"""

    response = llm.invoke(prompt).strip()

    print("LLM RESPONSE:", response)  # DEBUG LINE (important)

    # STEP 2: If valid ID → call tool
    if response.isdigit():
        return get_subsystem_cost_tool(response)

    # STEP 3: fallback
    return {
        "status": "error",
        "message": "Could not understand query. Ask like: 'cost of subsystem 1'"
    }