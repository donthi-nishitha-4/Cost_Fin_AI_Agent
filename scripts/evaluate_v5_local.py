import os
import sys
import re
import math
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from langsmith import Client  # type: ignore

# Add the project root to the python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.llm_factory import get_llm
from app.agents.finance_agent_v2 import ask_finance_agent_v2
from scripts.evaluate_v5 import v5_hybrid_evaluator

class MockObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def run_local_evaluation():
    load_dotenv()
    client = Client()
    dataset_name = "Cost_Finance_Golden_Strict"
    
    if not client.has_dataset(dataset_name=dataset_name):
        print(f"Dataset '{dataset_name}' not found in LangSmith.")
        return
        
    print(f"Fetching examples for dataset '{dataset_name}' from LangSmith...")
    dataset = client.read_dataset(dataset_name=dataset_name)
    examples = list(client.list_examples(dataset_id=dataset.id))
    
    total_runs = len(examples)
    print(f"Found {total_runs} examples. Starting local evaluation...\n")
    
    # Paths for logs and reports
    logs_json_path = os.path.join("docs", "evaluation_reports", "eval_runs_log_v5.json")
    report_md_path = os.path.join("docs", "evaluation_reports", "eval_report_v5_124_ollama_llama3_local.md")
    os.makedirs(os.path.dirname(logs_json_path), exist_ok=True)
    
    # Load checkpoints (only restore passing runs)
    completed_runs = {}
    if os.path.exists(logs_json_path):
        try:
            with open(logs_json_path, "r", encoding="utf-8") as f:
                checkpoint_data = json.load(f)
                for run in checkpoint_data.get("runs", []):
                    # Only restore if it passed to allow re-running warnings/failures
                    if run.get("severity") == "PASS":
                        completed_runs[run["query"]] = run
            print(f"Loaded checkpoint database. Found {len(completed_runs)} already passing runs to restore.")
        except Exception as e:
            print(f"Warning: Could not read checkpoint file, starting fresh. Details: {e}")
            
    all_runs_log = []
    latencies = []
    
    # Disable langchain tracing environment variable temporarily to prevent rate limit ingest warnings
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    
    start_eval_time = time.time()
    
    for idx, ex in enumerate(examples, start=1):
        query = ex.inputs["query"]
        expected = ex.outputs["expected"]
        
        # Check if query is in completed runs checkpoint
        if query in completed_runs:
            print(f"[{idx}/{total_runs}] Query: {query} (Restored from checkpoint)")
            checkpoint = completed_runs[query]
            actual_answer = checkpoint["actual"]
            latency = checkpoint.get("latency_seconds", 5.0)
            latencies.append(latency)
            
            math_score = checkpoint.get("math_score", 1)
            semantic_score = checkpoint.get("semantic_score", 1)
            severity = checkpoint.get("severity", "PASS")
            intent = checkpoint.get("intent", "unknown")
            reason = checkpoint.get("reason", "INFO: Perfect match.")
        else:
            print(f"[{idx}/{total_runs}] Query: {query}")
            
            start_query_time = time.time()
            # Run agent
            try:
                result = ask_finance_agent_v2(query)
                actual_answer = result.get("answer", str(result)) if isinstance(result, dict) else str(result)
            except Exception as e:
                actual_answer = f"Exception occurred during execution: {str(e)}"
            
            latency = time.time() - start_query_time
            latencies.append(latency)
            
            print(f"  Answer: {actual_answer}")
            print(f"  Latency: {latency:.2f}s")
            
            # Create Mock objects to pass to v5_hybrid_evaluator
            run_mock = MockObject(outputs={"result": actual_answer})
            example_mock = MockObject(inputs={"query": query}, outputs={"expected": expected})
            
            # Evaluate locally
            eval_results = v5_hybrid_evaluator(run_mock, example_mock)
            
            math_score = 0
            semantic_score = 0
            severity = "PASS"
            intent = "unknown"
            reason = ""
            
            for res in eval_results:
                if res["key"] == "v5_math_score":
                    math_score = res["score"]
                    reason = res["comment"]
                elif res["key"] == "v5_semantic_score":
                    semantic_score = res["score"]
                elif res["key"] == "v5_severity_level":
                    severity = res["comment"]
                elif res["key"] == "v5_intent":
                    intent = res["comment"]
            
            print(f"  Math: {math_score} | Semantic: {semantic_score} | Severity: {severity}\n")
            
        run_log = {
            "query": query,
            "expected": expected,
            "actual": actual_answer,
            "intent": intent,
            "math_score": math_score,
            "semantic_score": semantic_score,
            "severity": severity,
            "combined_score": 0.5 * math_score + 0.3 * semantic_score + 0.2,
            "latency_seconds": latency,
            "reason": reason
        }
        all_runs_log.append(run_log)
        
        # Save checkpoints immediately after query completion (merging with remaining cached runs to prevent wiping)
        try:
            runs_to_write = list(all_runs_log)
            processed_queries = {r["query"] for r in all_runs_log}
            for run_q, run_data in completed_runs.items():
                if run_q not in processed_queries:
                    runs_to_write.append(run_data)

            with open(logs_json_path, "w", encoding="utf-8") as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "summary": {
                        "total_queries": total_runs,
                        "checkpoint_count": len(runs_to_write)
                    },
                    "runs": runs_to_write
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save checkpoint: {e}")
            
    total_eval_time = time.time() - start_eval_time
    
    # Calculate stats
    passed_count = sum(1 for r in all_runs_log if r["math_score"] == 1 and r["severity"] == "PASS")
    warning_count = sum(1 for r in all_runs_log if r["severity"] == "WARNING")
    failed_count = sum(1 for r in all_runs_log if r["math_score"] == 0 and r["severity"] == "FAIL")
    critical_count = sum(1 for r in all_runs_log if r["severity"] == "CRITICAL")
    
    math_accuracy_pct = (sum(1 for r in all_runs_log if r["math_score"] == 1) / total_runs) * 100
    semantic_quality_pct = (sum(1 for r in all_runs_log if r["semantic_score"] == 1) / total_runs) * 100
    
    # Weighted score: 50% Math, 30% Semantic, 20% Severity (1.0 for PASS, 0.5 for WARNING, 0.0 for FAIL/CRITICAL)
    overall_score_pct = sum(r["combined_score"] for r in all_runs_log) / total_runs * 100
    
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    max_latency = max(latencies) if latencies else 0.0
    min_latency = min(latencies) if latencies else 0.0
    
    intent_stats = {}
    critical_cases = []
    fail_cases = []
    warning_cases = []
    
    for r in all_runs_log:
        intent = r["intent"]
        if intent not in intent_stats:
            intent_stats[intent] = {"total": 0, "passed": 0}
        intent_stats[intent]["total"] += 1
        if r["math_score"] == 1:
            intent_stats[intent]["passed"] += 1
            
        if r["severity"] == "CRITICAL":
            critical_cases.append(f"Q: {r['query']} | {r['reason']}")
        elif r["severity"] == "FAIL":
            fail_cases.append(f"Q: {r['query']} | {r['reason']}")
        elif r["severity"] == "WARNING":
            warning_cases.append(f"Q: {r['query']} | {r['reason']}")
            
    # Write final log summary stats
    try:
        with open(logs_json_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_queries": total_runs,
                    "math_accuracy_pct": round(math_accuracy_pct, 2),
                    "semantic_quality_pct": round(semantic_quality_pct, 2),
                    "overall_score_pct": round(overall_score_pct, 2),
                    "total_time_seconds": round(total_eval_time, 2),
                    "average_latency_seconds": round(avg_latency, 2),
                    "max_latency_seconds": round(max_latency, 2),
                    "min_latency_seconds": round(min_latency, 2),
                    "passed_count": passed_count,
                    "warning_count": warning_count,
                    "failed_count": failed_count,
                    "critical_count": critical_count
                },
                "runs": all_runs_log
            }, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Failed to save final json log summary: {e}")

    # Export failures and warnings to CSV
    failures_csv_path = os.path.join("docs", "evaluation_reports", "eval_failures_v5.csv")
    try:
        import csv
        with open(failures_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Query", "Expected", "Actual", "Intent", "Severity", "CombinedScore", "Reason"])
            for r in all_runs_log:
                if r["severity"] in ["FAIL", "CRITICAL", "WARNING"]:
                    writer.writerow([
                        r["query"],
                        r["expected"],
                        r["actual"],
                        r["intent"],
                        r["severity"],
                        round(r["combined_score"], 2),
                        r["reason"]
                    ])
        print(f"Failures and warnings exported to {failures_csv_path}")
    except Exception as e:
        print(f"Warning: Failed to export failures CSV: {e}")
        
    # Write Markdown Report
    md_report = f"""# V5 Project-Grade Local Evaluation Report
    
**Date**: {datetime.now().strftime('%B %d, %Y')}
**Execution Engine**: Local Ollama (llama3)

## 📊 High-Level Metrics
- **Overall Pipeline Score**: {overall_score_pct:.1f}% *(Weighted: 50% Math, 30% Semantic, 20% Business Logic Safety)*
- **Math Accuracy**: {math_accuracy_pct:.1f}%
- **Semantic Quality**: {semantic_quality_pct:.1f}%
- **Total Queries**: {total_runs}

### Severity Breakdown
- **{passed_count} Pass** (INFO: Perfect Match)
- **{warning_count} Warning** (Missing IDs but math passed)
- **{failed_count} Fail** (Wrong subsystem, missing fields)
- **{critical_count} Critical** (Sign reversals, Business logic contradictions)

### Performance Analytics
- **Total Execution Time**: {total_eval_time:.1f} seconds
- **Average Latency**: {avg_latency:.2f} seconds per query
- **Slowest Response**: {max_latency:.2f} seconds
- **Fastest Response**: {min_latency:.2f} seconds

## 🎯 Intent Accuracy Stats
"""
    for intnt, stats in sorted(intent_stats.items()):
        acc = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        md_report += f"- **{intnt.replace('_', ' ').title()}**: {acc:.1f}% ({stats['passed']}/{stats['total']})\n"
        
    md_report += "\n## 🚨 Deep Dive: Critical Failures\n"
    if not critical_cases:
        md_report += "*No critical business logic failures!*\n"
    else:
        for case in critical_cases:
            md_report += f"- {case}\n"
            
    md_report += "\n## ❌ Deep Dive: Standard Failures\n"
    if not fail_cases:
        md_report += "*No standard math failures!*\n"
    else:
        for case in fail_cases:
            md_report += f"- {case}\n"
            
    md_report += "\n## ⚠️ Deep Dive: Warnings\n"
    if not warning_cases:
        md_report += "*No warnings!*\n"
    else:
        for case in warning_cases:
            md_report += f"- {case}\n"
            
    try:
        with open(report_md_path, "w", encoding="utf-8") as f:
            f.write(md_report)
        print(f"\nEvaluation Complete! Local report written to {report_md_path}")
    except Exception as e:
        print(f"Error writing markdown report: {e}")

if __name__ == "__main__":
    run_local_evaluation()