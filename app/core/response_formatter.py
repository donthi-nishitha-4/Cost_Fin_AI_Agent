from app.core.llm_factory import get_llm

def format_agent_response(agent_result: dict):
    if agent_result.get("status") != "success":
        return agent_result

    tool = agent_result.get("tool")
    data = agent_result.get("data", {})
    subsystem_id = agent_result.get("subsystem_id")

    if subsystem_id is not None and "subsystem" in data:
        if not str(data["subsystem"]).startswith("Subsystem"):
            data["subsystem"] = f"Subsystem {subsystem_id} ({data['subsystem']})"

    answer = build_answer(tool, data)

    return {
        **agent_result,
        "answer": answer
    }


def build_answer(tool: str, data: dict):
    if tool == "subsystem_cost":
        return format_subsystem_cost_answer(data)

    if tool == "cost_breakdown":
        return format_cost_breakdown_answer(data)

    if tool == "budget_comparison":
        return format_budget_comparison_answer(data)

    if tool == "overrun_risk":
        return format_overrun_risk_answer(data)

    if tool == "financial_summary":
        return format_financial_summary_answer(data)

    if tool == "system_analytics":
        return format_system_analytics_answer(data)


    if tool == "none":
        return "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."

    return "I could not format the finance response."


def format_subsystem_cost_answer(data: dict):
    return (
        f"{data['subsystem']} has a planned cost of {data['planned_cost']}, "
        f"actual cost of {data['actual_cost']}, and remaining budget of "
        f"{data['remaining_budget']}."
    )


def format_cost_breakdown_answer(data: dict):
    return (
        f"{data['subsystem']} cost breakdown is labor {data['labor_cost']}, "
        f"material {data['material_cost']}, and equipment {data['equipment_cost']}."
    )


def format_budget_comparison_answer(data: dict):
    return (
        f"{data['subsystem']} is {data['budget_status']} with a variance of "
        f"{data['variance']} between planned cost {data['planned_cost']} and "
        f"actual cost {data['actual_cost']}."
    )


def format_overrun_risk_answer(data: dict):
    return (
        f"{data['subsystem']} has used {data['utilization_percent']}% of planned "
        f"cost and has {data['risk_level']} overrun risk."
    )


def format_financial_summary_answer(data: dict):
    cost = data["cost"]
    budget = data["budget_comparison"]
    risk = data["overrun_risk"]

    return (
        f"{data['subsystem']} has planned cost {cost['planned_cost']}, actual cost "
        f"{cost['actual_cost']}, and remaining budget {cost['remaining_budget']}. "
        f"It is {budget['budget_status']} by {budget['variance']} and has used "
        f"{risk['utilization_percent']}% of planned cost, giving it "
        f"{risk['risk_level']} overrun risk."
    )

def format_system_analytics_answer(data: dict):
    if "error" in data:
        return f"Sorry, the database query failed: {data['error']}"
        
    query = data.get("query")
    result = data.get("result", [])
    
    if not result:
        return f"No results found for your query: {query}"
        
    prompt = (
        f"The user asked: '{query}'. The database returned this raw JSON data: {result}.\n"
        "Write a concise, human-readable response (can be multiple sentences or a list if there are multiple items) answering the user's question using this data.\n"
        "CRITICAL RULES:\n"
        "1. You MUST list ALL subsystems and details returned in the database results. Do not omit or summarize any subsystems.\n"
        "2. You MUST explicitly mention the subsystem ID (prefixed with the word 'Subsystem', e.g., 'Subsystem X') for every subsystem in the answer if the ID is available in the data.\n"
        "3. You MUST explicitly include all relevant numeric cost values, planned budgets, and calculated metrics from the database results in your answer. Do not round off or skip any numbers. (This does NOT apply if the query only asks to find, list, or identify subsystems matching a condition without asking for their specific costs, in which case you should only list their names and IDs).\n"
        "4. If there are multiple subsystems in the results (e.g. more than 3), format the response as a concise list or comma-separated string containing the subsystem ID (e.g., 'Subsystem X') and its main metric. Do NOT write long explanatory paragraphs or detailed breakdowns for each subsystem, so that the answer is compact and lists every subsystem without truncation.\n"
        "5. Do not mention 'The database returned' or show the raw JSON format."
    )
    
    response = get_llm().invoke(prompt)
    if hasattr(response, "content"):
        response = response.content
    elif isinstance(response, str):
        pass
    else:
        response = str(response)
        
    return response.strip()
