def format_agent_response(agent_result: dict):
    if agent_result.get("status") != "success":
        return agent_result

    tool = agent_result.get("tool")
    data = agent_result.get("data", {})

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

    if tool == "none":
        return "Please ask a finance-related question about subsystem cost, budget, breakdown, risk, or summary."

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