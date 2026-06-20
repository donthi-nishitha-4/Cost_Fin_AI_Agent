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
    "cost_breakdown": ["cost breakdown"],
    "budget_status": ["over budget", "under budget", "budget status", "is subsystem"],
    "variance": ["variance"],
    "equipment_cost": ["equipment cost"],
    "labor_cost": ["labor cost"],
    "material_cost": ["material cost"],
    "aggregation": ["largest", "highest", "lowest", "percentage", "compare", "summary", "which subsystem", "find"]
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
        print(f"Deleting existing '{STRICT_DATASET_NAME}' dataset...")
        client.delete_dataset(dataset_name=STRICT_DATASET_NAME)

    print(f"Creating new dataset: '{STRICT_DATASET_NAME}'")
    strict_dataset = client.create_dataset(
        dataset_name=STRICT_DATASET_NAME,
        description="Golden deterministic dataset generated STRICTLY bypassing LLMs"
    )

    source_dataset = client.read_dataset(dataset_name=SOURCE_DATASET_NAME)
    examples = list(client.list_examples(dataset_id=source_dataset.id))
    
    total = len(examples)
    print(f"Found {total} examples in source dataset. Generating STRICT expected answers...\n")

    for i, ex in enumerate(examples, start=1):
        query = ex.inputs["query"]
        original_expected = ex.outputs["expected"]
        
        intent = get_intent(query)
        
        # Determine subsystem ID deterministically via regex
        subsystem_match = re.search(r'subsystem\s+(\d+)', query, re.IGNORECASE)
        subsystem_id = int(subsystem_match.group(1)) if subsystem_match else None
        
        strict_expected = None

        if intent == "aggregation":
            # Retain LLM output for SQL Text-to-SQL logic
            strict_expected = original_expected
            
        elif intent == "unknown":
            # Out of scope fallback
            strict_expected = "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."
            
        elif subsystem_id is not None:
            # Deterministic Math Execution bypassing LLM completely
            try:
                if intent in ["cost_breakdown", "equipment_cost", "labor_cost", "material_cost"]:
                    data = get_cost_breakdown_from_db(subsystem_id)
                    strict_expected = format_cost_breakdown_answer(data)
                elif intent in ["budget_status", "variance"]:
                    data = get_budget_comparison_from_db(subsystem_id)
                    strict_expected = format_budget_comparison_answer(data)
                elif intent == "risk":
                    data = get_overrun_risk_from_db(subsystem_id)
                    strict_expected = format_overrun_risk_answer(data)
                elif intent == "summary":
                    data = get_financial_summary(subsystem_id)
                    strict_expected = format_financial_summary_answer(data)
                else:
                    # Generic Subsystem queries fall back to financial summary
                    data = get_financial_summary(subsystem_id)
                    strict_expected = format_financial_summary_answer(data)
            except Exception as e:
                strict_expected = f"Error processing {subsystem_id}: {str(e)}"
                
        if not strict_expected:
            strict_expected = original_expected
        
        client.create_example(
            inputs={"query": query},
            outputs={"expected": strict_expected},
            dataset_id=strict_dataset.id,
        )

    print(f"\nSuccessfully generated STRICT Golden Dataset '{STRICT_DATASET_NAME}' with {total} examples!")

if __name__ == "__main__":
    generate_golden_dataset_strict()
