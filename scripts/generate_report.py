import os
from langsmith import Client # type: ignore
from datetime import datetime
from dotenv import load_dotenv

def generate_report():
    load_dotenv()
    print("Connecting to LangSmith...")
    client = Client()
    
    dataset_name = "Cost_Finance_Evaluation"
    
    print(f"Finding latest evaluation project for dataset: {dataset_name}")
    try:
        # Get all projects (test runs) associated with this dataset
        projects = list(client.list_projects(reference_dataset_name=dataset_name))
        if not projects:
            print("No test projects found for this dataset.")
            return
            
        # Sort by start time to get the latest one
        # Handle cases where start_time might be tricky
        latest_project = sorted(projects, key=lambda p: p.start_time, reverse=True)[0]
        print(f"Latest Project: {latest_project.name}")
        
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return

    print("Fetching runs and feedback...")
    runs = list(client.list_runs(project_id=latest_project.id, is_root=True))
    
    total_runs = len(runs)
    passed = 0
    failed = 0
    
    semantic_diffs = []
    failed_cases = []
    
    for run in runs:
        # Get feedback for the run
        feedback_iter = client.list_feedback(run_ids=[run.id])
        feedbacks = list(feedback_iter)
        
        score = 0
        if feedbacks:
            # Usually we expect one exact_match feedback
            score = feedbacks[0].score or 0
            
        if score >= 1:
            passed += 1
        else:
            failed += 1
            
        # Get I/O
        query = run.inputs.get("query", "") if run.inputs else ""
        actual_output = run.outputs.get("result", "") if run.outputs else ""
        
        # In evaluation runs, expected output is stored in reference_example
        expected_output = "N/A"
        if run.reference_example_id:
            example = client.read_example(run.reference_example_id)
            if example and example.outputs:
                expected_output = example.outputs.get("expected", example.outputs.get("result", ""))
                
        # Check for "Semantic Pass with Diff"
        # i.e., score is 1, but text is not identical
        if score >= 1 and expected_output != "N/A" and str(actual_output).strip().lower() != str(expected_output).strip().lower():
            semantic_diffs.append({
                "query": query,
                "expected": expected_output,
                "actual": actual_output
            })
            
        if score == 0:
            failed_cases.append({
                "query": query,
                "expected": expected_output,
                "actual": actual_output
            })

    accuracy = (passed / total_runs * 100) if total_runs > 0 else 0
    
    print(f"Finished processing. Passed: {passed}, Failed: {failed}")
    
    # Generate Markdown content
    md_content = f"""# V2 Semantic Evaluation Report (Auto-Generated)

**Date**: {datetime.now().strftime('%B %d, %Y')}
**Dataset**: `{dataset_name}`
**Test Run**: `{latest_project.name}`
**Evaluator**: LLM-as-a-Judge (Semantic Match)

## Executive Summary
This report captures the evaluation results of the LangGraph Agent V2 against the expanded evaluation dataset.

## Performance Metrics
- **Total Test Cases**: {total_runs}
- **Passed (Semantic Match)**: {passed}
- **Failed**: {failed}
- **Overall Accuracy**: {accuracy:.1f}%

## 🔍 Semantic Passes (The Magic of LLM-as-a-Judge)
These are cases where the agent passed (Score = 1) even though the text was completely different. It successfully matched the *intent* and *data*, proving semantic evaluation works!

"""
    if not semantic_diffs:
        md_content += "*No semantic diffs found.*\\n"
    else:
        for idx, diff in enumerate(semantic_diffs[:5]): # Show top 5
            md_content += f"### Example {idx+1}:\\n"
            md_content += f"- **Query**: {diff['query']}\\n"
            md_content += f"- **Expected**: {diff['expected']}\\n"
            md_content += f"- **Actual**: {diff['actual']}\\n\\n"

    md_content += """## ❌ Failed Cases
These are queries that the agent failed to answer correctly (or hallucinated).

"""
    if not failed_cases:
        md_content += "*Zero failures! Perfect score!*\\n"
    else:
        for idx, fail in enumerate(failed_cases[:10]): # Show top 10
            md_content += f"### Failure {idx+1}:\\n"
            md_content += f"- **Query**: {fail['query']}\\n"
            md_content += f"- **Expected**: {fail['expected']}\\n"
            md_content += f"- **Actual**: {fail['actual']}\\n\\n"
            
    md_content += """
## Recommendations for V3
- **Aggregate Analytics Tool**: Aggregate queries (like "Find severe overruns") failed because the planner defaults to `subsystem_id: 1` when no ID is present. We need a system-wide analytical tool (Text-to-SQL or similar).
"""

    report_path = os.path.join("docs", "evaluation_reports", "eval_report_v2_100.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"Report successfully written to {report_path}!")

if __name__ == "__main__":
    generate_report()
