import os
import re
from dotenv import load_dotenv
from langsmith import Client # type: ignore
from langsmith.evaluation import evaluate # type: ignore
from langchain_ollama import OllamaLLM # type: ignore

load_dotenv()

from app.agents.finance_agent_v2 import ask_finance_agent_v2

client = Client()
DATASET_NAME = "Cost_Finance_Evaluation"

def agent_target(inputs: dict) -> dict:
    query = inputs["query"]
    result = ask_finance_agent_v2(query)
    return {"result": result.get("answer", str(result))}

def get_intent_llm(query: str) -> str:
    prompt = f"""Classify the intent of the following query into exactly ONE of these categories:
- cost_breakdown
- cost_lookup
- budget_status
- comparison
- variance
- overrun_risk
- financial_summary
- aggregation
- out_of_scope

Query: {query}
Respond with EXACTLY the category name, nothing else."""
    
    judge_llm = OllamaLLM(model="llama3", temperature=0.0)
    response = judge_llm.invoke(prompt).strip().lower()
    
    # Clean up response in case LLM is chatty
    valid_intents = ["cost_breakdown", "cost_lookup", "budget_status", "comparison", 
                     "variance", "overrun_risk", "financial_summary", "aggregation", "out_of_scope"]
    for valid in valid_intents:
        if valid in response:
            return valid
    return "out_of_scope"

def extract_all_numbers(text):
    text = text.replace('$', '').replace(',', '')
    matches = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', text)
    return [float(m) for m in matches]

def v4_hybrid_evaluator(run, example):
    expected = str(example.outputs.get("expected", ""))
    actual = str(run.outputs.get("result", ""))
    query = str(example.inputs.get("query", ""))
    
    # LAYER 1: Intent Validation (via LLM)
    intent = get_intent_llm(query)
    
    # LAYER 2 & 3: Critical Extraction & Numeric Validation
    math_score = 1
    math_comment = ""
    warning = 0
    
    # Catch "not applicable" vs "over budget" logical errors across all intents
    if "not applicable" in expected.lower():
        if "over_budget" in actual.lower() or "over budget" in actual.lower() or "under budget" in actual.lower() or "under_budget" in actual.lower():
            math_score = 0
            math_comment = "Failed: Ignored 'not applicable' budget status."

    # Extract subsystem ID explicitly
    subsystem_match = re.search(r'subsystem\s+(\d+)', expected, re.IGNORECASE)
    expected_sub_id = float(subsystem_match.group(1)) if subsystem_match else None
    
    act_subsystem_match = re.search(r'subsystem\s+(\d+)', actual, re.IGNORECASE)
    actual_sub_id = float(act_subsystem_match.group(1)) if act_subsystem_match else None

    if expected_sub_id is not None:
        if actual_sub_id is None:
            warning = 1 # Missing = Warning
        elif actual_sub_id != expected_sub_id:
            math_score = 0 # Wrong = Failure
            math_comment = f"Failed: Wrong subsystem ID. Expected {expected_sub_id}, got {actual_sub_id}."

    # LAYER 2: Critical Field Extraction (Truncating irrelevant expected numbers)
    if intent == "cost_breakdown" and "Sum of direct costs" in expected:
        expected = expected.split("Sum of direct costs")[0]
        
    exp_nums = extract_all_numbers(expected)
    act_nums = extract_all_numbers(actual)
    
    # Remove subsystem IDs from numeric arrays to avoid false positives on ID matching
    if expected_sub_id is not None and expected_sub_id in exp_nums:
        exp_nums = [x for x in exp_nums if x != expected_sub_id]
    if actual_sub_id is not None and actual_sub_id in act_nums:
        act_nums = [x for x in act_nums if x != actual_sub_id]

    missing = []
    for en in exp_nums:
        # Ignore percentage symbols if the number is exact but formatting differs slightly,
        # but for V4 we strictly require all variances and costs to match exactly
        found = any(abs(en - an) < 0.1 for an in act_nums)
        if not found:
            missing.append(en)
            
    if missing and math_score == 1:
        math_score = 0
        math_comment = f"Failed: Missing required numeric field or sign flip: {missing}"

    if math_score == 1 and not math_comment:
        math_comment = f"Passed deterministic checks for intent: {intent}"

    # LAYER 4: Semantic Validation
    judge_llm = OllamaLLM(model="llama3", temperature=0.0)
    prompt = f"""You are a quality assurance auditor.
The mathematical correctness has already been verified perfectly.
Your job is ONLY to judge the conversational tone, clarity, and completeness.

Does the ACTUAL ANSWER clearly and politely convey the information found in the EXPECTED ANSWER?
Reply with exactly 'CORRECT' if it is well-formatted and polite.
Reply with exactly 'INCORRECT' if it is gibberish, rude, or cuts off mid-sentence.

EXPECTED: {expected}
ACTUAL: {actual}

Verdict:"""

    verdict = judge_llm.invoke(prompt).strip().upper()
    semantic_score = 1 if verdict.startswith("CORRECT") else 0
    
    confidence_score = math_score * semantic_score
    
    return [
        {"key": "v4_confidence_score", "score": confidence_score, "comment": f"Math: {math_score}, Semantic: {semantic_score}"},
        {"key": "v4_math_score", "score": math_score, "comment": math_comment},
        {"key": "v4_semantic_score", "score": semantic_score, "comment": verdict},
        {"key": "v4_subsystem_id_warning", "score": warning, "comment": "Missing subsystem ID" if warning else "OK"}
    ]

def main():
    if not client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset {DATASET_NAME} not found.")
        return
        
    print("Starting Query-Aware V4 Evaluation...")
    
    results = evaluate(
        agent_target,
        data=DATASET_NAME,
        evaluators=[v4_hybrid_evaluator], # single evaluator returning multiple metrics
        experiment_prefix="V4.1_LLM_Intent_Eval",
    )
    print("\nEvaluation complete!")

if __name__ == "__main__":
    main()
