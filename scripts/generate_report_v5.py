import os
from langsmith import Client # type: ignore
from datetime import datetime
from dotenv import load_dotenv

def generate_report():
    load_dotenv()
    print("Connecting to LangSmith...")
    client = Client()
    
    dataset_name = "Cost_Finance_Evaluation"
    
    try:
        projects = list(client.list_projects(reference_dataset_name=dataset_name))
        if not projects:
            print("No test projects found for this dataset.")
            return
            
        # Find the latest V5 project
        v5_projects = [p for p in projects if "V5_Project_Grade_Eval" in p.name]
        if not v5_projects:
            print("No V5 projects found.")
            return
        latest_project = sorted(v5_projects, key=lambda p: p.start_time, reverse=True)[0]
        print(f"Latest Project: {latest_project.name}")
        
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return

    print("Fetching runs and feedback...")
    runs = list(client.list_runs(project_id=latest_project.id, is_root=True))
    
    total_runs = len(runs)
    passed = 0
    warnings = 0
    failed = 0
    critical = 0
    
    semantic_passes = 0
    
    intent_stats = {} # intent -> {"total": 0, "passed": 0}
    
    critical_cases = []
    fail_cases = []
    warning_cases = []
    
    for run in runs:
        feedback_iter = client.list_feedback(run_ids=[run.id])
        feedbacks = list(feedback_iter)
        
        math_score = 0
        semantic_score = 0
        severity = "PASS"
        intent = "unknown"
        math_comment = ""
        
        for fb in feedbacks:
            if fb.key == "v5_math_score":
                math_score = fb.score or 0
                math_comment = fb.comment or ""
            elif fb.key == "v5_semantic_score":
                semantic_score = fb.score or 0
            elif fb.key == "v5_severity_level":
                severity = fb.comment or "PASS"
            elif fb.key == "v5_intent":
                intent = fb.comment or "unknown"
                
        if intent not in intent_stats:
            intent_stats[intent] = {"total": 0, "passed": 0}
            
        intent_stats[intent]["total"] += 1
        
        if math_score == 1:
            intent_stats[intent]["passed"] += 1
            if severity == "WARNING":
                warnings += 1
                warning_cases.append(math_comment)
            else:
                passed += 1
        else:
            if severity == "CRITICAL":
                critical += 1
                critical_cases.append(math_comment)
            else:
                failed += 1
                fail_cases.append(math_comment)
                
        if semantic_score == 1:
            semantic_passes += 1

    math_accuracy = ((passed + warnings) / total_runs * 100) if total_runs > 0 else 0
    semantic_accuracy = (semantic_passes / total_runs * 100) if total_runs > 0 else 0
    
    print(f"Finished processing. Passed: {passed}, Warnings: {warnings}, Failed: {failed}, Critical: {critical}")
    
    md_content = f"""# V5 Project-Grade Evaluation Report

**Date**: {datetime.now().strftime('%B %d, %Y')}
**Test Run**: `{latest_project.name}`

## 📊 High-Level Metrics
- **Total Queries**: {total_runs}
- **Math Accuracy**: {math_accuracy:.1f}%
- **Semantic Quality**: {semantic_accuracy:.1f}%

### Severity Breakdown
- **{passed} Pass** (INFO: Perfect Match)
- **{warnings} Warning** (Missing IDs but math passed)
- **{failed} Fail** (Wrong subsystem, missing fields)
- **{critical} Critical** (Sign reversals, Business logic contradictions)

## 🎯 Intent Accuracy Stats
"""
    for intnt, stats in sorted(intent_stats.items(), key=lambda x: x[0]):
        acc = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        md_content += f"- **{intnt.replace('_', ' ').title()}**: {acc:.1f}% ({stats['passed']}/{stats['total']})\\n"

    md_content += """
## 🚨 Deep Dive: Critical Failures
"""
    if not critical_cases:
        md_content += "*No critical business logic failures!*\\n"
    else:
        for idx, comment in enumerate(critical_cases[:10]):
            md_content += f"- {comment}\\n"

    md_content += """
## ❌ Deep Dive: Standard Failures
"""
    if not fail_cases:
        md_content += "*No standard math failures!*\\n"
    else:
        for idx, comment in enumerate(fail_cases[:10]):
            md_content += f"- {comment}\\n"

    report_path = os.path.join("docs", "evaluation_reports", "eval_report_v5_100.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"Report successfully written to {report_path}!")

if __name__ == "__main__":
    generate_report()
