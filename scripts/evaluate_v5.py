import os
import re
import math
import sys

# Add the project root to the python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langsmith import Client # type: ignore
from langsmith.evaluation import evaluate # type: ignore
from app.core.llm_factory import get_llm

load_dotenv()

from app.agents.finance_agent_v2 import ask_finance_agent_v2

client = Client()
DATASET_NAME = "Cost_Finance_Golden_Strict"

# Global LLM to avoid reallocation overhead
JUDGE_LLM = get_llm()

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

REQUIRED_FIELDS = {
    "cost_breakdown": ["labor", "material", "equipment"],
    "budget_status": ["status", "variance"],
    "variance": ["variance"],
    "equipment_cost": ["equipment"],
    "labor_cost": ["labor"],
    "material_cost": ["material"]
}

def agent_target(inputs: dict) -> dict:
    import time
    # Sleep to respect Groq rate limits for llama-3.3-70b-versatile (30 RPM)
    #time.sleep(5.5)
    query = inputs["query"]
    result = ask_finance_agent_v2(query)
    return {"result": result.get("answer", str(result))}

def get_intent(query: str) -> str:
    query = query.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        if any(p in query for p in patterns):
            return intent
    return "unknown"

def extract_field_number(text: str, keyword: str):
    # Scrub subsystem IDs to prevent the regex from accidentally extracting '79' instead of the cost
    safe_text = re.sub(r'subsystem\s+\d+', 'subsystem X', text, flags=re.IGNORECASE)
    # Scrub parentheses content (which often contains subsystem names with zone/sector numbers)
    safe_text = re.sub(r'\(.*?\)', '', safe_text)
    # Scrub any words with digits that aren't standalone numbers (like 'Zone 7' -> 'Zone')
    safe_text = re.sub(r'\b[a-zA-Z]+\s+\d+\b(?!\.)', '', safe_text)
    
    # Regex explicitly captures an optional sign followed by digits and decimals.
    pattern = rf'{keyword}[^\d+-]*([-+]?\d[\d,]*\.?\d*)'
    match = re.search(pattern, safe_text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1).replace(',', ''))
        except:
            return None
    return None

def extract_status(text: str):
    t = text.lower()
    if "not applicable" in t: return "not applicable"
    if "over budget" in t or "over_budget" in t: return "over budget"
    if "under budget" in t or "under_budget" in t: return "under budget"
    return None

def extract_all_numbers(text):
    text = text.replace('$', '').replace(',', '')
    matches = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', text)
    return [float(m) for m in matches]

def v5_hybrid_evaluator(run, example):
    expected = str(example.outputs.get("expected", ""))
    actual = str(run.outputs.get("result", ""))
    query = str(example.inputs.get("query", ""))
    
    # LAYER 1: Intent Classification
    q_lower = query.lower()
    subsystem_ids = [int(x) for x in re.findall(r'subsystem\s+(\d+)', query, re.IGNORECASE)]
    if len(subsystem_ids) >= 2 or "compare" in q_lower or "more over budget" in q_lower or "larger variance" in q_lower or "spent more" in q_lower or "average variance" in q_lower or "how many" in q_lower:
        intent = "aggregation"
    else:
        intent = get_intent(query)
    
    severity = "PASS"
    math_score = 1
    comment_log = []

    # LAYER 2 & 3: Extraction & Numeric Validation
    subsystem_match = re.search(r'subsystem\s+(\d+)', expected, re.IGNORECASE)
    expected_sub_id = float(subsystem_match.group(1)) if subsystem_match else None
    
    act_subsystem_match = re.search(r'subsystem\s+(\d+)', actual, re.IGNORECASE)
    actual_sub_id = float(act_subsystem_match.group(1)) if act_subsystem_match else None

    if expected_sub_id is not None:
        if actual_sub_id is None:
            severity = "WARNING"
            comment_log.append("WARNING: Missing subsystem ID.")
        elif not math.isclose(expected_sub_id, actual_sub_id, rel_tol=0.001, abs_tol=0.01):
            if intent in ["aggregation", "comparison"] and str(int(expected_sub_id)) in actual:
                pass
            else:
                severity = "FAIL"
                math_score = 0
                comment_log.append(f"FAIL: Wrong subsystem ID. Expected {expected_sub_id}, got {actual_sub_id}.")

    # Field-Specific Validation
    if math_score == 1 and intent in REQUIRED_FIELDS:
        fields_to_check = REQUIRED_FIELDS[intent]
        for field in fields_to_check:
            if field == "status":
                exp_stat = extract_status(expected)
                act_stat = extract_status(actual)
                if exp_stat != act_stat:
                    
                    # LAYER 4: Business Logic
                    if exp_stat == "not applicable" and act_stat in ["over budget", "under budget"]:
                        severity = "CRITICAL"
                        math_score = 0
                        comment_log.append(f"CRITICAL: Business logic contradiction. Expected {exp_stat}, got {act_stat}.")
                    else:
                        severity = "CRITICAL"
                        math_score = 0
                        comment_log.append(f"CRITICAL: Wrong budget status. Expected {exp_stat}, got {act_stat}.")
            else:
                exp_val = extract_field_number(expected, field)
                act_val = extract_field_number(actual, field)
                
                if exp_val is not None:
                    if act_val is None:
                        severity = "FAIL"
                        math_score = 0
                        comment_log.append(f"FAIL: Missing required field '{field}'. Expected {exp_val}.")
                    elif not math.isclose(exp_val, act_val, rel_tol=0.001, abs_tol=0.01):
                        # Catch sign reversals!
                        if math.isclose(abs(exp_val), abs(act_val), rel_tol=0.001, abs_tol=0.01) and exp_val != act_val:
                            severity = "CRITICAL"
                            math_score = 0
                            comment_log.append(f"CRITICAL: Sign reversal on '{field}'. Expected {exp_val}, got {act_val}.")
                        else:
                            severity = "FAIL"
                            math_score = 0
                            comment_log.append(f"FAIL: Wrong numeric value for '{field}'. Expected {exp_val}, got {act_val}.")

    # Fallback to general numeric matching if intent is generic (aggregation, unknown)
    elif math_score == 1:
        exp_nums = extract_all_numbers(expected)
        act_nums = extract_all_numbers(actual)
        if intent not in ["aggregation", "comparison"]:
            if expected_sub_id is not None and expected_sub_id in exp_nums:
                exp_nums = [x for x in exp_nums if x != expected_sub_id]
            if actual_sub_id is not None and actual_sub_id in act_nums:
                act_nums = [x for x in act_nums if x != actual_sub_id]
            
        for en in exp_nums:
            found = any(math.isclose(abs(en), abs(an), rel_tol=0.001, abs_tol=0.01) for an in act_nums)
            if not found:
                severity = "FAIL"
                math_score = 0
                comment_log.append(f"FAIL: Missing expected generic number: {en}")

    if severity == "PASS":
        comment_log.append("INFO: Perfect match.")

    final_comment = " | ".join(comment_log)

    # LAYER 5: Semantic Validation
    prompt = f"""Math has already been validated.
Check only:
1. Does the ACTUAL answer express the same business conclusion as EXPECTED?
2. Is the answer complete?
3. Is the answer understandable?
Ignore all numbers.
Return EXACTLY 'CORRECT' or 'INCORRECT'

EXPECTED: {expected}
ACTUAL: {actual}
Verdict:"""

    response = JUDGE_LLM.invoke(prompt)
    if hasattr(response, "content"):
        verdict = response.content.strip().upper()
    else:
        verdict = str(response).strip().upper()
    semantic_score = 1 if verdict.startswith("CORRECT") else 0

    return [
        {"key": "v5_math_score", "score": math_score, "comment": final_comment},
        {"key": "v5_semantic_score", "score": semantic_score, "comment": verdict},
        {"key": "v5_severity_level", "score": 1 if severity == "PASS" else 0, "comment": severity},
        {"key": "v5_intent", "score": 1, "comment": intent}
    ]

def main():
    if not client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset {DATASET_NAME} not found.")
        return
        
    print("Starting V5 Project-Grade Evaluation...")
    
    results = evaluate(
        agent_target,
        data=DATASET_NAME,
        evaluators=[v5_hybrid_evaluator],
        experiment_prefix="V5_Strict_Golden",
        max_concurrency=1,
    )
    print("\nEvaluation complete!")

if __name__ == "__main__":
    main()
