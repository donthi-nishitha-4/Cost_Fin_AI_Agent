import os
import sys
import re

# Add the project root to the python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langsmith import Client # type: ignore
from app.services.finance_service import (
    get_cost_breakdown_from_db,
    get_budget_comparison_from_db,
    get_overrun_risk_from_db,
    get_financial_summary
)
from app.core.database import get_db
from app.models.finance_db_models import FinanceSubsystem
from app.core.response_formatter import (
    format_cost_breakdown_answer,
    format_budget_comparison_answer,
    format_overrun_risk_answer,
    format_financial_summary_answer
)

load_dotenv()

SOURCE_DATASET_NAME = "Cost_Finance_Golden"
STRICT_DATASET_NAME = "Cost_Finance_Golden_Strict"

INTENT_PATTERNS = {
    "aggregation": ["largest", "highest", "lowest", "percentage", "compare", "summary", "which subsystem", "find", "total", "average", "count", "rank", "top", "bottom", "heavy", "most", "least", "how many"],
    "risk": ["risk", "overrun"],
    "remaining_budget": ["remaining budget", "remaining funds"],
    "cost_breakdown": ["cost breakdown"],
    "budget_status": ["over budget", "under budget", "budget status"],
    "variance": ["variance"],
    "equipment_cost": ["equipment cost", "equipment"],
    "labor_cost": ["labor cost", "labor"],
    "material_cost": ["material cost", "material"]
}

def get_intent(query: str) -> str:
    query = query.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        if any(p in query for p in patterns):
            return intent
    return "unknown"

client = Client()

def generate_golden_dataset_strict():
    if not client.has_dataset(dataset_name=SOURCE_DATASET_NAME):
        print(f"Error: Source dataset '{SOURCE_DATASET_NAME}' not found.")
        return

    if client.has_dataset(dataset_name=STRICT_DATASET_NAME):
        print(f"Updating existing dataset: '{STRICT_DATASET_NAME}' (Preserving experiment history)...")
        strict_dataset = client.read_dataset(dataset_name=STRICT_DATASET_NAME)
        strict_examples = list(client.list_examples(dataset_id=strict_dataset.id))
        existing_map = {ex.inputs["query"]: ex.id for ex in strict_examples}
    else:
        print(f"Creating new dataset: '{STRICT_DATASET_NAME}'")
        strict_dataset = client.create_dataset(
            dataset_name=STRICT_DATASET_NAME,
            description="Golden deterministic dataset generated STRICTLY bypassing LLMs"
        )
        existing_map = {}

    source_dataset = client.read_dataset(dataset_name=SOURCE_DATASET_NAME)
    examples = list(client.list_examples(dataset_id=source_dataset.id))
    
    NEW_QUERIES = [
        "What is the total planned cost of all subsystems?",
        "What is the total actual cost of all subsystems?",
        "What is the average planned cost?",
        "What is the average variance?",
        "What is the average equipment cost?",
        "How many subsystems are over budget?",
        "How many subsystems are under budget?",
        "What are the top 5 overruns?",
        "What are the bottom 5 variances?",
        "Which subsystem spent more, subsystem 15 or subsystem 42?",
        "Which has larger variance, subsystem 10 or subsystem 20?",
        "Which is more over budget, subsystem 12 or subsystem 19?",
        "Compare subsystem 15 and subsystem 42.",
        "What is the budget health of subsystem 12?",
        "What is the expenditure of subsystem 15?",
        "What is the burn rate of subsystem 8?",
        "What is the unused budget of subsystem 11?",
        "Has subsystem 10 overspent its allocation?",
        "What is the remaining funds for subsystem 25?",
        "Show subsystem cost.",
        "Compare two subsystems.",
        "Give planned cost, actual cost and labor breakdown for subsystem 18.",
        "Which subsystem has highest planned cost and is also over budget?",
        "Show subsystem 12 summary and compare it with subsystem 19."
    ]

    all_examples_to_process = []
    for ex in examples:
        all_examples_to_process.append({
            "query": ex.inputs["query"],
            "original_expected": ex.outputs.get("expected", "")
        })

    for q in NEW_QUERIES:
        if not any(item["query"] == q for item in all_examples_to_process):
            all_examples_to_process.append({
                "query": q,
                "original_expected": ""
            })

    total = len(all_examples_to_process)
    print(f"Total examples to process (including seeds): {total}\n")

    db_gen = get_db()
    db = next(db_gen)
    try:
        all_subsystems = db.query(FinanceSubsystem).all()
    finally:
        db.close()

    csv_rows = []
    for i, item in enumerate(all_examples_to_process, start=1):
        query = item["query"]
        original_expected = item["original_expected"]
        q_lower = query.lower()
        
        # Determine subsystem IDs deterministically via regex
        subsystem_ids = [int(x) for x in re.findall(r'subsystem\s+(\d+)', query, re.IGNORECASE)]
        subsystem_id = subsystem_ids[0] if subsystem_ids else None
        
        # Force aggregation intent for multi-subsystem, comparison, or average variance queries
        if len(subsystem_ids) >= 2 or "compare" in q_lower or "more over budget" in q_lower or "larger variance" in q_lower or "spent more" in q_lower or "average variance" in q_lower or "how many" in q_lower:
            intent = "aggregation"
        else:
            intent = get_intent(query)
            
        strict_expected = None

        # Specific synonym / multi-intent overrides
        if "expenditure" in q_lower and subsystem_id is not None:
            sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
            if sub:
                strict_expected = f"Actual cost for Subsystem {sub.id} is {sub.actual_cost}."
        elif "burn rate" in q_lower and subsystem_id is not None:
            sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
            if sub and sub.planned_cost > 0:
                pct = round((sub.actual_cost / sub.planned_cost) * 100, 2)
                strict_expected = f"Subsystem {sub.id} has consumed {pct}% of its planned cost."
        elif ("unused budget" in q_lower or "remaining funds" in q_lower) and subsystem_id is not None:
            sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
            if sub:
                rem = sub.planned_cost - sub.actual_cost
                strict_expected = f"Remaining budget for Subsystem {sub.id} is {rem}."
        elif "budget health" in q_lower and subsystem_id is not None:
            data = get_overrun_risk_from_db(subsystem_id)
            if data:
                strict_expected = f"Subsystem {subsystem_id} is {data['risk_level']} overrun risk because it has used {data['utilization_percent']}% of its planned budget."
        elif "overspent" in q_lower and subsystem_id is not None:
            sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
            if sub:
                overspent = sub.actual_cost > sub.planned_cost
                yes_no = "Yes" if overspent else "No"
                diff = abs(sub.actual_cost - sub.planned_cost)
                strict_expected = f"{yes_no}. Subsystem {sub.id} is {'over' if overspent else 'under'} budget by {diff}."
        elif "labor breakdown" in q_lower and ("planned" in q_lower or "actual" in q_lower) and subsystem_id is not None:
            sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
            if sub:
                strict_expected = f"Subsystem {sub.id} has planned cost {sub.planned_cost}, actual cost {sub.actual_cost}, labor cost {sub.labor_cost}, material cost {sub.material_cost}, equipment cost {sub.equipment_cost}."

        if strict_expected is not None:
            pass
        elif intent == "unknown" and ("subsystem" in q_lower or "compare" in q_lower or "summary" in q_lower or "breakdown" in q_lower or "cost" in q_lower) and subsystem_id is None:
            strict_expected = "Please specify which subsystem you are asking about."

        elif intent == "aggregation":
            if "percentage" in q_lower and ("consumed" in q_lower or "used" in q_lower) and subsystem_id is not None:
                sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
                if sub and sub.planned_cost > 0:
                    pct = round((sub.actual_cost / sub.planned_cost) * 100, 2)
                    strict_expected = f"Subsystem {sub.id} has consumed {pct}% of its planned cost."
            elif "labor-heavy" in q_lower:
                sub = max(all_subsystems, key=lambda s: s.labor_cost / (s.labor_cost + s.material_cost + s.equipment_cost + 1e-9))
                strict_expected = f"Subsystem {sub.id} is labor-heavy."
            elif "material-heavy" in q_lower:
                sub = max(all_subsystems, key=lambda s: s.material_cost / (s.labor_cost + s.material_cost + s.equipment_cost + 1e-9))
                strict_expected = f"Subsystem {sub.id} is material-heavy."
            elif "equipment-heavy" in q_lower:
                sub = max(all_subsystems, key=lambda s: s.equipment_cost / (s.labor_cost + s.material_cost + s.equipment_cost + 1e-9))
                strict_expected = f"Subsystem {sub.id} is equipment-heavy."
            elif "lowest non-zero planned budget" in q_lower or "lowest non-zero planned cost" in q_lower:
                sub = min([s for s in all_subsystems if s.planned_cost > 0], key=lambda s: s.planned_cost)
                strict_expected = f"Subsystem {sub.id} has the lowest non-zero planned cost of {sub.planned_cost}, with an actual cost of {sub.actual_cost}."
            elif "largest underspend" in q_lower or "maximum positive variance" in q_lower:
                sub = max(all_subsystems, key=lambda s: s.planned_cost - s.actual_cost)
                strict_expected = f"Subsystem {sub.id} has the largest underspend."
            elif "zero planned budget" in q_lower:
                sub = next((s for s in all_subsystems if s.planned_cost == 0), None)
                if sub:
                    strict_expected = f"Subsystem {sub.id} has a zero planned budget."
            elif "total planned cost" in q_lower:
                total_planned = sum(s.planned_cost for s in all_subsystems)
                strict_expected = f"Total planned cost of all subsystems is ${round(total_planned, 2)}."
            elif "total actual cost" in q_lower:
                total_actual = sum(s.actual_cost for s in all_subsystems)
                strict_expected = f"Total actual cost of all subsystems is ${round(total_actual, 2)}."
            elif "average planned cost" in q_lower:
                avg_planned = sum(s.planned_cost for s in all_subsystems) / len(all_subsystems)
                strict_expected = f"Average planned cost of subsystems is ${round(avg_planned, 2)}."
            elif "average variance" in q_lower:
                avg_var = sum(s.planned_cost - s.actual_cost for s in all_subsystems) / len(all_subsystems)
                strict_expected = f"Average variance is ${round(avg_var, 2)}."
            elif "average equipment cost" in q_lower:
                avg_equip = sum(s.equipment_cost for s in all_subsystems) / len(all_subsystems)
                strict_expected = f"Average equipment cost of subsystems is ${round(avg_equip, 2)}."
            elif "how many" in q_lower and "over budget" in q_lower:
                cnt = sum(1 for s in all_subsystems if s.actual_cost > s.planned_cost)
                strict_expected = f"There are {cnt} subsystems over budget."
            elif "how many" in q_lower and "under budget" in q_lower:
                cnt = sum(1 for s in all_subsystems if s.actual_cost <= s.planned_cost)
                strict_expected = f"There are {cnt} subsystems under budget."
            elif "top 5 overrun" in q_lower:
                overruns = sorted([s for s in all_subsystems if s.actual_cost > s.planned_cost], key=lambda s: s.actual_cost - s.planned_cost, reverse=True)[:5]
                list_str = ", ".join([f"Subsystem {s.id} (overrun of ${round(s.actual_cost - s.planned_cost, 2)})" for s in overruns])
                strict_expected = f"Top 5 overruns: {list_str}."
            elif "bottom 5 variance" in q_lower:
                variances = sorted(all_subsystems, key=lambda s: s.planned_cost - s.actual_cost)[:5]
                list_str = ", ".join([f"Subsystem {s.id} (variance of ${round(s.planned_cost - s.actual_cost, 2)})" for s in variances])
                strict_expected = f"Bottom 5 variances: {list_str}."
            elif "spent more" in q_lower and len(subsystem_ids) >= 2:
                sub1 = next((s for s in all_subsystems if s.id == subsystem_ids[0]), None)
                sub2 = next((s for s in all_subsystems if s.id == subsystem_ids[1]), None)
                if sub1 and sub2:
                    winner = sub1 if sub1.actual_cost > sub2.actual_cost else sub2
                    strict_expected = f"Subsystem {winner.id} spent more."
            elif "larger variance" in q_lower and len(subsystem_ids) >= 2:
                sub1 = next((s for s in all_subsystems if s.id == subsystem_ids[0]), None)
                sub2 = next((s for s in all_subsystems if s.id == subsystem_ids[1]), None)
                if sub1 and sub2:
                    var1 = abs(sub1.planned_cost - sub1.actual_cost)
                    var2 = abs(sub2.planned_cost - sub2.actual_cost)
                    winner = sub1 if var1 > var2 else sub2
                    strict_expected = f"Subsystem {winner.id} has the larger variance."
            elif "more over budget" in q_lower and len(subsystem_ids) >= 2:
                sub1 = next((s for s in all_subsystems if s.id == subsystem_ids[0]), None)
                sub2 = next((s for s in all_subsystems if s.id == subsystem_ids[1]), None)
                if sub1 and sub2:
                    over1 = max(0.0, sub1.actual_cost - sub1.planned_cost)
                    over2 = max(0.0, sub2.actual_cost - sub2.planned_cost)
                    winner = sub1 if over1 > over2 else sub2
                    strict_expected = f"Subsystem {winner.id} is more over budget."
            elif "compare" in q_lower and len(subsystem_ids) >= 2:
                sub1 = next((s for s in all_subsystems if s.id == subsystem_ids[0]), None)
                sub2 = next((s for s in all_subsystems if s.id == subsystem_ids[1]), None)
                if sub1 and sub2:
                    strict_expected = f"Comparing Subsystem {sub1.id} (planned: {sub1.planned_cost}, actual: {sub1.actual_cost}) and Subsystem {sub2.id} (planned: {sub2.planned_cost}, actual: {sub2.actual_cost})."
            elif "severe overrun" in q_lower:
                overruns = sorted([s for s in all_subsystems if s.actual_cost > 1.3 * s.planned_cost], key=lambda s: s.id)
                list_str = ", ".join([str(s.id) for s in overruns])
                strict_expected = f"There are {len(overruns)} subsystems with severe overruns: {list_str}."
            elif "exactly equal" in q_lower:
                sub = next((s for s in all_subsystems if s.planned_cost == s.actual_cost), None)
                if sub:
                    strict_expected = f"Subsystem {sub.id} has planned cost exactly equal to actual cost: both are {sub.planned_cost}."
            elif "highest planned cost" in q_lower and "over budget" in q_lower:
                over_budget = [s for s in all_subsystems if s.actual_cost > s.planned_cost]
                if over_budget:
                    sub = max(over_budget, key=lambda s: s.planned_cost)
                    strict_expected = f"Subsystem {sub.id} has the highest planned cost among over-budget subsystems."

            if not strict_expected and "highest planned cost" in q_lower:
                sub = max(all_subsystems, key=lambda s: s.planned_cost)
                strict_expected = f"Subsystem {sub.id} has the highest planned cost."

        elif intent == "remaining_budget" and subsystem_id is not None:
            sub = next((s for s in all_subsystems if s.id == subsystem_id), None)
            if sub:
                rem = sub.planned_cost - sub.actual_cost
                strict_expected = f"Remaining budget for Subsystem {sub.id} is {rem}."

        elif intent == "risk" and subsystem_id is not None:
            data = get_overrun_risk_from_db(subsystem_id)
            if data:
                if "low risk" in q_lower or "high risk" in q_lower or "medium risk" in q_lower or "is subsystem" in q_lower or "is it" in q_lower:
                    risk_level = data['risk_level']
                    asked_level = "low" if "low risk" in q_lower else ("medium" if "medium risk" in q_lower else "high")
                    is_correct = (risk_level == asked_level)
                    yes_no = "Yes" if is_correct else "No"
                    strict_expected = f"{yes_no}. Subsystem {subsystem_id} is {risk_level} overrun risk because it has used {data['utilization_percent']}% of its planned budget."
                else:
                    strict_expected = f"Subsystem {subsystem_id} is {data['risk_level']} overrun risk because it has used {data['utilization_percent']}% of its planned budget."

        elif intent == "unknown":
            strict_expected = "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."

        elif subsystem_id is not None:
            try:
                if intent in ["cost_breakdown", "equipment_cost", "labor_cost", "material_cost"]:
                    data = get_cost_breakdown_from_db(subsystem_id)
                    strict_expected = format_cost_breakdown_answer(data)
                elif intent in ["budget_status", "variance"]:
                    data = get_budget_comparison_from_db(subsystem_id)
                    if intent == "variance" or "variance" in q_lower:
                        strict_expected = f"Variance for Subsystem {subsystem_id} is {data['variance']} between planned cost {data['planned_cost']} and actual cost {data['actual_cost']}."
                    else:
                        strict_expected = format_budget_comparison_answer(data)
                elif intent == "summary" or "summary" in q_lower:
                    data = get_financial_summary(subsystem_id)
                    strict_expected = format_financial_summary_answer(data)
                else:
                    data = get_financial_summary(subsystem_id)
                    strict_expected = format_financial_summary_answer(data)
            except Exception as e:
                strict_expected = f"Error processing {subsystem_id}: {str(e)}"
                
        if not strict_expected:
            strict_expected = original_expected if original_expected else "Out of scope"
        
        if query in existing_map:
            client.update_example(
                example_id=existing_map[query],
                outputs={"expected": strict_expected},
            )
        
        csv_rows.append((query, strict_expected, '["base"]'))

    import csv
    csv_path = "app/data/golden_dataset_strict_v5_local.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "expected", "splits"])
        writer.writerows(csv_rows)
        
    print(f"Successfully saved strict golden dataset locally to {csv_path}!")
    print(f"\nSuccessfully generated STRICT Golden Dataset '{STRICT_DATASET_NAME}' with {total} examples!")

if __name__ == "__main__":
    generate_golden_dataset_strict()
