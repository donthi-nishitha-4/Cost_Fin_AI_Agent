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

def extract_numbers(text):
    """Extract all floats from text, respecting signs."""
    text = text.replace('$', '').replace(',', '')
    # Match optional sign, optional digits, optional decimal point and digits
    # Or just digits
    matches = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', text)
    return [float(m) for m in matches]

def deterministic_math_match(run, example):
    """Evaluates strict mathematical correctness."""
    expected = str(example.outputs.get("expected", ""))
    actual = str(run.outputs.get("result", ""))
    
    # Rule 1: Catch "not applicable" vs "over budget" logical errors
    if "not applicable" in expected.lower() and ("over_budget" in actual.lower() or "over budget" in actual.lower() or "under budget" in actual.lower() or "under_budget" in actual.lower()):
        return {"key": "math_score", "score": 0, "comment": "Failed: Ignored 'not applicable' budget status."}

    # Extract subsystem ID from expected string if it exists
    subsystem_match = re.search(r'subsystem\s+(\d+)', expected, re.IGNORECASE)
    subsystem_id = float(subsystem_match.group(1)) if subsystem_match else None

    # Rule 2: Strict numerical presence and sign matching
    exp_nums = extract_numbers(expected)
    act_nums = extract_numbers(actual)
    
    missing = []
    for en in exp_nums:
        # Ignore the exact subsystem ID if it's the only thing missing
        if subsystem_id is not None and abs(en - subsystem_id) < 0.01:
            continue
            
        found = any(abs(en - an) < 0.1 for an in act_nums)
        if not found:
            missing.append(en)
            
    if missing:
        return {"key": "math_score", "score": 0, "comment": f"Failed: Missing expected numbers or sign flip: {missing}"}

    return {"key": "math_score", "score": 1, "comment": "Passed strict deterministic math checks."}

def semantic_quality_match(run, example):
    """Uses LLM to evaluate tone and conversational completeness."""
    actual = str(run.outputs.get("result", ""))
    expected = str(example.outputs.get("expected", ""))
    
    judge_llm = OllamaLLM(model="llama3", temperature=0.0)
    prompt = f"""You are a quality assurance auditor grading an AI agent.
The mathematical correctness of the ACTUAL ANSWER has already been verified perfectly.
Your job is ONLY to judge the conversational tone, clarity, and completeness.

Does the ACTUAL ANSWER clearly and politely convey the information found in the EXPECTED ANSWER?
Reply with exactly 'CORRECT' if it is well-formatted and polite.
Reply with exactly 'INCORRECT' if it is gibberish, rude, or cuts off mid-sentence.

EXPECTED: {expected}
ACTUAL: {actual}

Verdict:"""

    verdict = judge_llm.invoke(prompt).strip().upper()
    score = 1 if verdict.startswith("CORRECT") else 0
    return {"key": "semantic_score", "score": score, "comment": verdict}

def confidence_score(run, example):
    """Combines Math and Semantic scores."""
    # Since evaluators run in parallel in LangSmith, we calculate it natively inside the dashboard 
    # or just return a combined result by running the logic here.
    math_result = deterministic_math_match(run, example)
    sem_result = semantic_quality_match(run, example)
    
    final_score = math_result["score"] * sem_result["score"]
    comment = f"Math: {math_result['score']} | Semantic: {sem_result['score']} | Reason: {math_result['comment']}"
    
    return {"key": "confidence_score", "score": final_score, "comment": comment}

def main():
    if not client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset {DATASET_NAME} not found. Please run evaluate_v2 to seed it.")
        return
        
    print("Starting Hybrid Deterministic + Semantic V3 Evaluation...")
    
    results = evaluate(
        agent_target,
        data=DATASET_NAME,
        evaluators=[deterministic_math_match, semantic_quality_match, confidence_score],
        experiment_prefix="V3_Hybrid_Eval",
    )
    
    print("\nEvaluation complete! Check your LangSmith dashboard.")

if __name__ == "__main__":
    main()
